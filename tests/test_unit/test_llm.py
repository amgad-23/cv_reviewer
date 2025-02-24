from unittest.mock import patch

from app.llm.open_ai_llm_client import llm_client
from app.services.chatbot_service import chatbot_query


@patch("app.services.llm_service.openai.ChatCompletion.create",
       return_value={"choices": [{"message": {"content": "Mocked LLM response"}}]})
def test_call_openai(mock_openai):
    response = chatbot_query("Parse my CV", [])
    assert response == "Mocked LLM response"
    mock_openai.assert_called_once()


def test_llm_response_structure():
    sample_cv_text = "John Doe\nPython Developer at Google\nB.Sc. in CS from MIT\nSkills: Python, Django, AWS"

    response = llm_client.analyze_cv_text(sample_cv_text)

    # Ensure it's valid JSON
    assert isinstance(response, dict), "Response should be a dictionary"

    # Personal Info
    assert "personal_info" in response
    assert isinstance(response["personal_info"], dict)
    assert "name" in response["personal_info"]
    assert "email" in response["personal_info"]
    assert "phone" in response["personal_info"]

    # Education should always be a list
    assert "education" in response
    assert isinstance(response["education"], list)

    # Experience should always be a list
    assert "experience" in response
    assert isinstance(response["experience"], list)

    # Skills should be a flat list
    assert "skills" in response
    assert isinstance(response["skills"], list)
    assert all(isinstance(skill, str) for skill in response["skills"]), "Skills must be a list of strings"

    # Projects should be a list (even if empty)
    assert "projects" in response
    assert isinstance(response["projects"], list)

    # Certifications should be a list (even if empty)
    assert "certifications" in response
    assert isinstance(response["certifications"], list)

    print("LLM response structure is correct!")


test_llm_response_structure()
