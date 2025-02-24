from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.cv_query_services.mysq_cv_query import cv_query_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/candidates-with-skill")
def candidates_with_skill(skill: str, db: Session = Depends(get_db)):
    results = cv_query_service.find_candidates_with_skill(db, skill)
    return {"count": len(results), "candidates": results}


@router.get("/experience-in-industry")
def experience_in_industry(industry: str, db: Session = Depends(get_db)):
    results = cv_query_service.search_experience_in_industry(db, industry)
    return {"count": len(results), "candidates": results}


@router.post("/match-candidates")
def match_candidates(requirements: dict, db: Session = Depends(get_db)):
    results = cv_query_service.match_candidates_for_job_requirements(db, requirements)
    return {"count": len(results), "candidates": results}


@router.get("/all-cv-records")
def all_cv_records(db: Session = Depends(get_db)):
    results = cv_query_service.get_all_cv_records(db)
    return {"count": len(results), "candidates": results}
