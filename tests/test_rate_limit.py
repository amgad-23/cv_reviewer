import time


def test_rate_limit(client):
    for _ in range(11):  # Assuming limit is 10 per minute
        response = client.get("/api/candidates-with-skill?skill=Python")
        if response.status_code == 429:
            break

    assert response.status_code == 429  # Expecting "Too Many Requests"
