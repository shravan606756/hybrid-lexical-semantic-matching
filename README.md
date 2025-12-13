# Resume Analyzer

A Streamlit-based NLP application for batch resume screening that ranks resumes against a job description using semantic similarity, section extraction, and skill identification.

The system is designed to be lightweight, interpretable, and practical for small-scale resume analysis (10–20 resumes), avoiding black-box models while maintaining meaningful relevance scoring.

---

## Overview

Resume screening is often manual, subjective, and time-consuming. This project automates the initial screening step by analyzing resumes in PDF format and ranking them based on their relevance to a provided job description.

The focus of this project is:
- Clear NLP pipeline design
- Explainable scoring logic
- Modular and extensible architecture

---

## Features

- Upload and process multiple resume PDFs in one batch
- Robust text extraction from PDF files
- Text preprocessing including normalization, tokenization, and stopword removal
- TF-IDF based semantic representation using unigrams and bigrams
- Cosine similarity scoring between resumes and job description
- Resume ranking based on match percentage
- Resume section extraction (skills, experience, education)
- Skill identification using a predefined technical skill vocabulary
- Visual ranking using horizontal bar charts
- CSV export of ranked results

---

## System Workflow

1. User uploads multiple resume PDFs and provides a job description
2. Text is extracted from each resume
3. Text is cleaned and preprocessed
4. TF-IDF vectorizer is trained on resumes and job description
5. Cosine similarity is computed for each resume
6. Resumes are ranked based on similarity score
7. Sections and skills are extracted from the top-ranked resume
8. Results are displayed in tabular and visual form

---

## Project Structure

app/main.py              → Streamlit entry point  
utils/pdf_parser.py     → Extracts text from resumes  
utils/text_cleaning.py  → Cleans and normalizes text  
utils/scoring.py        → TF-IDF + similarity scoring  
utils/section_extraction.py → Section & skill extraction  
ui/charts.py            → Visualizations.


---

## Technologies Used

- Python
- Streamlit
- Scikit-learn
  - TF-IDF Vectorizer
  - Cosine Similarity
- Pandas
- Matplotlib
- PyPDF2

---

## Technical Details

### Text Processing
- Case normalization
- Removal of non-essential characters
- Lightweight tokenization
- Stopword removal using a custom minimal stopword set

### Vectorization
- TF-IDF vectorization with unigram and bigram support
- Vocabulary learned jointly from resumes and job description

### Scoring
- Cosine similarity between each resume vector and job description vector
- Similarity score scaled to percentage for interpretability

### Section Extraction
- Heuristic-based heading detection for common resume sections
- Skill extraction using a curated list of technical skills
- Fallback inference when explicit section headings are missing

---

## How to Run Locally

1. Clone the repository:
git clone https://github.com/shravan606756/resume-analyzer.git

2. Install dependencies:


3. Run the application:

4. Upload resume PDFs and paste a job description to analyze.

---

## Use Cases

- Resume shortlisting for internships or entry-level roles
- Skill relevance analysis for students
- Demonstration of applied NLP concepts
- Academic mini-project or placement portfolio project

---

## Limitations

- Skill extraction depends on a predefined skill list
- Section detection is heuristic-based and may vary across resume formats
- Not intended for large-scale enterprise ATS systems
- Does not use transformer-based embeddings by design

---

## Future Enhancements

- Section-wise similarity scoring (skills vs experience vs education)
- Custom skill vocabulary input
- Optional embedding-based semantic matching
- Keyword-level match highlighting
- Resume-to-resume similarity detection

---

## Author

Developed as an applied Natural Language Processing project focusing on practical resume analysis, modular design, and explainable scoring.
