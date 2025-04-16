from nltk.tokenize import sent_tokenize
import time
from textblob import TextBlob
from utils import UNEXPECTED_ERROR

def analyze_sentiment(text):
    try:
        # Try using TextBlob for sentiment analysis
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except:
            # Simple positive/negative word detection as fallback
            positive_words = ["good", "great", "excellent", "positive", "true", "correct", "fact", "proven"]
            negative_words = ["bad", "wrong", "false", "incorrect", "lie", "misleading", "fake"]
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count == negative_count:
                return 0
            return (positive_count - negative_count) / max(positive_count + negative_count, 1)
    except Exception as e:
        print(UNEXPECTED_ERROR.format(str(e)))
        return 0  # Neutral sentiment as fallback 