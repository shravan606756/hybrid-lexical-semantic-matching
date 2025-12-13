def extract_skills_from_text(text: str, skill_list: list):
    if not text:
        return set()

    text = text.lower()
    found = set()

    for skill in skill_list:
        if skill in text:
            found.add(skill)

    return found


def skill_gap_analysis(resume_text: str, jd_text: str, skill_list: list):
    resume_skills = extract_skills_from_text(resume_text, skill_list)
    jd_skills = extract_skills_from_text(jd_text, skill_list)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra
    }
