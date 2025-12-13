from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_section(section_text: str, jd_text: str) -> float:
    if not section_text or not jd_text:
        return 0.0

    vect = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
    vect.fit([section_text, jd_text])

    sec_vec = vect.transform([section_text])
    jd_vec = vect.transform([jd_text])

    return cosine_similarity(sec_vec, jd_vec)[0][0] * 100


def section_wise_scores(sections: dict, jd_text: str):
    skills_text = sections.get("skills", {}).get("raw", "")
    projects_text = sections.get("projects", {}).get("raw", "")
    experience_text = sections.get("experience", {}).get("raw", "")

    skills_score = score_section(skills_text, jd_text)
    projects_score = score_section(projects_text, jd_text)
    experience_score = score_section(experience_text, jd_text)

    final_score = (
        0.4 * skills_score +
        0.4 * projects_score +
        0.2 * experience_score
    )

    return {
        "skills": round(skills_score, 2),
        "projects": round(projects_score, 2),
        "experience": round(experience_score, 2),
        "final": round(final_score, 2)
    }
