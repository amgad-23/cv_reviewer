def test_full_flow(client):
    # Step 1: Upload a CV
    response = client.post("/api/upload-cv", files={"file": ("dummy.pdf", b"data", "application/pdf")})
    assert response.status_code == 200
    cv_id = response.json()["cv_id"]

    # Step 2: Query skills
    response = client.get(f"/api/candidates-with-skill?skill=Python")
    assert response.status_code == 200

    # Step 3: Chatbot interaction
    response = client.post("/api/chatbot", json={"session_id": "e2e-test", "user_message": "Find Python candidates"})
    assert response.status_code == 200
