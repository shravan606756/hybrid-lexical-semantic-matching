def generate_suggestions(missing_skills, section_scores, threshold=40):
    suggestions = []

    # Skill-based suggestions (data-driven)
    for skill in missing_skills[:5]:
        suggestions.append(
            f"Add experience or projects demonstrating **{skill}**, as it is required in the job description."
        )

    # Section-based suggestions (rule-based, explainable)
    if section_scores.get("projects", 100) < threshold:
        suggestions.append(
            "Improve the **Projects** section by clearly stating technologies used, your role, and measurable impact."
        )

    if section_scores.get("experience", 100) < threshold:
        suggestions.append(
            "Align the **Experience** section more closely with the job responsibilities mentioned in the JD."
        )

    if section_scores.get("skills", 100) < threshold:
        suggestions.append(
            "Reorder and highlight the most relevant skills in the **Skills** section based on the job description."
        )

    # Fallback
    if not suggestions:
        suggestions.append(
            "Your resume aligns well with the job description. Focus on improving clarity and impact of bullet points."
        )

    return suggestions
