from .models import Sentiment


def get_sentiment_by_review_text(text):
    if any(k in text for k in ('хорош', 'люблю')):
        return Sentiment.POSITIVE
    if any(k in text for k in ('плохо', 'ненавиж')):
        return Sentiment.NEGATIVE
    return Sentiment.NEUTRAL