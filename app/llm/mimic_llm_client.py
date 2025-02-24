import json


def mock_llm_parse_cv_text(cv_text: str) -> str:
    """
    Mimics the response of an LLM parsing a CV.
    Returns a JSON string with the keys:
    ["personal_info", "education", "experience", "skills", "projects", "certifications"].

    For testing, we ignore the input cv_text and just return a dummy structure.
    """
    # Example static JSON response:
    response_dict = {
        "personal_info": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890"
        },
        "education": [
            {
                "degree": "B.Sc. in Computer Science",
                "institution": "University of Testing",
                "year": "2018 - 2022"
            }
        ],
        "experience": [
            {
                "title": "Software Developer",
                "company": "TestCorp",
                "duration": "2 years"
            }
        ],
        "skills": ["Python", "FastAPI", "Docker"],
        "projects": [
            {
                "name": "Mock Project",
                "description": "A project to demonstrate a mock LLM response."
            }
        ],
        "certifications": ["AWS Certified Solutions Architect"]
    }
    return json.dumps(response_dict)
