import os
from pathlib import Path

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# Project structure
structure = {
    'README.md': '''# Web Scraper Project

A Python-based web scraping project that demonstrates various web scraping techniques and best practices.

## Features

- Web scraping using BeautifulSoup4
- Data extraction and processing
- Error handling and rate limiting
- Data storage options

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Patrick-Mebust/Webscrapper.git
cd Webscrapper
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

[Usage instructions will be added as the project develops]

## Project Structure

```
webscraper/
├── src/                    # Source code
│   ├── scrapers/          # Individual scraper modules
│   ├── utils/             # Utility functions
│   └── main.py            # Main entry point
├── data/                  # Data storage
├── tests/                 # Test files
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
''',
    
    'requirements.txt': '''beautifulsoup4==4.12.2
requests==2.31.0
lxml==4.9.3
pandas==2.1.4
python-dotenv==1.0.0
aiohttp==3.9.1
fake-useragent==1.4.0
tqdm==4.66.1
pytest==7.4.3
black==23.11.0
flake8==6.1.0
''',
    
    'src/scrapers/example_scraper.py': '''import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExampleScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Generate random headers for each request."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make a request with error handling and rate limiting."""
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            time.sleep(1)  # Basic rate limiting
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape a single page and extract data."""
        response = self._make_request(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        results = []
        
        # Example: Extract all links from the page
        for link in soup.find_all('a', href=True):
            results.append({
                'text': link.text.strip(),
                'url': link['href'],
                'source_url': url
            })
        
        return results
    
    def scrape_site(self, start_url: str, max_pages: int = 5) -> List[Dict]:
        """Scrape multiple pages from a site."""
        all_results = []
        current_url = start_url
        pages_scraped = 0
        
        while current_url and pages_scraped < max_pages:
            logger.info(f"Scraping page {pages_scraped + 1}: {current_url}")
            page_results = self.scrape_page(current_url)
            all_results.extend(page_results)
            
            # Example: Find next page link (customize based on site structure)
            soup = BeautifulSoup(self._make_request(current_url).text, 'lxml')
            next_link = soup.find('a', text='Next')
            current_url = next_link['href'] if next_link else None
            
            pages_scraped += 1
        
        return all_results

if __name__ == "__main__":
    # Example usage
    scraper = ExampleScraper("https://example.com")
    results = scraper.scrape_site("https://example.com")
    print(f"Scraped {len(results)} items")
''',
    
    'src/utils/helpers.py': '''import json
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime

def save_to_json(data: List[Dict], filename: str) -> None:
    """Save scraped data to a JSON file."""
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {filepath}")

def save_to_csv(data: List[Dict], filename: str) -> None:
    """Save scraped data to a CSV file."""
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding='utf-8')
    
    print(f"Data saved to {filepath}")

def clean_text(text: str) -> str:
    """Clean and normalize text data."""
    if not isinstance(text, str):
        return ""
    return text.strip().replace('\\n', ' ').replace('\\r', '').replace('\\t', ' ')

def validate_url(url: str) -> bool:
    """Validate URL format."""
    if not isinstance(url, str):
        return False
    return url.startswith(('http://', 'https://'))
''',
    
    'src/main.py': '''from scrapers.example_scraper import ExampleScraper
from utils.helpers import save_to_json, save_to_csv
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Web Scraper Tool')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--max-pages', type=int, default=5, help='Maximum number of pages to scrape')
    parser.add_argument('--output-format', choices=['json', 'csv'], default='json', help='Output format')
    args = parser.parse_args()

    try:
        # Initialize scraper
        scraper = ExampleScraper(args.url)
        
        # Scrape the site
        logger.info(f"Starting to scrape {args.url}")
        results = scraper.scrape_site(args.url, args.max_pages)
        
        # Save results
        filename = "scraped_data"
        if args.output_format == 'json':
            save_to_json(results, filename)
        else:
            save_to_csv(results, filename)
            
        logger.info(f"Successfully scraped {len(results)} items")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
''',
    
    '.gitignore': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
data/
.env
*.log

# OS
.DS_Store
Thumbs.db
'''
}

# Create all files
for path, content in structure.items():
    create_file(path, content)

print("All files created successfully!") 