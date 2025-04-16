import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
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
    
    def _save_plot(self, fig, filename: str) -> None:
        """Save a matplotlib figure to a file."""
        filepath = self.output_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close(fig)
        logger.info(f"Saved visualization to {filepath}")
    
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