import asyncio
import aiohttp
import json
import logging
import os
import re
import hashlib
from typing import Dict, Any, List, Set, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from urllib.parse import urlparse, quote_plus
from dataclasses import dataclass, asdict
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from lib.dork_generator import DorkGenerator
from utils.remove_result_dedup import ResultDeduplicator
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Configuration ====================
@dataclass
class SearchConfig:
    max_results_per_dork: int = 50
    max_concurrent_requests: int = 5
    quota_limit: int = 100
    quota_warning_threshold: float = 0.8
    request_timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 2.0
    cache_ttl: int = 3600  # 1 hour
    enable_fallback_browse: bool = True
    enable_entity_extraction: bool = True
    enable_deduplication: bool = True
    min_snippet_length: int = 50
    
config = SearchConfig()

# ==================== Quota & Rate Limiting ====================
class QuotaManager:
    def __init__(self, limit: int):
        self.limit = limit
        self.used = 0
        self.lock = asyncio.Lock()
        self.reset_time = datetime.now() + timedelta(days=1)
    
    async def acquire(self) -> bool:
        async with self.lock:
            if datetime.now() >= self.reset_time:
                self.used = 0
                self.reset_time = datetime.now() + timedelta(days=1)
            
            if self.used >= self.limit:
                logger.error(f"Quota exhausted: {self.used}/{self.limit}")
                return False
            
            self.used += 1
            if self.used >= self.limit * config.quota_warning_threshold:
                logger.warning(f"Quota warning: {self.used}/{self.limit}")
            return True
    
    def get_remaining(self) -> int:
        return max(0, self.limit - self.used)

quota_manager = QuotaManager(config.quota_limit)

# ==================== Cache System ====================
class SimpleCache:
    def __init__(self):
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        async with self.lock:
            if key in self.cache:
                data, timestamp = self.cache[key]
                if time.time() - timestamp < config.cache_ttl:
                    logger.info(f"Cache hit: {key[:50]}...")
                    return data
                else:
                    del self.cache[key]
        return None
    
    async def set(self, key: str, value: Any):
        async with self.lock:
            self.cache[key] = (value, time.time())
    
    async def clear_expired(self):
        async with self.lock:
            current_time = time.time()
            expired = [k for k, (_, t) in self.cache.items() if current_time - t >= config.cache_ttl]
            for k in expired:
                del self.cache[k]

cache = SimpleCache()

# ==================== Entity Extraction ====================
class EntityExtractor:
    @staticmethod
    def extract_emails(text: str) -> Set[str]:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = set(re.findall(pattern, text))
        valid_emails = set()
        for email in emails:
            try:
                valid = validate_email(email, check_deliverability=False)
                valid_emails.add(valid.email)
            except EmailNotValidError:
                pass
        return valid_emails
    
    @staticmethod
    def extract_phone_numbers(text: str) -> Set[str]:
        phones = set()
        for match in phonenumbers.PhoneNumberMatcher(text, None):
            phones.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
        return phones
    
    @staticmethod
    def extract_urls(text: str) -> Set[str]:
        pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        return set(re.findall(pattern, text))
    
    @staticmethod
    def extract_social_handles(text: str) -> Dict[str, Set[str]]:
        handles = {
            'twitter': set(re.findall(r'@([A-Za-z0-9_]{1,15})', text)),
            'linkedin': set(re.findall(r'linkedin\.com/in/([A-Za-z0-9-]+)', text)),
            'github': set(re.findall(r'github\.com/([A-Za-z0-9-]+)', text)),
            'instagram': set(re.findall(r'instagram\.com/([A-Za-z0-9_.]+)', text))
        }
        return {k: v for k, v in handles.items() if v}
    
    @staticmethod
    def extract_dates(text: str) -> Set[str]:
        patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
            r'\b\d{2}/\d{2}/\d{4}\b',  # MM/DD/YYYY
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
        ]
        dates = set()
        for pattern in patterns:
            dates.update(re.findall(pattern, text, re.IGNORECASE))
        return dates
    
    @staticmethod
    def extract_all(text: str) -> Dict[str, Any]:
        return {
            'emails': list(EntityExtractor.extract_emails(text)),
            'phones': list(EntityExtractor.extract_phone_numbers(text)),
            'urls': list(EntityExtractor.extract_urls(text)),
            'social_handles': {k: list(v) for k, v in EntityExtractor.extract_social_handles(text).items()},
            'dates': list(EntityExtractor.extract_dates(text))
        }

# ==================== Advanced Web Scraping ====================
class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    async def extract_structured_data(self, html: str, url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract meta information
        meta_data = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_data[name] = content
        
        # Extract main content
        content_selectors = [
            ('article', {}),
            ('div', {'class': re.compile(r'content|main|article|post', re.I)}),
            ('div', {'id': re.compile(r'content|main|article|post', re.I)}),
        ]
        
        main_content = ''
        for tag, attrs in content_selectors:
            element = soup.find(tag, attrs)
            if element:
                main_content = element.get_text(separator=' ', strip=True)
                break
        
        if not main_content:
            main_content = soup.get_text(separator=' ', strip=True)
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'meta': meta_data,
            'content': main_content[:2000],  # Limit content size
            'links': [a.get('href') for a in soup.find_all('a', href=True)][:50]
        }
    
    async def browse_url(self, session: aiohttp.ClientSession, url: str, target: str) -> Dict[str, Any]:
        try:
            async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=config.request_timeout)) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    structured_data = await self.extract_structured_data(html, url)
                    
                    # Extract entities if enabled
                    if config.enable_entity_extraction:
                        entities = EntityExtractor.extract_all(structured_data['content'])
                        structured_data['entities'] = entities
                    
                    return structured_data
                else:
                    return {'error': f'Status {resp.status}', 'url': url}
        except asyncio.TimeoutError:
            return {'error': 'Timeout', 'url': url}
        except Exception as e:
            return {'error': str(e), 'url': url}

# ==================== Result Scoring & Ranking ====================
class ResultScorer:
    @staticmethod
    def calculate_relevance_score(result: Dict[str, Any], target: str) -> float:
        score = 0.0
        target_lower = target.lower()
        
        # Title matching
        title = result.get('title', '').lower()
        if target_lower in title:
            score += 3.0
        
        # Snippet matching
        snippet = result.get('snippet', '').lower()
        target_count = snippet.count(target_lower)
        score += min(target_count * 0.5, 2.0)
        
        # Domain authority (simple heuristic)
        domain = result.get('displayLink', '').lower()
        authoritative_domains = ['linkedin.com', 'github.com', 'wikipedia.org', 'reuters.com', 'nytimes.com']
        if any(auth_domain in domain for auth_domain in authoritative_domains):
            score += 2.0
        
        # Snippet length (prefer substantial content)
        snippet_length = len(snippet)
        if snippet_length >= config.min_snippet_length:
            score += 1.0
        
        # Has extracted entities
        if result.get('entities') and any(result['entities'].values()):
            score += 1.5
        
        return score
    
    @staticmethod
    def rank_results(results: List[Dict[str, Any]], target: str) -> List[Dict[str, Any]]:
        for result in results:
            result['relevance_score'] = ResultScorer.calculate_relevance_score(result, target)
        
        ranked = sorted(results, key=lambda x: x.get('relevance_score', 0), reverse=True)
        return ranked

# ==================== Retry Logic ====================
async def retry_async(func, *args, **kwargs):
    for attempt in range(config.retry_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == config.retry_attempts - 1:
                raise
            wait_time = config.retry_delay * (2 ** attempt)
            logger.warning(f"Retry {attempt + 1}/{config.retry_attempts} after {wait_time}s: {e}")
            await asyncio.sleep(wait_time)

# ==================== Core Search Functions ====================
async def fetch_search_results(
    session: aiohttp.ClientSession,
    api_key: str,
    cx_id: str,
    query: str,
    start: int = 1,
    num: int = 10
) -> Dict[str, Any]:
    """Fetch results from Google Custom Search API with retry logic."""
    cache_key = f"search_{hashlib.md5(f'{query}_{start}_{num}'.encode()).hexdigest()}"
    
    # Check cache
    cached = await cache.get(cache_key)
    if cached:
        return cached
    
    # Check quota
    if not await quota_manager.acquire():
        return {'error': 'Quota exhausted'}
    
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': cx_id,
        'q': query,
        'num': num,
        'start': start
    }
    
    try:
        result = await retry_async(
            lambda: session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=config.request_timeout))
        )
        
        async with result as resp:
            if resp.status == 200:
                data = await resp.json()
                items = data.get('items', [])
                
                cleaned = []
                for item in items:
                    snippet = item.get('snippet', '')
                    cleaned_item = {
                        'title': item.get('title', '').strip(),
                        'link': item.get('link', ''),
                        'snippet': snippet.strip(),
                        'displayLink': item.get('displayLink', ''),
                        'pagemap': item.get('pagemap', {})
                    }
                    
                    # Extract entities from snippet
                    if config.enable_entity_extraction:
                        cleaned_item['entities'] = EntityExtractor.extract_all(snippet)
                    
                    cleaned.append(cleaned_item)
                
                result_data = {
                    'results': cleaned,
                    'totalResults': data.get('searchInformation', {}).get('totalResults', 0),
                    'searchTime': data.get('searchInformation', {}).get('searchTime', 0)
                }
                
                # Cache results
                await cache.set(cache_key, result_data)
                
                return result_data
            elif resp.status == 429:
                logger.error("Rate limited by API")
                return {'error': 'Rate limited'}
            else:
                return {'error': f'Status {resp.status}'}
                
    except Exception as e:
        logger.error(f"Search error for '{query}': {e}")
        return {'error': str(e)}

async def execute_single_dork(
    session: aiohttp.ClientSession,
    api_key: str,
    cx_id: str,
    target: str,
    dork_name: str,
    query: str,
    max_results: int
) -> Dict[str, Any]:
    """Execute a single dork with pagination."""
    all_results = []
    total_results = 0
    pages_fetched = 0
    start = 1
    
    while len(all_results) < max_results and start <= 91:  # Google CSE limit
        page_result = await fetch_search_results(
            session, api_key, cx_id, query, start, min(10, max_results - len(all_results))
        )
        
        if 'error' in page_result:
            logger.error(f"Dork '{dork_name}' failed: {page_result['error']}")
            break
        
        results = page_result.get('results', [])
        if not results:
            break
        
        all_results.extend(results)
        
        if pages_fetched == 0:
            total_results = int(page_result.get('totalResults', 0))
        
        pages_fetched += 1
        start += 10
        
        # Rate limiting between pages
        await asyncio.sleep(0.5)
    
    # Fallback browsing for low-yield dorks
    if config.enable_fallback_browse and len(all_results) > 0 and len(all_results) < 5:
        scraper = WebScraper()
        top_url = all_results[0]['link']
        logger.info(f"Fallback browse for '{dork_name}': {top_url}")
        browse_result = await scraper.browse_url(session, top_url, target)
        if 'error' not in browse_result:
            all_results.append({
                'title': browse_result.get('title', 'Scraped Content'),
                'link': browse_result['url'],
                'snippet': browse_result.get('content', '')[:500],
                'displayLink': urlparse(browse_result['url']).netloc,
                'entities': browse_result.get('entities', {}),
                'meta': browse_result.get('meta', {}),
                'source': 'web_scrape'
            })
    
    return {
        'dork_name': dork_name,
        'query': query,
        'total_results': total_results,
        'pages_fetched': pages_fetched,
        'results': all_results[:max_results]
    }

# ==================== Main Deep Search ====================
async def deep_search(
    target: str,
    target_type: str = 'person',
    max_results_per_dork: int = 50,
    enable_dedup: bool = True,
    enable_ranking: bool = True
) -> Dict[str, Any]:
    """
    Advanced OSINT deep search with comprehensive features.
    
    Args:
        target: The search target (person name, email, phone)
        target_type: Type of target ('person', 'email', 'phone')
        max_results_per_dork: Maximum results per dork query
        enable_dedup: Enable result deduplication
        enable_ranking: Enable relevance scoring and ranking
    
    Returns:
        Comprehensive search results with metadata
    """
    # Validate target type
    valid_types = ['person', 'email', 'phone']
    if target_type not in valid_types:
        raise ValueError(f"Invalid target_type '{target_type}'. Must be one of: {valid_types}")
    
    start_time = time.time()
    
    # Validate environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    cx_id = os.getenv("GOOGLE_CX_ID")
    if not api_key or not cx_id:
        raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CX_ID environment variables")
    
    logger.info(f"Starting deep search: target='{target}', type='{target_type}'")
    
    # Generate dorks
    dorks = DorkGenerator.generate_dorks(target, target_type)
    logger.info(f"Generated {len(dorks)} dork queries")
    
    # Execute all dorks concurrently
    async with aiohttp.ClientSession() as session:
        tasks = [
            execute_single_dork(
                session, api_key, cx_id, target, dork_name, query, max_results_per_dork
            )
            for dork_name, query in dorks.items()
        ]
        
        dork_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    processed_results = {}
    all_results = []
    
    for result in dork_results:
        if isinstance(result, Exception):
            logger.error(f"Dork execution exception: {result}")
            continue
        
        dork_name = result['dork_name']
        processed_results[dork_name] = {
            'query': result['query'],
            'total_results': result['total_results'],
            'pages_fetched': result['pages_fetched'],
            'results_count': len(result['results'])
        }
        all_results.extend(result['results'])
    
    # Deduplication
    if enable_dedup and config.enable_deduplication:
        deduplicator = ResultDeduplicator()
        all_results = deduplicator.deduplicate(all_results)
    
    # Ranking
    if enable_ranking:
        all_results = ResultScorer.rank_results(all_results, target)
    
    # Aggregate entities
    aggregated_entities = {
        'emails': set(),
        'phones': set(),
        'urls': set(),
        'social_handles': defaultdict(set),
        'dates': set()
    }
    
    for result in all_results:
        entities = result.get('entities', {})
        aggregated_entities['emails'].update(entities.get('emails', []))
        aggregated_entities['phones'].update(entities.get('phones', []))
        aggregated_entities['urls'].update(entities.get('urls', []))
        for platform, handles in entities.get('social_handles', {}).items():
            aggregated_entities['social_handles'][platform].update(handles)
        aggregated_entities['dates'].update(entities.get('dates', []))
    
    # Convert sets to lists for JSON serialization
    aggregated_entities = {
        'emails': sorted(list(aggregated_entities['emails'])),
        'phones': sorted(list(aggregated_entities['phones'])),
        'urls': sorted(list(aggregated_entities['urls']))[:50],  # Limit URLs
        'social_handles': {k: sorted(list(v)) for k, v in aggregated_entities['social_handles'].items()},
        'dates': sorted(list(aggregated_entities['dates']))
    }
    
    execution_time = time.time() - start_time
    
    return {
        'metadata': {
            'target': target,
            'target_type': target_type,
            'timestamp': datetime.now().isoformat(),
            'execution_time': round(execution_time, 2),
            'total_results': len(all_results),
            'dorks_executed': len(dorks),
            'quota_used': quota_manager.used,
            'quota_remaining': quota_manager.get_remaining()
        },
        'dork_summary': processed_results,
        'aggregated_entities': aggregated_entities,
        'top_results': all_results[:50],  # Return top 50 results
        'all_results': all_results  # Full results list
    }

# ==================== Export Functions ====================
def export_to_json(results: Dict[str, Any], filename: str = None) -> str:
    """Export results to JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"deep_search_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Results exported to {filename}")
    return filename

def results_to_json_string(results: Dict[str, Any]) -> str:
    """Convert results to JSON string."""
    return json.dumps(results, indent=2, ensure_ascii=False)