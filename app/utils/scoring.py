from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def compute_vectorizer_and_scores(resumes_cleaned: list, job_description: str, filenames: list) -> pd.DataFrame:
    all_texts = [job_description] + resumes_cleaned
    vect = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
    vect.fit(all_texts)

    job_vec = vect.transform([job_description])
    rows = []
    for i, r in enumerate(resumes_cleaned):
        vec = vect.transform([r])
        score = cosine_similarity(vec, job_vec)[0][0] * 100
        rows.append({"Filename": filenames[i], "Match%": round(score, 2)})

    df = pd.DataFrame(rows).sort_values("Match%", ascending=False).reset_index(drop=True)
    return df
