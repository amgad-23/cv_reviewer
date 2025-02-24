from fastapi.testclient import TestClient


def test_candidates_with_skill(client: TestClient):
    response = client.get("/api/candidates-with-skill?skill=Python")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "candidates" in data


def test_experience_in_industry(client: TestClient):
    response = client.get("/api/experience-in-industry?industry=finance")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data


def test_get_all_cv_records(client: TestClient):
    """Test the /cv-records API endpoint to ensure it returns structured data."""

    response = client.get("/cv-records")
    assert response.status_code == 200

    json_data = response.json()

    # Ensure count is returned
    assert "count" in json_data
    assert isinstance(json_data["count"], int), "Count should be an integer"

    # Ensure candidates are returned as a list
    assert "candidates" in json_data
    assert isinstance(json_data["candidates"], list), "Candidates should be a list"

    if json_data["count"] > 0:
        first_candidate = json_data["candidates"][0]

        # Ensure all required fields exist
        assert "personal_info" in first_candidate
        assert "education" in first_candidate
        assert "experience" in first_candidate
        assert "skills" in first_candidate
        assert "projects" in first_candidate
        assert "certifications" in first_candidate

        # Ensure proper formats
        assert isinstance(first_candidate["education"], list)
        assert isinstance(first_candidate["experience"], list)
        assert isinstance(first_candidate["skills"], list)
        assert isinstance(first_candidate["projects"], list)
        assert isinstance(first_candidate["certifications"], list)

    print("✅ API response structure is correct!")
