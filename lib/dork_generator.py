

from typing import Dict


class DorkGenerator:
    @staticmethod
    def generate_person_dorks(target: str) -> Dict[str, str]:
        return {
            'linkedin_profiles': f'"{target}" site:linkedin.com/in',
            'twitter_x': f'"{target}" (site:twitter.com OR site:x.com)',
            'facebook': f'"{target}" site:facebook.com',
            'instagram': f'"{target}" site:instagram.com',
            'github': f'"{target}" site:github.com',
            'resumes_cv': f'"{target}" (filetype:pdf OR filetype:docx) ("resume" OR "CV" OR "curriculum vitae")',
            'publications': f'"{target}" (filetype:pdf OR site:scholar.google.com OR site:researchgate.net)',
            'news_mentions': f'"{target}" (site:nytimes.com OR site:washingtonpost.com OR site:bbc.com OR site:reuters.com)',
            'blog_posts': f'"{target}" (site:medium.com OR site:wordpress.com OR site:blogger.com)',
            'presentations': f'"{target}" (filetype:pptx OR filetype:ppt OR site:slideshare.net)',
            'videos': f'"{target}" (site:youtube.com OR site:vimeo.com)',
            'professional_orgs': f'"{target}" ("member" OR "director" OR "CEO" OR "founder")',
            'contact_info': f'"{target}" (email OR phone OR contact)',
            'simple': f'"{target}"'
        }
    
    @staticmethod
    def generate_email_dorks(target: str) -> Dict[str, str]:
        return {
            'breach_check': f'"{target}" (site:haveibeenpwned.com OR "data breach" OR "leaked")',
            'social_mentions': f'"{target}" (site:reddit.com OR site:twitter.com OR site:x.com)',
            'forum_posts': f'"{target}" (site:stackoverflow.com OR site:stackexchange.com)',
            'pastebin_leaks': f'"{target}" (site:pastebin.com OR site:ghostbin.com)',
            'github_commits': f'"{target}" site:github.com',
            'domain_info': f'"{target.split("@")[1]}" (whois OR dns OR "mail server")' if '@' in target else '',
            'business_listings': f'"{target}" ("contact" OR "email")',
            'pgp_keys': f'"{target}" (site:keys.openpgp.org OR "PGP key")',
            'simple': f'"{target}"'
        }
    
    @staticmethod
    def generate_phone_dorks(target: str) -> Dict[str, str]:
        return {
            'reverse_lookup': f'"{target}" ("phone" OR "contact" OR "mobile")',
            'business_listings': f'"{target}" (site:yellowpages.com OR site:whitepages.com)',
            'social_media': f'"{target}" (site:facebook.com OR site:linkedin.com)',
            'simple': f'"{target}"'
        }

    @staticmethod
    def generate_dark_web_dorks(target: str) -> Dict[str, str]:
        return {
            'onion_proxies': f'"{target}" (site:onion.link OR site:onion.ws OR site:tor2web.org OR site:onion.pet OR site:onion.dog)',
            'leaks_dumps': f'"{target}" (site:pastebin.com OR site:ghostbin.com OR site:justpaste.it OR site:rentry.co OR "leaked database" OR "dump" OR "breach")',
            'darknet_markets': f'"{target}" ("darknet" OR "market" OR "silk road" OR "alpha bay" OR "hydra" OR "dream market")',
            'hacking_forums': f'"{target}" (site:raidforums.com OR site:breached.vc OR "hacking forum" OR "carding")',
        }
    
    @staticmethod
    def generate_dorks(target: str, target_type: str, options: Dict[str, bool] = None) -> Dict[str, str]:
        if options is None:
            options = {}

        generators = {
            'person': DorkGenerator.generate_person_dorks,
            'email': DorkGenerator.generate_email_dorks,
            'phone': DorkGenerator.generate_phone_dorks
        }
        
        generator = generators.get(target_type, DorkGenerator.generate_person_dorks)
        dorks = generator(target)

        # Filter social media if disabled
        if not options.get('social_media', True):
            keys_to_remove = ['twitter_x', 'facebook', 'instagram', 'linkedin_profiles', 'social_mentions', 'social_media']
            for k in keys_to_remove:
                dorks.pop(k, None)

        # Add Dark Web dorks if enabled
        if options.get('dark_web', False):
            dorks.update(DorkGenerator.generate_dark_web_dorks(target))
        
        # Filter out empty queries
        return {k: v for k, v in dorks.items() if v}
