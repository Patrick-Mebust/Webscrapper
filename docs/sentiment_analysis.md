# Job Description Sentiment Analysis

This document describes the sentiment analysis features implemented in the job scraper project.

## Overview

The sentiment analysis system analyzes job descriptions to determine their emotional tone (positive, negative, or neutral) using multiple NLP techniques. This helps identify companies with potentially better or worse work environments based on their job postings.

## Features

### 1. Multi-Method Sentiment Analysis

The system uses three different sentiment analysis methods:

- **TextBlob**: Simple and fast sentiment analysis
- **VADER (NLTK)**: Specifically designed for social media text
- **spaCy**: Advanced NLP with custom sentiment analysis

### 2. Company-Level Analysis

- Aggregates sentiment across all job postings from a company
- Calculates average sentiment and distribution
- Identifies patterns in job posting language

### 3. Visualization Tools

- Sentiment distribution plots
- Word clouds for positive/negative/neutral descriptions
- Company-specific sentiment analysis
- Detailed sentiment score distributions

## Usage

### Basic Usage

```python
from src.scrapers.job_scraper import IndeedScraper
from src.utils.sentiment_analyzer import SentimentAnalyzer

# Initialize components
scraper = IndeedScraper("https://www.indeed.com")
sentiment_analyzer = SentimentAnalyzer()

# Scrape and analyze jobs
jobs = scraper.scrape_jobs(max_pages=2)
for job in jobs:
    sentiment = job['sentiment_analysis']
    print(f"Job: {job['title']}")
    print(f"Sentiment: {sentiment['overall_sentiment']}")
```

### Company Analysis

```python
# Get company-specific analysis
company_analysis = scraper.get_company_sentiment_analysis("Example Corp")
print(f"Average Sentiment: {company_analysis['average_sentiment']}")
print(f"Distribution: {company_analysis['sentiment_distribution']}")
```

### Visualizations

```python
from src.utils.visualization import JobVisualizer

visualizer = JobVisualizer()

# Generate various visualizations
visualizer.plot_sentiment_distribution(jobs)
visualizer.plot_sentiment_wordcloud(jobs, sentiment='positive')
visualizer.plot_company_sentiment(company_analysis)
```

## Command Line Interface

The sentiment analysis can be run from the command line:

```bash
python examples/sentiment_analysis_example.py --max-pages 3 --output-dir output/sentiment
```

Options:
- `--max-pages`: Number of pages to scrape (default: 2)
- `--output-dir`: Directory to save visualizations (default: output/sentiment_analysis)

## Output Files

The analysis generates several visualization files:

1. `sentiment_distribution.png`: Distribution of sentiment across all jobs
2. `wordcloud_positive.png`: Word cloud for positive job descriptions
3. `wordcloud_negative.png`: Word cloud for negative job descriptions
4. `wordcloud_neutral.png`: Word cloud for neutral job descriptions
5. `company_sentiment_[company].png`: Company-specific sentiment analysis
6. `sentiment_scores.png`: Distribution of sentiment scores from different methods

## Sentiment Score Interpretation

- **Positive**: Score > 0.1
- **Neutral**: -0.1 ≤ Score ≤ 0.1
- **Negative**: Score < -0.1

The final sentiment is determined by averaging scores from all three methods.

## Best Practices

1. **Sample Size**: Analyze at least 5-10 job postings per company for reliable results
2. **Context**: Consider industry norms when interpreting sentiment
3. **Updates**: Run analysis periodically to track changes in company sentiment
4. **Validation**: Compare results with employee reviews for validation

## Limitations

1. Sentiment analysis may not capture industry-specific terminology
2. Cultural differences in language use may affect results
3. Sarcasm or irony in job descriptions may be misinterpreted
4. Results should be used as one factor in company evaluation

## Future Improvements

1. Industry-specific sentiment lexicons
2. Machine learning-based sentiment classification
3. Integration with employee review data
4. Real-time sentiment tracking
5. Custom sentiment thresholds per industry 