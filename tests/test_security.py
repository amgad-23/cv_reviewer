
def test_sql_injection(client):
    response = client.get("/api/candidates-with-skill?skill=' OR 1=1;--")
    assert response.status_code == 400  # Expecting rejection
