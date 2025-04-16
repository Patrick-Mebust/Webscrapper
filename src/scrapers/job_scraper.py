import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def _make_request(self, url: str) -> BeautifulSoup:
        try:
            response = self.session.get(url, headers=self._get_headers())
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            raise

class JobScraper:
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
            time.sleep(2)  # More conservative rate limiting for job sites
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def _extract_job_details(self, soup: BeautifulSoup, job_url: str) -> Dict:
        """Extract job details from a job listing page."""
        # This is a template method that should be overridden for specific job sites
        return {
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'posted_date': '',
            'job_type': '',
            'salary': '',
            'url': job_url,
            'scraped_date': datetime.now().isoformat()
        }
    
    def _extract_job_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract job listings from a search results page."""
        # This is a template method that should be overridden for specific job sites
        return []
    
    def _get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Find the URL for the next page of results."""
        # This is a template method that should be overridden for specific job sites
        return None
    
    def scrape_job_listings(self, start_url: str, max_pages: int = 5) -> List[Dict]:
        """Scrape job listings from multiple pages."""
        all_jobs = []
        current_url = start_url
        pages_scraped = 0
        
        while current_url and pages_scraped < max_pages:
            logger.info(f"Scraping page {pages_scraped + 1}: {current_url}")
            response = self._make_request(current_url)
            if not response:
                break
            
            soup = BeautifulSoup(response.text, 'lxml')
            jobs = self._extract_job_listings(soup)
            
            # Scrape individual job details
            for job in jobs:
                job_url = job.get('url')
                if job_url:
                    job_details = self.scrape_job_details(job_url)
                    if job_details:
                        job.update(job_details)
            
            all_jobs.extend(jobs)
            current_url = self._get_next_page_url(soup)
            pages_scraped += 1
        
        return all_jobs
    
    def scrape_job_details(self, job_url: str) -> Optional[Dict]:
        """Scrape detailed information from a single job listing."""
        response = self._make_request(job_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        return self._extract_job_details(soup, job_url)

class IndeedScraper(JobScraper):
    def _extract_job_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract job listings from Indeed search results."""
        jobs = []
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        for card in job_cards:
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')
            
            if title_elem and title_elem.find('a'):
                job_url = urljoin(self.base_url, title_elem.find('a')['href'])
                jobs.append({
                    'title': title_elem.text.strip(),
                    'company': company_elem.text.strip() if company_elem else '',
                    'location': location_elem.text.strip() if location_elem else '',
                    'url': job_url
                })
        
        return jobs
    
    def _extract_job_details(self, soup: BeautifulSoup, job_url: str) -> Dict:
        """Extract job details from an Indeed job listing."""
        job_details = {
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'posted_date': '',
            'job_type': '',
            'salary': '',
            'url': job_url,
            'scraped_date': datetime.now().isoformat()
        }
        
        # Extract job title
        title_elem = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
        if title_elem:
            job_details['title'] = title_elem.text.strip()
        
        # Extract company name
        company_elem = soup.find('div', class_='jobsearch-CompanyInfoContainer')
        if company_elem:
            job_details['company'] = company_elem.text.strip()
        
        # Extract location
        location_elem = soup.find('div', class_='jobsearch-JobInfoHeader-subtitle')
        if location_elem:
            job_details['location'] = location_elem.text.strip()
        
        # Extract job description
        desc_elem = soup.find('div', id='jobDescriptionText')
        if desc_elem:
            job_details['description'] = desc_elem.text.strip()
        
        # Extract salary
        salary_elem = soup.find('div', class_='jobsearch-JobMetadataHeader-item')
        if salary_elem and 'salary' in salary_elem.text.lower():
            job_details['salary'] = salary_elem.text.strip()
        
        return job_details
    
    def _get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Find the URL for the next page of Indeed results."""
        next_link = soup.find('a', {'aria-label': 'Next Page'})
        if next_link:
            return urljoin(self.base_url, next_link['href'])
        return None

class LinkedInScraper(JobScraper):
    def _extract_job_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract job listings from LinkedIn search results."""
        jobs = []
        job_cards = soup.find_all('div', class_='base-card')
        
        for card in job_cards:
            title_elem = card.find('h3', class_='base-search-card__title')
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            location_elem = card.find('span', class_='job-search-card__location')
            
            if title_elem and title_elem.find('a'):
                job_url = title_elem.find('a')['href']
                jobs.append({
                    'title': title_elem.text.strip(),
                    'company': company_elem.text.strip() if company_elem else '',
                    'location': location_elem.text.strip() if location_elem else '',
                    'url': job_url
                })
        
        return jobs
    
    def _extract_job_details(self, soup: BeautifulSoup, job_url: str) -> Dict:
        """Extract job details from a LinkedIn job listing."""
        job_details = {
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'posted_date': '',
            'job_type': '',
            'salary': '',
            'url': job_url,
            'scraped_date': datetime.now().isoformat()
        }
        
        # Extract job title
        title_elem = soup.find('h1', class_='top-card-layout__title')
        if title_elem:
            job_details['title'] = title_elem.text.strip()
        
        # Extract company name
        company_elem = soup.find('a', class_='topcard__org-name-link')
        if company_elem:
            job_details['company'] = company_elem.text.strip()
        
        # Extract location
        location_elem = soup.find('span', class_='topcard__flavor--bullet')
        if location_elem:
            job_details['location'] = location_elem.text.strip()
        
        # Extract job description
        desc_elem = soup.find('div', class_='show-more-less-html__markup')
        if desc_elem:
            job_details['description'] = desc_elem.text.strip()
        
        # Extract job type and posted date
        metadata = soup.find_all('span', class_='description__job-criteria-text')
        if len(metadata) >= 2:
            job_details['job_type'] = metadata[0].text.strip()
            job_details['posted_date'] = metadata[1].text.strip()
        
        return job_details
    
    def _get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Find the URL for the next page of LinkedIn results."""
        next_link = soup.find('button', {'aria-label': 'Next'})
        if next_link:
            return urljoin(self.base_url, next_link['href'])
        return None

if __name__ == "__main__":
    # Example usage
    indeed_scraper = IndeedScraper("https://www.indeed.com")
    linkedin_scraper = LinkedInScraper("https://www.linkedin.com")
    
    # Scrape Indeed jobs
    indeed_jobs = indeed_scraper.scrape_job_listings(
        "https://www.indeed.com/jobs?q=python&l=Remote",
        max_pages=2
    )
    print(f"Scraped {len(indeed_jobs)} jobs from Indeed")
    
    # Scrape LinkedIn jobs
    linkedin_jobs = linkedin_scraper.scrape_job_listings(
        "https://www.linkedin.com/jobs/search/?keywords=python&location=Remote",
        max_pages=2
    )
    print(f"Scraped {len(linkedin_jobs)} jobs from LinkedIn") 