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