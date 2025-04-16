import json
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

def clean_text(text: str) -> str:
    """Clean and normalize text data."""
    if not isinstance(text, str):
        return ""
    return " ".join(text.split())

def validate_url(url: str) -> bool:
    """Validate URL format."""
    return url.startswith(('http://', 'https://')) 