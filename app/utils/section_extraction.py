import re
from typing import Dict, List
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
    "python", "java", "c++", "c", "sql", "postgresql", "mysql", "mongodb",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "nlp", "spacy", "transformers", "docker", "aws", "azure",
    "html", "css", "javascript", "react", "git", "linux", "bash",
]

def _find_headings(lines: List[str]):
    headings = []
    for i, ln in enumerate(lines):
        s = ln.strip().lower()
        s_norm = re.sub(r"\s+", " ", s)
        for pat in SECTION_HEADINGS:
            if re.match(pat, s_norm):
                headings.append((i, s_norm))
                break
    return headings

def segment_by_headings(text: str) -> Dict[str, str]:
    lines = [l for l in text.splitlines()]
    headings = _find_headings(lines)
    sections = defaultdict(list)
    if not headings:
        sections['full'] = text
        return sections

    indices = [idx for idx, _ in headings] + [len(lines)]
    for j in range(len(headings)):
        idx, h = headings[j]
        start = idx + 1
        end = indices[j+1]
        body = "\n".join(lines[start:end]).strip()
        key = re.sub(r"[^a-z0-9]", "_", h).strip('_')
        sections[key] = body
    return sections

def extract_skills_from_text(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z\+\#\.\-]+", text.lower())
    found = []
    skills_set = set([s.lower() for s in COMMON_SKILLS])
    for t in tokens:
        if t in skills_set:
            found.append(t)
    seen = set()
    out = []
    for s in found:
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out

def extract_sections(text: str) -> Dict[str, object]:
    """
    Returns dict with keys for found sections. Example:
    {
      'skills': {'raw': '...', 'skills_list': ['python','sql']},
      'experience': {'raw': '...'},
      'education': {'raw': '...'}
    }
    """
    if not text:
        return {}
    text = text.replace('\r\n', '\n')
    segs = segment_by_headings(text)
    out = {}
    for k, v in segs.items():
        if 'skill' in k:
            out['skills'] = {'raw': v, 'skills_list': extract_skills_from_text(v)}
        elif 'experience' in k or 'employment' in k or 'professional' in k:
            out['experience'] = {'raw': v}
        elif 'education' in k or 'academic' in k:
            out['education'] = {'raw': v}
        else:
            out[k] = {'raw': v}

    if 'skills' not in out:
        inferred = extract_skills_from_text(text)
        out['skills'] = {'raw': '', 'skills_list': inferred}

    return out
