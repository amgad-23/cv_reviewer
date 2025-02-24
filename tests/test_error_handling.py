def test_missing_file_upload(client):
    response = client.post("/api/upload-cv", files={})
    assert response.status_code == 400


def test_invalid_llm_response(client):
    response = client.post("/api/chatbot", json={"session_id": "123", "user_message": ""})
    assert response.status_code == 400
