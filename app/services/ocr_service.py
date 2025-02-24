import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from docx import Document
import io
from app.core.config import settings
from app.core.logger import module_logger

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH


def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a given file (PDF, Word, or Image).
    :param file_path: Path to the file.
    :return: Extracted text as a string.
    """
    text = ""
    file_extension = os.path.splitext(file_path)[-1].lower()
    module_logger.info(f"Extracting text from file: {file_path}")

    if file_extension == ".pdf":
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    elif file_extension in [".docx", ".doc"]:
        doc = Document(file_path)
        for rel in doc.part.rels:
            if "image" in doc.part.rels[rel].target_ref:
                image_part = doc.part.rels[rel].target_part
                image_data = image_part.blob
                image = Image.open(io.BytesIO(image_data))
                text += pytesseract.image_to_string(image) + "\n"

    elif file_extension in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    else:
        module_logger.error("Unsupported file format. Only PDF, Word, and image files are supported.")
        raise ValueError("Unsupported file format. Only PDF, Word, and image files are supported.")
    module_logger.info(f"Extracted text: {text}")
    return text


if __name__ == "__main__":
    # Test the function with a sample file
    cvs_dir = "C:\\Users\\engam\\Downloads\\Documents\\CVs\\CVs"
    for file in os.listdir(cvs_dir):
        print(f"Extracting text from: {file}")
        file_path = os.path.join(cvs_dir, file)
        extracted_text = extract_text_from_file(file_path)
        print(extracted_text)
        print("=" * 50)
