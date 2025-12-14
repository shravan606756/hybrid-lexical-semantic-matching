import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def split_into_sentences(text):
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def explain_top_resume(resume_text, jd_text, top_k=5):
    model = get_model()

    sentences = split_into_sentences(resume_text)
    if not sentences:
        return []

    jd_embedding = model.encode([jd_text], normalize_embeddings=True)
    sent_embeddings = model.encode(sentences, normalize_embeddings=True)

    scores = cosine_similarity(sent_embeddings, jd_embedding).flatten()

    ranked = sorted(
        zip(sentences, scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for sent, score in ranked[:top_k]:
        results.append({
            "sentence": sent,
            "score": round(score * 100, 2)
        })

    return results
