import json
import csv
import os
from datetime import datetime
from typing import List, Dict
import pandas as pd
import re

def clean_text(text: str) -> str:
    """Clean and normalize text data."""
    if not isinstance(text, str):
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