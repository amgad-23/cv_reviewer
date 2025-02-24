from sqlalchemy import Column, Integer, String, Text, JSON
from app.db import Base


class CVRecord(Base):
    __tablename__ = "cv_records"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    personal_info = Column(JSON)
    education = Column(JSON)
    experience = Column(JSON)
    skills = Column(JSON)
    projects = Column(JSON)
    certifications = Column(JSON)
    raw_text = Column(Text)
