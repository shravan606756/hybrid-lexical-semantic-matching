from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaning import clean_and_remove_stopwords
from utils.scoring import compute_vectorizer_and_scores
from ui.charts import plot_ranked_bars
from utils.section_extraction import extract_sections
import streamlit as st


st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("Resume Analyzer — Batch scoring")

uploaded_files = st.file_uploader("Upload resumes (PDF)", type=["pdf"], accept_multiple_files=True)
job_description = st.text_area("Paste job description", height=220)

if st.button("Analyze"):
    if not uploaded_files or not job_description:
        st.warning("Upload resumes and paste a job description first.")
    else:
        raw_texts = [extract_text_from_pdf(f) for f in uploaded_files]
        cleaned = [clean_and_remove_stopwords(t) for t in raw_texts]
        df = compute_vectorizer_and_scores(cleaned, job_description, [f.name for f in uploaded_files])

        st.subheader("Ranked results")
        st.table(df)
        plot_ranked_bars(df)

        # show parsed sections for top resume
        top = df.iloc[0] if not df.empty else None
        if top is not None:
            top_idx = df.index[0]
            st.markdown("---")
            st.subheader(f"Top resume: {top['Filename']}")
            raw = raw_texts[0]
            sections = extract_sections(raw)
            skills = sections.get("skills", {}).get("skills_list", [])
            st.write("Skills found:", ", ".join(skills) if skills else "No skills found")

        st.download_button("Download CSV", df.to_csv(index=False), file_name="results.csv")
