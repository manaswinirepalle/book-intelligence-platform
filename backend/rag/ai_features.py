import re
from collections import Counter


def generate_summary(description: str, max_sentences: int = 2) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", description.strip())
    return " ".join(sentences[:max_sentences]) if sentences else ""


def classify_genre(description: str) -> str:
    genre_keywords = {
        "Fantasy": ["magic", "dragon", "wizard", "kingdom"],
        "Science Fiction": ["space", "future", "technology", "robot"],
        "Romance": ["love", "romance", "heart", "relationship"],
        "Mystery": ["murder", "detective", "mystery", "clue"],
        "Non-Fiction": ["history", "science", "biography", "research"],
    }
    text = description.lower()
    scores = {g: sum(k in text for k in keys) for g, keys in genre_keywords.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"


def sentiment_analysis(text: str) -> str:
    positive = {"excellent", "amazing", "good", "great", "loved", "brilliant"}
    negative = {"poor", "bad", "boring", "terrible", "awful", "hated"}
    tokens = re.findall(r"\w+", text.lower())
    counter = Counter(tokens)
    pos = sum(counter[t] for t in positive)
    neg = sum(counter[t] for t in negative)
    if pos > neg:
        return "Positive"
    if neg > pos:
        return "Negative"
    return "Neutral"

