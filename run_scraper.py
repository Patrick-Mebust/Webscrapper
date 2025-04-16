import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import main
from src.utils.visualization import JobVisualizer

def get_sample_data():
    return [
        {
            'title': 'Senior Python Developer',
            'company': 'TechCorp',
            'location': 'Remote',
            'description': 'Looking for an experienced Python developer with strong skills in Django, Flask, and cloud technologies. Must have excellent problem-solving abilities.',
            'job_type': 'Full-time',
            'salary': '120000',
            'posted_date': '2025-04-16',
            'sentiment_analysis': {
                'textblob_score': 0.8,
                'vader_scores': {'compound': 0.6},
                'spacy_score': 0.7,
                'overall_sentiment': 'positive'
            }
        },
        {
            'title': 'Python Backend Engineer',
            'company': 'StartupCo',
            'location': 'San Francisco',
            'description': 'Join our fast-paced startup! We need a Python expert who can help scale our infrastructure.',
            'job_type': 'Full-time',
            'salary': '140000',
            'posted_date': '2025-04-15',
            'sentiment_analysis': {
                'textblob_score': 0.6,
                'vader_scores': {'compound': 0.5},
                'spacy_score': 0.6,
                'overall_sentiment': 'positive'
            }
        },
        {
            'title': 'Python Data Scientist',
            'company': 'DataCorp',
            'location': 'Remote',
            'description': 'Looking for a data scientist with strong Python skills. Experience with machine learning required.',
            'job_type': 'Contract',
            'salary': '100000',
            'posted_date': '2025-04-14',
            'sentiment_analysis': {
                'textblob_score': 0.7,
                'vader_scores': {'compound': 0.4},
                'spacy_score': 0.5,
                'overall_sentiment': 'positive'
            }
        }
    ]

if __name__ == "__main__":
    # Use sample data instead of scraping
    jobs = get_sample_data()
    
    # Generate visualizations
    visualizer = JobVisualizer()
    visualizer.generate_all_visualizations(jobs)
    
    # Save the data
    from src.utils.helpers import save_to_json
    save_to_json(jobs, f"data/sample_jobs_{os.path.basename(__file__)}_{os.getpid()}.json") 