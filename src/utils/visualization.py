<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobVisualizer:
    def __init__(self, output_dir: str = "data/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def _save_plot(self, fig, filename: str, save_path: str = None) -> None:
        """Save a matplotlib figure to a file."""
        filepath = self.output_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close(fig)
        logger.info(f"Saved visualization to {filepath}")
        if save_path:
            save_path.append(filepath)
    
    def plot_jobs_by_company(self, jobs: List[Dict]) -> None:
        """Create a bar plot of jobs by company."""
        df = pd.DataFrame(jobs)
        company_counts = df['company'].value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=company_counts.values, y=company_counts.index)
        plt.title('Top 10 Companies by Number of Job Postings')
        plt.xlabel('Number of Jobs')
        plt.ylabel('Company')
        
        self._save_plot(plt.gcf(), 'jobs_by_company')
    
    def plot_jobs_by_location(self, jobs: List[Dict]) -> None:
        """Create a bar plot of jobs by location."""
        df = pd.DataFrame(jobs)
        location_counts = df['location'].value_counts().head(10)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=location_counts.values, y=location_counts.index)
        plt.title('Top 10 Locations by Number of Job Postings')
        plt.xlabel('Number of Jobs')
        plt.ylabel('Location')
        
        self._save_plot(plt.gcf(), 'jobs_by_location')
    
    def plot_job_types(self, jobs: List[Dict]) -> None:
        """Create a pie chart of job types."""
        df = pd.DataFrame(jobs)
        job_types = df['job_type'].value_counts()
        
        plt.figure(figsize=(10, 10))
        plt.pie(job_types.values, labels=job_types.index, autopct='%1.1f%%')
        plt.title('Distribution of Job Types')
        
        self._save_plot(plt.gcf(), 'job_types')
    
    def create_word_cloud(self, jobs: List[Dict]) -> None:
        """Create a word cloud from job descriptions."""
        # Combine all job descriptions
        text = ' '.join(job.get('description', '') for job in jobs)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            max_words=200
        ).generate(text)
        
        # Plot word cloud
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Job Descriptions')
        
        self._save_plot(plt.gcf(), 'word_cloud')
    
    def plot_salary_ranges(self, jobs: List[Dict]) -> None:
        """Create a histogram of salary ranges."""
        # Extract salary information (this is a simplified example)
        salaries = []
        for job in jobs:
            salary = job.get('salary', '')
            if salary:
                # Extract numeric value (this is a simplified example)
                try:
                    salary_value = float(''.join(filter(str.isdigit, salary)))
                    salaries.append(salary_value)
                except ValueError:
                    continue
        
        if salaries:
            plt.figure(figsize=(12, 6))
            sns.histplot(salaries, bins=20)
            plt.title('Distribution of Salary Ranges')
            plt.xlabel('Salary')
            plt.ylabel('Count')
            
            self._save_plot(plt.gcf(), 'salary_ranges')
    
    def generate_all_visualizations(self, jobs: List[Dict]) -> None:
        """Generate all visualizations for the job data."""
        logger.info("Generating visualizations...")
        
        try:
            self.plot_jobs_by_company(jobs)
            self.plot_jobs_by_location(jobs)
            self.plot_job_types(jobs)
            self.create_word_cloud(jobs)
            self.plot_salary_ranges(jobs)
            
            logger.info("All visualizations generated successfully")
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")

    def plot_sentiment_distribution(self, job_postings: List[Dict], save_path: str = None) -> None:
        """
        Plot the distribution of sentiment scores across job postings.
        
        Args:
            job_postings (List[Dict]): List of job postings with sentiment analysis
            save_path (str, optional): Path to save the plot
        """
        sentiments = [job['sentiment_analysis']['overall_sentiment'] for job in job_postings]
        sentiment_counts = pd.Series(sentiments).value_counts()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
        plt.title('Distribution of Sentiment in Job Descriptions')
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Job Postings')
        
        self._save_plot(plt, 'sentiment_distribution', save_path)

    def plot_company_sentiment(self, company_analysis: Dict, save_path: str = None) -> None:
        """
        Plot sentiment analysis for a specific company.
        
        Args:
            company_analysis (Dict): Company sentiment analysis results
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(10, 6))
        
        # Plot sentiment distribution
        distribution = company_analysis['sentiment_distribution']
        plt.bar(distribution.keys(), distribution.values())
        
        plt.title(f"Company Job Posting Sentiment Analysis\nOverall: {company_analysis['average_sentiment']}")
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Job Postings')
        
        self._save_plot(plt, 'company_sentiment', save_path)

    def plot_sentiment_wordcloud(self, job_postings: List[Dict], sentiment: str = 'positive', save_path: str = None) -> None:
        """
        Generate a word cloud for job descriptions with a specific sentiment.
        
        Args:
            job_postings (List[Dict]): List of job postings with sentiment analysis
            sentiment (str): Sentiment to filter ('positive', 'negative', or 'neutral')
            save_path (str, optional): Path to save the plot
        """
        # Filter job descriptions by sentiment
        filtered_descriptions = [
            job['description'] for job in job_postings 
            if job['sentiment_analysis']['overall_sentiment'] == sentiment
        ]
        
        if not filtered_descriptions:
            self.logger.warning(f"No job descriptions found with {sentiment} sentiment")
            return
        
        # Generate word cloud
        text = ' '.join(filtered_descriptions)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {sentiment.capitalize()} Job Descriptions')
        
        self._save_plot(plt, f'wordcloud_{sentiment}', save_path)

    def plot_sentiment_scores(self, job_postings: List[Dict], save_path: str = None) -> None:
        """
        Plot the distribution of sentiment scores across all job postings.
        
        Args:
            job_postings (List[Dict]): List of job postings with sentiment analysis
            save_path (str, optional): Path to save the plot
        """
        # Extract sentiment scores
        textblob_scores = [job['sentiment_analysis']['textblob_score'] for job in job_postings]
        vader_scores = [job['sentiment_analysis']['vader_scores']['compound'] for job in job_postings]
        spacy_scores = [job['sentiment_analysis']['spacy_score'] for job in job_postings]
        
        # Create subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Plot TextBlob scores
        sns.histplot(textblob_scores, ax=axes[0], bins=20)
        axes[0].set_title('TextBlob Sentiment Scores')
        axes[0].set_xlabel('Score')
        axes[0].set_ylabel('Count')
        
        # Plot VADER scores
        sns.histplot(vader_scores, ax=axes[1], bins=20)
        axes[1].set_title('VADER Sentiment Scores')
        axes[1].set_xlabel('Score')
        axes[1].set_ylabel('Count')
        
        # Plot spaCy scores
        sns.histplot(spacy_scores, ax=axes[2], bins=20)
        axes[2].set_title('spaCy Sentiment Scores')
        axes[2].set_xlabel('Score')
        axes[2].set_ylabel('Count')
        
        plt.tight_layout()
        self._save_plot(plt, 'sentiment_scores', save_path)

    def plot_sentiment_trends(self, job_postings: List[Dict], save_path: str = None) -> None:
        """
        Plot sentiment trends over time.
        
        Args:
            job_postings (List[Dict]): List of job postings with sentiment analysis
            save_path (str, optional): Path to save the plot
        """
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(job_postings)
        
        # Extract dates and scores
        df['date'] = pd.to_datetime(df['posted_date'])
        df['textblob_score'] = df['sentiment_analysis'].apply(lambda x: x['textblob_score'])
        df['vader_score'] = df['sentiment_analysis'].apply(lambda x: x['vader_scores']['compound'])
        df['spacy_score'] = df['sentiment_analysis'].apply(lambda x: x['spacy_score'])
        
        # Calculate rolling averages
        window = 7  # 7-day rolling average
        df['textblob_rolling'] = df['textblob_score'].rolling(window=window).mean()
        df['vader_rolling'] = df['vader_score'].rolling(window=window).mean()
        df['spacy_rolling'] = df['spacy_score'].rolling(window=window).mean()
        
        # Plot trends
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['textblob_rolling'], label='TextBlob')
        plt.plot(df['date'], df['vader_rolling'], label='VADER')
        plt.plot(df['date'], df['spacy_rolling'], label='spaCy')
        
        plt.title('Sentiment Score Trends Over Time')
        plt.xlabel('Date')
        plt.ylabel('Sentiment Score (7-day rolling average)')
        plt.legend()
        plt.grid(True)
        
        self._save_plot(plt, 'sentiment_trends', save_path)

if __name__ == "__main__":
    # Example usage
    visualizer = JobVisualizer()
    
    # Example jobs
    jobs = [
        {
            'title': 'Senior Python Developer',
            'company': 'Tech Corp',
            'location': 'Remote',
            'description': 'Looking for a senior Python developer with Django experience',
            'job_type': 'Full-time',
            'salary': '$120,000 - $150,000'
        },
        {
            'title': 'Java Developer',
            'company': 'Other Corp',
            'location': 'New York',
            'description': 'Java developer needed',
            'job_type': 'Contract',
            'salary': '$90,000 - $110,000'
        }
    ]
    
    # Generate visualizations
    visualizer.generate_all_visualizations(jobs) 
=======
import logging
import os
from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

logger = logging.getLogger(__name__)

class JobVisualizer:
    """Class for generating visualizations from job data."""
    
    def __init__(self, jobs: List[Dict]):
        """Initialize with job data."""
        self.jobs = jobs
        self.df = pd.DataFrame(jobs)
        self.output_dir = 'data/visualizations'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _save_plot(self, filename: str) -> str:
        """Save the current plot and return the filepath."""
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath)
        plt.close()
        return filepath
    
    def plot_jobs_by_company(self) -> str:
        """Create a bar plot of jobs by company."""
        plt.figure(figsize=(12, 6))
        company_counts = self.df['company'].value_counts().head(10)
        sns.barplot(x=company_counts.values, y=company_counts.index)
        plt.title('Top 10 Companies by Number of Job Listings')
        plt.xlabel('Number of Jobs')
        plt.ylabel('Company')
        filepath = self._save_plot('jobs_by_company.png')
        logger.info(f"Saved company distribution plot to {filepath}")
        return filepath
    
    def plot_jobs_by_location(self) -> str:
        """Create a bar plot of jobs by location."""
        plt.figure(figsize=(12, 6))
        location_counts = self.df['location'].value_counts().head(10)
        sns.barplot(x=location_counts.values, y=location_counts.index)
        plt.title('Top 10 Locations by Number of Job Listings')
        plt.xlabel('Number of Jobs')
        plt.ylabel('Location')
        filepath = self._save_plot('jobs_by_location.png')
        logger.info(f"Saved location distribution plot to {filepath}")
        return filepath
    
    def plot_job_types(self) -> str:
        """Create a pie chart of job types."""
        plt.figure(figsize=(10, 10))
        job_types = self.df['job_type'].value_counts()
        plt.pie(job_types.values, labels=job_types.index, autopct='%1.1f%%')
        plt.title('Distribution of Job Types')
        filepath = self._save_plot('job_types.png')
        logger.info(f"Saved job types plot to {filepath}")
        return filepath
    
    def plot_salary_distribution(self) -> str:
        """Create a histogram of salary ranges."""
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.df, x='salary', bins=20)
        plt.title('Salary Distribution')
        plt.xlabel('Salary Range')
        plt.ylabel('Number of Jobs')
        filepath = self._save_plot('salary_distribution.png')
        logger.info(f"Saved salary distribution plot to {filepath}")
        return filepath
    
    def create_word_cloud(self) -> str:
        """Create a word cloud from job descriptions."""
        plt.figure(figsize=(12, 8))
        text = ' '.join(self.df['description'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Job Descriptions')
        filepath = self._save_plot('job_descriptions_wordcloud.png')
        logger.info(f"Saved word cloud to {filepath}")
        return filepath 
>>>>>>> 8ea1b89381d322c3402bc9fb04a78c0131bbf2e5
