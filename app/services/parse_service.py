from app.llm.open_ai_llm_client import llm_client
from app.llm.claude_llm_client import claude_client
import json


def parse_cv_text(text: str) -> dict:
    """
    Sends the raw text to LLM to parse the CV structure,
    returns a dict with keys: personal_info, education, experience, skills, projects, certifications.
    """
    try:
        # llm_response = claude_client.analyze_cv_text(text)
        llm_response = llm_client.analyze_cv_text(text)
        data = json.loads(llm_response)
    except json.JSONDecodeError:
        data = {
            "personal_info": {},
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "certifications": []
        }
    return data
