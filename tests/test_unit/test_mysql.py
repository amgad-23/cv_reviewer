from sqlalchemy.orm import Session
from sqlalchemy.testing import db

from app.models.cv import CVRecord
from app.services.cv_query_services.mysq_cv_query import cv_query_service


def test_find_candidates_with_skill(db: Session):
    """Test searching for candidates with a skill (now ensuring skills are a flat list)."""

    # Insert test data
    test_cv = CVRecord(
        filename="test.pdf",
        personal_info={"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"},
        education=[{"degree": "B.Sc. in Computer Science", "institution": "MIT", "years": "2015-2019"}],
        experience=[{"job_title": "Python Developer", "company": "Google", "duration": "2019 - Present"}],
        skills=["Python", "Django", "AWS"],  # Ensure skills are a list, not nested
        projects=[],
        certifications=[]
    )
    db.add(test_cv)
    db.commit()

    # Query by skill
    results = cv_query_service.find_candidates_with_skill(db, "Python")

    assert len(results) > 0, "Should return at least one candidate"
    assert isinstance(results[0].skills, list), "Skills should be stored as a list"
    assert "Python" in results[0].skills, "Python should be listed as a skill"

    print("✅ Skill search test passed!")

test_find_candidates_with_skill(db)
