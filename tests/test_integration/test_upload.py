from fastapi.testclient import TestClient
import pytest
import os

def test_upload_cv(client: TestClient):
    test_file_path = "data/sample_cvs/File.pdf"
    if not os.path.exists(test_file_path):
        # create a tiny dummy file for demonstration
        with open(test_file_path, "wb") as f:
            f.write(b"Dummy PDF content")

    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/upload-cv",
            files={"file": ("dummy_cv.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "cv_id" in data
    assert data["message"] == "CV uploaded and processed successfully."
