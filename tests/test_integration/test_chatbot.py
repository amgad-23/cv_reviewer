from fastapi.testclient import TestClient


def test_chatbot_flow(client: TestClient):
    """
    Test a simple conversation flow.
    """
    # Start a session
    session_id = "test-session-123"
    first_msg = {
        "session_id": session_id,
        "user_message": "Find candidates who know Python"
    }
    resp = client.post("/api/chatbot", json=first_msg)
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert "context" in data

    # Follow-up
    second_msg = {
        "session_id": session_id,
        "user_message": "Which of those has a Master's degree?"
    }
    resp2 = client.post("/api/chatbot", json=second_msg)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert "response" in data2
    # etc.
