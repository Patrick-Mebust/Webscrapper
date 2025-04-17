<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin
from datetime import datetime
from src.utils.sentiment_analyzer import SentimentAnalyzer
from src.utils.helpers import clean_text
import random

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
        self.sentiment_analyzer = SentimentAnalyzer()
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for HTTP requests."""
        ua = UserAgent()
        return {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
        }
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make an HTTP request with retries and delays."""
=======
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
>>>>>>> 8ea1b89381d322c3402bc9fb04a78c0131bbf2e5
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
<<<<<<< HEAD
                headers = self._get_headers()
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    time.sleep(random.uniform(2, 5))  # Random delay between requests
                    return response
                elif response.status_code == 403:
                    logger.warning(f"Rate limited on attempt {attempt + 1}, waiting {retry_delay} seconds")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Error {response.status_code} for URL: {url}")
                    return None
                
            except requests.RequestException as e:
                logger.error(f"Request failed on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return None
        
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

    def scrape_jobs(self, max_pages: int = 5) -> List[Dict]:
        """
        Scrape job postings from the website.
        
        Args:
            max_pages (int): Maximum number of pages to scrape
            
        Returns:
            List[Dict]: List of job postings with sentiment analysis
        """
        job_postings = []
        job_listings = self.scrape_job_listings(self.base_url)
        
        for job in job_listings:
            job_data = {
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', ''),
                'description': job.get('description', ''),
                'url': job.get('url', ''),
                'sentiment_analysis': self.sentiment_analyzer.analyze_job_description(
                    job.get('description', '')
                )
            }
            job_postings.append(job_data)
        
        return job_postings

    def get_company_sentiment_analysis(self, company_name: str) -> Dict:
        """
        Get sentiment analysis for all job postings from a specific company.
        
        Args:
            company_name (str): Name of the company to analyze
            
        Returns:
            Dict: Company-level sentiment analysis
        """
        company_jobs = [job for job in self.scrape_jobs() if job['company'].lower() == company_name.lower()]
        return self.sentiment_analyzer.analyze_company_sentiment(company_jobs)

class IndeedScraper(JobScraper):
    def __init__(self):
        super().__init__("https://www.indeed.com")

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
    def __init__(self):
        super().__init__("https://www.linkedin.com")

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
    indeed_scraper = IndeedScraper()
    linkedin_scraper = LinkedInScraper()
    
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
=======
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
>>>>>>> 8ea1b89381d322c3402bc9fb04a78c0131bbf2e5
