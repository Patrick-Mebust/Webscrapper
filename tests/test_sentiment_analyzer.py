import pytest
from src.utils.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def sentiment_analyzer():
    return SentimentAnalyzer()

def test_analyze_job_description_positive(sentiment_analyzer):
    """Test sentiment analysis with a positive job description."""
    positive_description = """
    We are looking for a talented developer to join our amazing team!
    Our company offers excellent benefits, a supportive work environment,
    and opportunities for growth and development. You'll work with
    cutting-edge technologies and collaborate with brilliant colleagues.
    """
    
    result = sentiment_analyzer.analyze_job_description(positive_description)
    
    assert 'textblob_score' in result
    assert 'vader_scores' in result
    assert 'spacy_score' in result
    assert 'overall_sentiment' in result
    assert result['overall_sentiment'] == 'positive'

def test_analyze_job_description_negative(sentiment_analyzer):
    """Test sentiment analysis with a negative job description."""
    negative_description = """
    This position requires working long hours under tight deadlines.
    The work environment is fast-paced and demanding. You must be
    available for overtime and weekend work. High stress tolerance
    is essential for this challenging role.
    """
    
    result = sentiment_analyzer.analyze_job_description(negative_description)
    assert result['overall_sentiment'] == 'negative'

def test_analyze_job_description_neutral(sentiment_analyzer):
    """Test sentiment analysis with a neutral job description."""
    neutral_description = """
    The position requires a bachelor's degree in computer science.
    Experience with Python and SQL is required. The role is full-time
    and located in our downtown office. Standard benefits apply.
    """
    
    result = sentiment_analyzer.analyze_job_description(neutral_description)
    assert result['overall_sentiment'] == 'neutral'

def test_analyze_company_sentiment(sentiment_analyzer):
    """Test company-level sentiment analysis."""
    job_postings = [
        {
            'description': 'Join our amazing team with great benefits!',
            'company': 'Tech Corp'
        },
        {
            'description': 'Fast-paced environment with growth opportunities.',
            'company': 'Tech Corp'
        },
        {
            'description': 'Standard position with regular hours.',
            'company': 'Tech Corp'
        }
    ]
    
    result = sentiment_analyzer.analyze_company_sentiment(job_postings)
    
    assert 'average_sentiment' in result
    assert 'total_postings' in result
    assert 'sentiment_distribution' in result
    assert result['total_postings'] == 3

def test_empty_job_description(sentiment_analyzer):
    """Test sentiment analysis with an empty job description."""
    result = sentiment_analyzer.analyze_job_description('')
    assert result['overall_sentiment'] == 'neutral'

def test_invalid_input(sentiment_analyzer):
    """Test sentiment analysis with invalid input."""
    result = sentiment_analyzer.analyze_job_description(None)
    assert result['overall_sentiment'] == 'neutral'

def test_company_sentiment_empty_list(sentiment_analyzer):
    """Test company sentiment analysis with empty job postings list."""
    result = sentiment_analyzer.analyze_company_sentiment([])
    assert result['average_sentiment'] == 'neutral'
    assert result['total_postings'] == 0
    assert result['sentiment_distribution'] == {'positive': 0, 'neutral': 0, 'negative': 0} 