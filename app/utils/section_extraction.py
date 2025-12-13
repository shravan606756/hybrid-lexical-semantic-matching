import re
from typing import Dict
from collections import defaultdict

SECTION_HEADINGS = [
    r"^experience",
    r"^work experience",
    r"^professional experience",
    r"^employment history",
    r"^education",
    r"^academic qualifications",
    r"^skills",
    r"^technical skills",
    r"^projects",
    r"^certifications",
    r"^internships",
]

COMMON_SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "data structures",
    "algorithms",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "docker",
    "aws",
    "azure",
    "html",
    "css",
    "javascript",
    "react",
    "git",
    "linux"
]

def _find_headings(lines):
    headings = []
    for i, ln in enumerate(lines):
        s = ln.strip().lower()
        s_norm = re.sub(r"\s+", " ", s)
        for pat in SECTION_HEADINGS:
            if re.match(pat, s_norm):
                headings.append((i, s_norm))
                break
    return headings

def segment_by_headings(text: str):
    lines = text.splitlines()
    headings = _find_headings(lines)
    sections = defaultdict(list)

    if not headings:
        sections["full"] = text
        return sections

    indices = [idx for idx, _ in headings] + [len(lines)]

    for i in range(len(headings)):
        idx, h = headings[i]
        start = idx + 1
        end = indices[i + 1]
        body = "\n".join(lines[start:end]).strip()
        key = re.sub(r"[^a-z0-9]", "_", h).strip("_")
        sections[key] = body

    return sections

def extract_skills_from_text(text: str):
    text = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found.append(skill)

    return list(dict.fromkeys(found))

def extract_sections(text: str) -> Dict[str, object]:
    if not text:
        return {}

    text = text.replace("\r\n", "\n")
    segs = segment_by_headings(text)
    out = {}

    for k, v in segs.items():
        if "skill" in k:
            out["skills"] = {
                "raw": v,
                "skills_list": extract_skills_from_text(v)
            }
        elif "experience" in k or "employment" in k:
            out["experience"] = {"raw": v}
        elif "education" in k or "academic" in k:
            out["education"] = {"raw": v}
        else:
            out[k] = {"raw": v}

    if "skills" not in out:
        inferred = extract_skills_from_text(text)
        out["skills"] = {"raw": "", "skills_list": inferred}

    return out
