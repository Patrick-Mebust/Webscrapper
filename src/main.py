import argparse
import logging
from scrapers.job_scraper import IndeedScraper, LinkedInScraper
from utils.helpers import save_to_json, save_to_csv
from utils.visualization import JobVisualizer
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_jobs(site: str, query: str, location: str, max_pages: int, output_format: str) -> None:
    """Scrape jobs from the specified site."""
    if site.lower() == 'indeed':
        scraper = IndeedScraper()
        url = f"https://www.indeed.com/jobs?q={query}&l={location}"
    elif site.lower() == 'linkedin':
        scraper = LinkedInScraper()
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}"
    else:
        raise ValueError(f"Unsupported site: {site}")
    
    logger.info(f"Scraping jobs from {site} for query: {query}, location: {location}")
    jobs = scraper.scrape_job_listings(url, max_pages=max_pages)
    
    # Save results
    filename = f"data/jobs_{site}_{query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if output_format.lower() == 'json':
        save_to_json(jobs, f"{filename}.json")
    else:
        save_to_csv(jobs, f"{filename}.csv")
    
    # Generate visualizations
    visualizer = JobVisualizer()
    visualizer.generate_all_visualizations(jobs)

def main():
    parser = argparse.ArgumentParser(description='Job Scraper')
    parser.add_argument('site', choices=['indeed', 'linkedin'], help='Job site to scrape')
    parser.add_argument('query', help='Job search query')
    parser.add_argument('--location', default='Remote', help='Job location')
    parser.add_argument('--max-pages', type=int, default=5, help='Maximum number of pages to scrape')
    parser.add_argument('--output-format', choices=['json', 'csv'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    try:
        scrape_jobs(args.site, args.query, args.location, args.max_pages, args.output_format)
    except Exception as e:
        logger.error(f"Error scraping jobs: {str(e)}")
        raise

if __name__ == "__main__":
    main() 