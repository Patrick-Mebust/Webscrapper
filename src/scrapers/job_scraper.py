import logging
import time
import random
from typing import List, Dict
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from utils.helpers import clean_text

logger = logging.getLogger(__name__)

class BaseScraper:
    """Base class for job scrapers."""
    
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self._update_headers()
    
    def _update_headers(self):
        """Update headers with a new random user agent."""
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    
    def _get_soup(self, url: str) -> BeautifulSoup:
        """Get BeautifulSoup object from URL with retry mechanism."""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                # Update headers with new user agent for each request
                self._update_headers()
                
                # Add random delay between requests
                time.sleep(random.uniform(2, 5))
                
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                if response.status_code == 200:
                    return BeautifulSoup(response.text, 'html.parser')
                
            except requests.RequestException as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed for URL {url}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise
    
    def _extract_job_data(self, job_element: BeautifulSoup) -> Dict:
        """Extract job data from a job element."""
        raise NotImplementedError("Subclasses must implement _extract_job_data")

class IndeedScraper(BaseScraper):
    """Scraper for Indeed job listings."""
    
    def _extract_job_data(self, job_element: BeautifulSoup) -> Dict:
        try:
            title = job_element.find('h2', class_='jobTitle').text.strip()
            company = job_element.find('span', class_='companyName').text.strip()
            location = job_element.find('div', class_='companyLocation').text.strip()
            salary = job_element.find('div', class_='salary-snippet')
            salary = salary.text.strip() if salary else 'Not specified'
            
            return {
                'title': clean_text(title),
                'company': clean_text(company),
                'location': clean_text(location),
                'salary': clean_text(salary),
                'source': 'Indeed'
            }
        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
            return {}
    
    def scrape_job_listings(self, url: str, max_pages: int = 5) -> List[Dict]:
        """Scrape job listings from Indeed."""
        jobs = []
        for page in range(max_pages):
            try:
                page_url = f"{url}&start={page * 10}"
                soup = self._get_soup(page_url)
                job_elements = soup.find_all('div', class_='job_seen_beacon')
                
                for job_element in job_elements:
                    job_data = self._extract_job_data(job_element)
                    if job_data:
                        jobs.append(job_data)
                
                logger.info(f"Scraped page {page + 1} of {max_pages}")
                time.sleep(random.uniform(1, 3))  # Be nice to the server
                
            except Exception as e:
                logger.error(f"Error scraping page {page + 1}: {str(e)}")
                continue
        
        return jobs

class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn job listings."""
    
    def _extract_job_data(self, job_element: BeautifulSoup) -> Dict:
        try:
            title = job_element.find('h3', class_='base-search-card__title').text.strip()
            company = job_element.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job_element.find('span', class_='job-search-card__location').text.strip()
            
            # Extract job type from title (common patterns)
            job_type = 'Full-time'  # Default
            title_lower = title.lower()
            if any(term in title_lower for term in ['contract', 'contractor']):
                job_type = 'Contract'
            elif 'part-time' in title_lower:
                job_type = 'Part-time'
            elif 'intern' in title_lower:
                job_type = 'Internship'
            elif 'temporary' in title_lower:
                job_type = 'Temporary'
            
            # Try to extract salary information
            salary = 'Not specified'
            salary_elem = job_element.find('span', class_='job-search-card__salary-info')
            if salary_elem:
                salary = salary_elem.text.strip()
            
            return {
                'title': clean_text(title),
                'company': clean_text(company),
                'location': clean_text(location),
                'salary': clean_text(salary),
                'job_type': job_type,
                'source': 'LinkedIn'
            }
        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
            return {}
    
    def scrape_job_listings(self, url: str, max_pages: int = 5) -> List[Dict]:
        """Scrape job listings from LinkedIn."""
        jobs = []
        for page in range(max_pages):
            try:
                page_url = f"{url}&start={page * 25}"
                soup = self._get_soup(page_url)
                job_elements = soup.find_all('div', class_='base-card')
                
                for job_element in job_elements:
                    job_data = self._extract_job_data(job_element)
                    if job_data:
                        jobs.append(job_data)
                
                logger.info(f"Scraped page {page + 1} of {max_pages}")
                time.sleep(random.uniform(1, 3))  # Be nice to the server
                
            except Exception as e:
                logger.error(f"Error scraping page {page + 1}: {str(e)}")
                continue
        
        return jobs 