from unittest.mock import patch
from app.services.ocr_service import extract_text_from_file


@patch("app.services.ocr_service.pytesseract.image_to_string", return_value="Sample OCR text")
def test_extract_text_from_pdf(mock_tesseract):
    text = extract_text_from_file("data/sample_cvs/File.pdf")
    assert text == "Sample OCR text"
    mock_tesseract.assert_called_once()
