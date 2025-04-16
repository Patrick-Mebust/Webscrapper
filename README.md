# Job Scraper

A Python-based web scraper for job listings from Indeed and LinkedIn, with data visualization capabilities.

## Features

- Scrape job listings from Indeed and LinkedIn
- Save data in JSON or CSV format
- Generate visualizations:
  - Jobs by company
  - Jobs by location
  - Job types distribution
  - Word cloud of job descriptions
  - Salary ranges distribution
- Error handling and logging
- Configurable search parameters

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job-scraper.git
cd job-scraper
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper with the following command:

```bash
python src/main.py <site> <query> [options]
```

### Arguments

- `site`: Job site to scrape (choices: indeed, linkedin)
- `query`: Job search query

### Options

- `--location`: Job location (default: Remote)
- `--max-pages`: Maximum number of pages to scrape (default: 5)
- `--output-format`: Output format (choices: json, csv, default: json)

### Examples

Scrape Python developer jobs from Indeed:
```bash
python src/main.py indeed "python developer" --location "Remote"
```

Scrape data science jobs from LinkedIn:
```bash
python src/main.py linkedin "data scientist" --max-pages 3 --output-format csv
```

## Project Structure

```
job-scraper/
├── src/
│   ├── scrapers/
│   │   └── job_scraper.py
│   ├── utils/
│   │   ├── helpers.py
│   │   └── visualization.py
│   └── main.py
├── data/
│   ├── jobs/
│   └── visualizations/
├── tests/
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
