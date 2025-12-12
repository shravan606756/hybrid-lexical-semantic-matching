import PyPDF2

def extract_text_from_pdf(uploaded_file) -> str:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        parts = []
        for p in reader.pages:
            text = p.extract_text() or ""
            parts.append(text)
        return " ".join(parts).strip()
    except Exception:
        return ""
