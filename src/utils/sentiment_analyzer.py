import logging
from typing import Dict, List
from textblob import TextBlob
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def analyze_job_description(self, description: str) -> Dict:
        """
        Analyze the sentiment of a job description using multiple methods.
        
        Args:
            description (str): The job description text to analyze
            
        Returns:
            Dict: Dictionary containing sentiment scores from different methods
        """
        try:
            # TextBlob analysis
            blob = TextBlob(description)
            textblob_sentiment = blob.sentiment.polarity
            
            # NLTK VADER analysis
            vader_scores = self.sia.polarity_scores(description)
            
            # spaCy analysis
            doc = nlp(description)
            spacy_sentiment = sum([token.sentiment for token in doc]) / len(doc) if len(doc) > 0 else 0
            
            return {
                'textblob_score': textblob_sentiment,
                'vader_scores': vader_scores,
                'spacy_score': spacy_sentiment,
                'overall_sentiment': self._calculate_overall_sentiment(
                    textblob_sentiment,
                    vader_scores['compound'],
                    spacy_sentiment
                )
            }
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return {
                'textblob_score': 0,
                'vader_scores': {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0},
                'spacy_score': 0,
                'overall_sentiment': 'neutral'
            }

    def analyze_company_sentiment(self, job_postings: List[Dict]) -> Dict:
        """
        Analyze sentiment across all job postings for a company.
        
        Args:
            job_postings (List[Dict]): List of job postings for a company
            
        Returns:
            Dict: Dictionary containing company-level sentiment analysis
        """
        if not job_postings:
            return {
                'average_sentiment': 'neutral',
                'total_postings': 0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0}
            }

        total_sentiment = 0
        sentiment_distribution = {'positive': 0, 'neutral': 0, 'negative': 0}
        
        for posting in job_postings:
            description = posting.get('description', '')
            sentiment = self.analyze_job_description(description)
            
            # Update sentiment distribution
            if sentiment['overall_sentiment'] == 'positive':
                sentiment_distribution['positive'] += 1
            elif sentiment['overall_sentiment'] == 'negative':
                sentiment_distribution['negative'] += 1
            else:
                sentiment_distribution['neutral'] += 1
            
            # Calculate average sentiment
            total_sentiment += (
                sentiment['textblob_score'] +
                sentiment['vader_scores']['compound'] +
                sentiment['spacy_score']
            ) / 3

        average_sentiment = total_sentiment / len(job_postings)
        
        return {
            'average_sentiment': self._get_sentiment_label(average_sentiment),
            'total_postings': len(job_postings),
            'sentiment_distribution': sentiment_distribution
        }

    def _calculate_overall_sentiment(self, textblob_score: float, vader_score: float, spacy_score: float) -> str:
        """
        Calculate overall sentiment based on multiple analysis methods.
        
        Args:
            textblob_score (float): TextBlob sentiment score
            vader_score (float): VADER sentiment score
            spacy_score (float): spaCy sentiment score
            
        Returns:
            str: Overall sentiment label ('positive', 'negative', or 'neutral')
        """
        average_score = (textblob_score + vader_score + spacy_score) / 3
        return self._get_sentiment_label(average_score)

    def _get_sentiment_label(self, score: float) -> str:
        """
        Convert sentiment score to label.
        
        Args:
            score (float): Sentiment score
            
        Returns:
            str: Sentiment label
        """
        if score > 0.1:
            return 'positive'
        elif score < -0.1:
            return 'negative'
        else:
            return 'neutral' 