import re

# light-weight tokenization + stopword removal without NLTK
# small built-in stopword list (you can expand it later)
STOP_WORDS = {
    "a","an","the","and","or","in","on","for","with","to","of","is","are","was","were",
    "i","you","he","she","it","they","we","this","that","these","those","as","by",
    "at","from","be","been","has","have","had","but","not","will","can","may"
}

def clean_text(text: str) -> str:
    if not text:
        return ""
    t = text.lower()
    # keep letters, numbers, spaces and +, #, . (for things like c++, c#, scikit-learn)
    t = re.sub(r"[^a-z0-9\+\#\.\-\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def tokenize(text: str):
    # return list of word-like tokens (keeps c++, c#, scikit-learn as tokens)
    return re.findall(r"[a-z0-9\+\#\.\-]+", text.lower())

def clean_and_remove_stopwords(text: str) -> str:
    cleaned = clean_text(text)
    tokens = [w for w in tokenize(cleaned) if w not in STOP_WORDS and len(w) > 1]
    return " ".join(tokens)
