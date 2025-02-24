from fastapi.testclient import TestClient


def test_candidates_with_skill(client: TestClient):
    # Insert a test record in DB or assume one was created
    # Then query the skill
    response = client.get("/api/candidates-with-skill?skill=Python")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "candidates" in data

    # Optionally check that an expected candidate is returned


def test_experience_in_industry(client: TestClient):
    response = client.get("/api/experience-in-industry?industry=finance")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    # etc.
