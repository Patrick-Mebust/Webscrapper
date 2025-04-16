import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExampleScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Generate random headers for each request."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make a request with error handling and rate limiting."""
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            time.sleep(1)  # Basic rate limiting
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape a single page and extract data."""
        response = self._make_request(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        results = []
        
        # Example: Extract all links from the page
        for link in soup.find_all('a', href=True):
            results.append({
                'text': link.text.strip(),
                'url': link['href'],
                'source_url': url
            })
        
        return results
    
    def scrape_site(self, start_url: str, max_pages: int = 5) -> List[Dict]:
        """Scrape multiple pages from a site."""
        all_results = []
        current_url = start_url
        pages_scraped = 0
        
        while current_url and pages_scraped < max_pages:
            logger.info(f"Scraping page {pages_scraped + 1}: {current_url}")
            page_results = self.scrape_page(current_url)
            all_results.extend(page_results)
            
            # Example: Find next page link (customize based on site structure)
            soup = BeautifulSoup(self._make_request(current_url).text, 'lxml')
            next_link = soup.find('a', text='Next')
            current_url = next_link['href'] if next_link else None
            
            pages_scraped += 1
        
        return all_results

if __name__ == "__main__":
    # Example usage
    scraper = ExampleScraper("https://example.com")
    results = scraper.scrape_site("https://example.com")
    print(f"Scraped {len(results)} items") 