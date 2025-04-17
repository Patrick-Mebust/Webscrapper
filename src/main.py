import argparse
import logging
from typing import List, Dict
from urllib.parse import quote
from datetime import datetime
from src.scrapers.job_scraper import IndeedScraper, LinkedInScraper
from src.utils.helpers import save_to_json, save_to_csv, validate_url
from src.utils.visualization import JobVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_jobs(
    platform: str,
    search_query: str,
    location: str,
    max_pages: int = 5,
    output_format: str = 'json'
) -> List[Dict]:
    """Scrape job listings from specified platform."""
    # URL encode the query parameters
    encoded_query = quote(search_query)
    encoded_location = quote(location)
    
    if platform.lower() == 'indeed':
        scraper = IndeedScraper()
        base_url = f"https://www.indeed.com/jobs?q={encoded_query}&l={encoded_location}"
    elif platform.lower() == 'linkedin':
        scraper = LinkedInScraper()
        base_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&location={encoded_location}"
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    if not validate_url(base_url):
        raise ValueError(f"Invalid URL format: {base_url}")

    logger.info(f"Scraping {platform} for '{search_query}' in {location}")
    jobs = scraper.scrape_job_listings(base_url, max_pages)
    logger.info(f"Found {len(jobs)} jobs")

    return jobs

def main():
    parser = argparse.ArgumentParser(description='Job Scraper')
    parser.add_argument('--platform', choices=['indeed', 'linkedin'], required=True,
                      help='Platform to scrape jobs from')
    parser.add_argument('--query', required=True,
                      help='Search query for jobs')
    parser.add_argument('--location', required=True,
                      help='Location to search for jobs')
    parser.add_argument('--max-pages', type=int, default=5,
                      help='Maximum number of pages to scrape')
    parser.add_argument('--output-format', choices=['json', 'csv'], default='json',
                      help='Output format for the scraped data')
    parser.add_argument('--visualize', action='store_true',
                      help='Generate visualizations of the scraped data')

    args = parser.parse_args()

    try:
        # Scrape jobs
        jobs = scrape_jobs(
            args.platform,
            args.query,
            args.location,
            args.max_pages,
            args.output_format
        )

        # Save data
        filename = f"{args.platform}_{args.query}_{args.location}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if args.output_format == 'json':
            filepath = save_to_json(jobs, filename)
        else:
            filepath = save_to_csv(jobs, filename)
        logger.info(f"Data saved to {filepath}")

        # Generate visualizations if requested
        if args.visualize and jobs:
            visualizer = JobVisualizer()
            visualizer.plot_jobs_by_company(jobs)
            visualizer.plot_jobs_by_location(jobs)
            visualizer.plot_job_types(jobs)
            visualizer.plot_salary_distribution(jobs)
            visualizer.plot_sentiment_trends(jobs)
            logger.info("Visualizations generated successfully")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    main() 