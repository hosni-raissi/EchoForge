

import hashlib
import logging
from typing import List, Dict, Any, Set

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResultDeduplicator:
    def __init__(self):
        self.seen_hashes: Set[str] = set()
        self.seen_urls: Set[str] = set()
    
    def _hash_content(self, content: str) -> str:
        return hashlib.md5(content.lower().strip().encode()).hexdigest()
    
    def is_duplicate(self, result: Dict[str, Any]) -> bool:
        url = result.get('link', '')
        snippet = result.get('snippet', '')
        
        # Check URL
        if url in self.seen_urls:
            return True
        
        # Check content hash
        content_hash = self._hash_content(snippet)
        if content_hash in self.seen_hashes:
            return True
        
        # Add to seen
        self.seen_urls.add(url)
        self.seen_hashes.add(content_hash)
        return False
    
    def deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique_results = []
        for result in results:
            if not self.is_duplicate(result):
                unique_results.append(result)
        logger.info(f"Deduplicated: {len(results)} -> {len(unique_results)}")
        return unique_results

