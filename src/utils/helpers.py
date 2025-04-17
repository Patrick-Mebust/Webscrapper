import json
<<<<<<< HEAD
import pandas as pd
from typing import List, Dict
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def save_to_json(data: List[Dict], filename: str) -> None:
    """Save data to a JSON file."""
    try:
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Data saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving JSON file: {str(e)}")
        raise

def save_to_csv(data: List[Dict], filename: str) -> None:
    """Save data to a CSV file."""
    try:
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"Data saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving CSV file: {str(e)}")
        raise
=======
import csv
import os
from datetime import datetime
from typing import List, Dict
import pandas as pd
import re
>>>>>>> 8ea1b89381d322c3402bc9fb04a78c0131bbf2e5

def clean_text(text: str) -> str:
    """Clean and normalize text data."""
    if not isinstance(text, str):
<<<<<<< HEAD
        return ""
    return " ".join(text.split())

def validate_url(url: str) -> bool:
    """Validate URL format."""
    return url.startswith(('http://', 'https://')) 
=======
        return str(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s.,$]', '', text)
    return text.strip()

def save_to_json(data: List[Dict], filename: str) -> str:
    """Save data to a JSON file with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename}_{timestamp}.json"
    
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filepath

def save_to_csv(data: List[Dict], filename: str) -> str:
    """Save data to a CSV file with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename}_{timestamp}.csv"
    
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding='utf-8')
    
    return filepath

def validate_url(url: str) -> bool:
    """Validate URL format."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url)) 
>>>>>>> 8ea1b89381d322c3402bc9fb04a78c0131bbf2e5
