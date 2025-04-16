import logging
import argparse
from pathlib import Path
from src.scrapers.job_scraper import IndeedScraper
from src.utils.visualization import JobVisualizer
from src.utils.sentiment_analyzer import SentimentAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_output_directory(output_dir: str = "output/sentiment_analysis"):
    """Create output directory for visualizations."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

def analyze_job_postings(scraper, max_pages: int = 2):
    """Scrape and analyze job postings."""
    logger.info("Scraping job postings...")
    job_postings = scraper.scrape_jobs(max_pages=max_pages)
    
    if not job_postings:
        logger.warning("No job postings found")
        return None
    
    return job_postings

def generate_sentiment_visualizations(visualizer, job_postings, output_dir: Path):
    """Generate various sentiment analysis visualizations."""
    logger.info("\nGenerating sentiment visualizations...")
    
    # 1. Overall sentiment distribution
    visualizer.plot_sentiment_distribution(
        job_postings,
        save_path=str(output_dir / "sentiment_distribution.png")
    )
    
    # 2. Sentiment word clouds
    for sentiment in ['positive', 'negative', 'neutral']:
        visualizer.plot_sentiment_wordcloud(
            job_postings,
            sentiment=sentiment,
            save_path=str(output_dir / f"wordcloud_{sentiment}.png")
        )
    
    # 3. Sentiment by company
    companies = set(job['company'] for job in job_postings)
    for company in companies:
        company_jobs = [job for job in job_postings if job['company'] == company]
        company_analysis = sentiment_analyzer.analyze_company_sentiment(company_jobs)
        visualizer.plot_company_sentiment(
            company_analysis,
            save_path=str(output_dir / f"company_sentiment_{company}.png")
        )
    
    # 4. Sentiment score distribution
    visualizer.plot_sentiment_scores(
        job_postings,
        save_path=str(output_dir / "sentiment_scores.png")
    )

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Job Sentiment Analysis Tool')
    parser.add_argument('--max-pages', type=int, default=2,
                       help='Maximum number of pages to scrape')
    parser.add_argument('--output-dir', type=str, default="output/sentiment_analysis",
                       help='Output directory for visualizations')
    args = parser.parse_args()

    try:
        # Setup
        output_dir = setup_output_directory(args.output_dir)
        scraper = IndeedScraper("https://www.indeed.com")
        visualizer = JobVisualizer()
        sentiment_analyzer = SentimentAnalyzer()

        # Analyze job postings
        job_postings = analyze_job_postings(scraper, args.max_pages)
        if not job_postings:
            return

        # Generate visualizations
        generate_sentiment_visualizations(visualizer, job_postings, output_dir)

        # Print summary
        logger.info("\nAnalysis Summary:")
        logger.info(f"Total jobs analyzed: {len(job_postings)}")
        companies = set(job['company'] for job in job_postings)
        logger.info(f"Companies analyzed: {len(companies)}")
        logger.info(f"Visualizations saved to: {output_dir}")

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main() 