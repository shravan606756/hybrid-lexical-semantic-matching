from utils.explainability import explain_top_resume
from utils.suggestions import generate_suggestions
from utils.embedding_scoring import compute_embedding_scores
from utils.section_scoring import section_wise_scores
from utils.skill_gap import skill_gap_analysis
from utils.section_extraction import COMMON_SKILLS, extract_sections
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaning import clean_and_remove_stopwords
from utils.scoring import compute_vectorizer_and_scores
from ui.charts import plot_ranked_bars
import streamlit as st

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("Hybrid Lexical–Semantic Matching with Explainability and Feedback")

uploaded_files = st.file_uploader(
    "Upload resumes (PDF)", type=["pdf"], accept_multiple_files=True
)
job_description = st.text_area("Paste job description", height=220)

if st.button("Analyze"):
    if not uploaded_files or not job_description:
        st.warning("Upload resumes and paste a job description first.")
    else:
        # 🔄 Loading spinner while analysis runs
        with st.spinner("Analyzing resumes using semantic matching..."):

            # -------- Load and preprocess resumes --------
            raw_texts = [extract_text_from_pdf(f) for f in uploaded_files]
            cleaned = [clean_and_remove_stopwords(t) for t in raw_texts]
            filenames = [f.name for f in uploaded_files]

            # -------- TF-IDF ranking --------
            df = compute_vectorizer_and_scores(
                cleaned,
                job_description,
                filenames
            )

            # -------- Semantic embedding ranking --------
            embed_df = compute_embedding_scores(
                cleaned,
                job_description,
                filenames
            )

            # -------- Merge + final score --------
            df = df.merge(embed_df, on="Filename")

            df["Final Score"] = (
                0.5 * df["Match%"] +
                0.5 * df["Semantic Match%"]
            )

            df = df.sort_values(
                "Final Score",
                ascending=False
            ).reset_index(drop=True)

        # -------- Display results --------
        st.subheader("Ranked results (TF-IDF + Semantic Embeddings)")

        df_display = df.reset_index(drop=True)
        df_display.insert(0, "Rank", range(1, len(df_display) + 1))

        st.table(df_display)

        # Chart uses original df (contains Final Score)
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

            # -------- Explainability: Why ranked #1 --------
            explanations = explain_top_resume(
                resume_text=raw,
                jd_text=job_description,
                top_k=5
            )

            st.markdown("## Why this resume ranked #1")

            if explanations:
                for i, item in enumerate(explanations, 1):
                    st.markdown(
                        f"**{i}. ({item['score']}%)** {item['sentence']}"
                    )
            else:
                st.write("No strong matching sentences found.")

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

            # -------- Resume Improvement Suggestions --------
            st.markdown("---")
            st.markdown("## Resume Improvement Suggestions")

            suggestions = generate_suggestions(
                missing_skills=gap["missing"],
                section_scores=sec_scores
            )

            for i, s in enumerate(suggestions, 1):
                st.markdown(f"**{i}.** {s}")

        # -------- Download --------
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="results.csv"
        )
