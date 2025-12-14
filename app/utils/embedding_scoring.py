from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def compute_embedding_scores(resumes, jd_text, filenames):
    model = get_model()

    texts = [jd_text] + resumes
    embeddings = model.encode(texts, normalize_embeddings=True)

    jd_emb = embeddings[0]
    res_embs = embeddings[1:]

    rows = []
    for i, emb in enumerate(res_embs):
        score = cosine_similarity(
            emb.reshape(1, -1),
            jd_emb.reshape(1, -1)
        )[0][0] * 100

        rows.append({
            "Filename": filenames[i],
            "Semantic Match%": round(score, 2)
        })

    return pd.DataFrame(rows)
