from utils.section_scoring import section_wise_scores
from utils.skill_gap import skill_gap_analysis
from utils.section_extraction import COMMON_SKILLS, extract_sections
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaning import clean_and_remove_stopwords
from utils.scoring import compute_vectorizer_and_scores
from ui.charts import plot_ranked_bars
import streamlit as st

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("Resume Analyzer — Batch scoring")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF)", type=["pdf"], accept_multiple_files=True
)
job_description = st.text_area("Paste job description", height=220)

if st.button("Analyze"):
    if not uploaded_files or not job_description:
        st.warning("Upload resumes and paste a job description first.")
    else:
        # -------- Load and preprocess resumes --------
        raw_texts = [extract_text_from_pdf(f) for f in uploaded_files]
        cleaned = [clean_and_remove_stopwords(t) for t in raw_texts]
        filenames = [f.name for f in uploaded_files]

        # -------- Global ranking --------
        df = compute_vectorizer_and_scores(cleaned, job_description, filenames)

        st.subheader("Ranked results")
        st.table(df)
        plot_ranked_bars(df)

        # -------- Detailed analysis for top resume --------
        if not df.empty:
            st.markdown("---")
            top = df.iloc[0]
            st.subheader(f"Top resume: {top['Filename']}")

            top_idx = filenames.index(top["Filename"])
            raw = raw_texts[top_idx]

            sections = extract_sections(raw)
            skills = sections.get("skills", {}).get("skills_list", [])

            st.write(
                "Skills found:",
                ", ".join(skills) if skills else "No skills found"
            )

            # -------- Skill Gap Analysis --------
            gap = skill_gap_analysis(
                resume_text=raw,
                jd_text=job_description,
                skill_list=COMMON_SKILLS
            )

            with st.container():
                st.markdown("## Skill Gap Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Matched Skills**")
                    st.write(", ".join(gap["matched"]) if gap["matched"] else "None")

                with col2:
                    st.markdown("**Missing Skills**")
                    st.write(", ".join(gap["missing"]) if gap["missing"] else "None")

                with col3:
                    st.markdown("**Extra Skills**")
                    st.write(", ".join(gap["extra"]) if gap["extra"] else "None")

            # -------- Section-wise scoring --------
            sec_scores = section_wise_scores(sections, job_description)

            with st.container():
                st.markdown("## Section-wise Match Scores")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Skills", f"{sec_scores['skills']}%")
                col2.metric("Projects", f"{sec_scores['projects']}%")
                col3.metric("Experience", f"{sec_scores['experience']}%")
                col4.metric("Final ATS Score", f"{sec_scores['final']}%")

        # -------- Download --------
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="results.csv"
        )
