import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobNotifier:
    def __init__(self, config_path: str = "config/notifications.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.last_notified_jobs = self._load_last_notified()
    
    def _load_config(self) -> Dict:
        """Load notification configuration from JSON file."""
        if not self.config_path.exists():
            return {
                "email": {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "from_email": "",
                    "to_email": ""
                },
                "keywords": [],
                "locations": [],
                "companies": []
            }
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def _load_last_notified(self) -> Dict:
        """Load the last notified jobs from file."""
        last_notified_path = Path("data/last_notified.json")
        if not last_notified_path.exists():
            return {}
        
        with open(last_notified_path, 'r') as f:
            return json.load(f)
    
    def _save_last_notified(self) -> None:
        """Save the last notified jobs to file."""
        last_notified_path = Path("data/last_notified.json")
        last_notified_path.parent.mkdir(exist_ok=True)
        
        with open(last_notified_path, 'w') as f:
            json.dump(self.last_notified_jobs, f, indent=2)
    
    def _matches_criteria(self, job: Dict) -> bool:
        """Check if a job matches the notification criteria."""
        # Check keywords in title and description
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        for keyword in self.config.get('keywords', []):
            if keyword.lower() in title or keyword.lower() in description:
                return True
        
        # Check location
        location = job.get('location', '').lower()
        for loc in self.config.get('locations', []):
            if loc.lower() in location:
                return True
        
        # Check company
        company = job.get('company', '').lower()
        for comp in self.config.get('companies', []):
            if comp.lower() in company:
                return True
        
        return False
    
    def _send_email(self, subject: str, body: str) -> None:
        """Send an email notification."""
        if not self.config['email']['enabled']:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['from_email']
            msg['To'] = self.config['email']['to_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(
                self.config['email']['smtp_server'],
                self.config['email']['smtp_port']
            ) as server:
                server.starttls()
                server.login(
                    self.config['email']['username'],
                    self.config['email']['password']
                )
                server.send_message(msg)
            
            logger.info("Email notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
    
    def check_new_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Check for new jobs that match the criteria and send notifications."""
        new_jobs = []
        
        for job in jobs:
            job_id = job.get('url', '')  # Use URL as unique identifier
            
            # Skip if we've already notified about this job
            if job_id in self.last_notified_jobs:
                continue
            
            # Check if job matches criteria
            if self._matches_criteria(job):
                new_jobs.append(job)
                self.last_notified_jobs[job_id] = datetime.now().isoformat()
        
        if new_jobs:
            # Send email notification
            subject = f"New Job Matches Found: {len(new_jobs)}"
            body = "New job matches found:\n\n"
            
            for job in new_jobs:
                body += f"Title: {job.get('title', '')}\n"
                body += f"Company: {job.get('company', '')}\n"
                body += f"Location: {job.get('location', '')}\n"
                body += f"URL: {job.get('url', '')}\n\n"
            
            self._send_email(subject, body)
            
            # Save updated last notified jobs
            self._save_last_notified()
        
        return new_jobs

if __name__ == "__main__":
    # Example usage
    notifier = JobNotifier()
    
    # Example jobs
    jobs = [
        {
            'title': 'Senior Python Developer',
            'company': 'Tech Corp',
            'location': 'Remote',
            'description': 'Looking for a senior Python developer with Django experience',
            'url': 'https://example.com/job/1'
        },
        {
            'title': 'Java Developer',
            'company': 'Other Corp',
            'location': 'New York',
            'description': 'Java developer needed',
            'url': 'https://example.com/job/2'
        }
    ]
    
    # Check for new jobs and send notifications
    new_jobs = notifier.check_new_jobs(jobs)
    print(f"Found {len(new_jobs)} new matching jobs") 