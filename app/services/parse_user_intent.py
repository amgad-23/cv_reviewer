import re

def parse_user_intent(user_message: str):
    """
    Return (intent, params) based on keywords in user_message.
    This is a naive approach for demonstration:
       - Looks for words like 'skill', 'industry', 'education', etc.
    """
    text = user_message.lower()

    # We'll define some simple "intents" we recognize
    if "skill" in text or "know" in text or "expert" in text:
        # e.g. "Find me candidates who know Python"
        # Let's do a naive regex to find the skill
        # e.g. "python", "django", "react"
        match = re.search(r"(python|django|react|java|aws|sql)", text)
        skill = match.group(1) if match else "Python"  # default to "Python" if none found
        return ("find_skill", {"skill": skill})

    if "industry" in text or "experience in" in text:
        # e.g. "experience in finance" => industry=finance
        match = re.search(r"experience in ([A-Za-z]+)", text)
        industry = match.group(1) if match else "Finance"
        return ("search_industry", {"industry": industry})

    if "compare education" in text or "education" in text:
        # e.g. "Compare education of the last candidates"
        # Possibly parse candidate IDs
        match = re.findall(r"\d+", text)
        candidate_ids = [int(m) for m in match] if match else []
        return ("compare_education", {"candidate_ids": candidate_ids})

    if "follow up" in text or "out of those" in text:
        # e.g. "Out of those, who has Java skill?"
        match = re.search(r"skill (?:named )?(\w+)", text)
        skill = match.group(1) if match else "Java"
        return ("follow_up_filter", {"skill": skill})

    if "requirement" in text or "job" in text:
        # e.g. "We need Python and Django with 3 years of experience"
        # We'll do a naive parse
        skill_match = re.findall(r"(python|django|react|java|aws|sql)", text)
        exp_match = re.search(r"(\d+) ?years", text)
        exp = int(exp_match.group(1)) if exp_match else 0
        requirements = {
            "skills": skill_match,
            "min_experience_years": exp
        }
        return ("job_requirements", {"requirements": requirements})

    # Fallback
    return ("unknown", {})
