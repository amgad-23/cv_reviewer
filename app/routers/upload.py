import os
import uuid
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.logger import module_logger
from app.db import SessionLocal
from app.models.cv import CVRecord
from app.services.ocr_service import extract_text_from_file
from app.services.parse_service import parse_cv_text

router = APIRouter()
TMP_FOLDER = "tmp"
os.makedirs(TMP_FOLDER, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# add rate limiter to this endpoint
@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(TMP_FOLDER, filename)
    try:

        with open(temp_path, "wb") as f:
            f.write(await file.read())
        text = extract_text_from_file(temp_path)
        parsed_data = parse_cv_text(text)

        cv_record = CVRecord(
            filename=file.filename,
            personal_info=parsed_data.get("personal_info", {}),
            education=parsed_data.get("education", []),
            experience=parsed_data.get("experience", []),
            skills=parsed_data.get("skills", []),
            projects=parsed_data.get("projects", []),
            certifications=parsed_data.get("certifications", []),
            raw_text=text
        )
        db.add(cv_record)
        db.commit()
        db.refresh(cv_record)
    except Exception as e:
        module_logger.error(f"Error processing CV: {e}")
        return JSONResponse({"message": f"Error processing CV"}, status_code=400)
    finally:
        os.remove(temp_path)
    return JSONResponse({"cv_id": cv_record.id, "message": "CV uploaded and processed successfully."}, status_code=201)


