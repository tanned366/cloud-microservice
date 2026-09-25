"""Utility functions for sentiment analysis and text statistics."""
import re
from typing import Tuple

POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "awesome", "fantastic", "wonderful",
    "love", "best", "happy", "brilliant", "outstanding", "superb", "terrific",
    "positive", "perfect", "clean", "fast", "reliable", "easy", "helpful", "delight"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "horrible", "awful", "worst", "poor", "hate", "sad",
    "broken", "slow", "fail", "failure", "bug", "error", "difficult", "useless",
    "disappointing", "ugly", "painful", "wrong", "annoying", "problem"
}


def analyze_sentiment(text: str) -> Tuple[str, float]:
    """
    Analyzes the sentiment of a given text.
    Returns a tuple of (sentiment_label, sentiment_score).
    Score ranges from -1.0 (most negative) to +1.0 (most positive).
    """
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return "neutral", 0.0

    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    total_sentiment_words = pos_count + neg_count

    if total_sentiment_words == 0:
        return "neutral", 0.0

    score = round((pos_count - neg_count) / total_sentiment_words, 2)

    if score > 0.15:
        sentiment = "positive"
    elif score < -0.15:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, score


def count_sentences(text: str) -> int:
    """Counts the number of sentences in a given text."""
    sentences = re.split(r'[.!?]+', text.strip())
    return max(1, len([s for s in sentences if s.strip()]))


def estimate_reading_time(word_count: int, wpm: int = 200) -> float:
    """Estimates reading time in seconds assuming 200 words per minute."""
    if word_count == 0:
        return 0.0
    return round((word_count / wpm) * 60, 2)


def perform_text_transformation(text: str, operation: str) -> str:
    """Performs string transformation based on requested operation."""
    op = operation.strip().lower()
    if op == "uppercase":
        return text.upper()
    elif op == "lowercase":
        return text.lower()
    elif op == "reverse":
        return text[::-1]
    elif op == "titlecase":
        return text.title()
    else:
        raise ValueError(f"Unsupported operation: '{operation}'. Supported: uppercase, lowercase, reverse, titlecase")
