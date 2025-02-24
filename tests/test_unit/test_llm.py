from unittest.mock import patch
from app.services.chatbot_service import chatbot_query


@patch("app.services.llm_service.openai.ChatCompletion.create",
       return_value={"choices": [{"message": {"content": "Mocked LLM response"}}]})
def test_call_openai(mock_openai):
    response = chatbot_query("Parse my CV", [])
    assert response == "Mocked LLM response"
    mock_openai.assert_called_once()
