from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cv import CVRecord
from app.services.cv_query_services.abstract_cv_query import AbstractCVQueryService


class MySQLCVQueryService(AbstractCVQueryService):
    """
    Implementation of AbstractCVQueryService for MySQL with a JSON column.
    """

    def find_candidates_with_skill(self, db: Session, skill: str, partial: bool = False) -> List[Any]:
        if partial:
            # MySQL's JSON_EXTRACT or ->> operator might vary depending on your version.
            # Example for a naive partial match:
            return db.query(CVRecord).filter(
                func.lower(func.json_extract(CVRecord.skills, '$')).like(f"%{skill.lower()}%")
            ).all()
        else:
            # If 'skills' is a JSON array, and we want exact matching:
            return db.query(CVRecord).filter(
                CVRecord.skills.contains([skill])
            ).all()

    def compare_education_levels(self, db: Session, candidate_ids: List[int]) -> List[Dict[str, Any]]:
        records = db.query(CVRecord).filter(CVRecord.id.in_(candidate_ids)).all()
        results = []
        # (Same logic as the Postgres version)
        for record in records:
            education_info = record.education
            highest_degree = None
            if education_info and isinstance(education_info, list):
                rank_map = {'phd': 3, 'master': 2, 'bachelor': 1}
                max_rank = 0
                for edu in education_info:
                    deg = edu.get('degree', '').lower()
                    if 'phd' in deg and rank_map['phd'] > max_rank:
                        highest_degree = edu.get('degree')
                        max_rank = rank_map['phd']
                    elif 'master' in deg and rank_map['master'] > max_rank:
                        highest_degree = edu.get('degree')
                        max_rank = rank_map['master']
                    elif ('bachelor' in deg or 'bsc' in deg) and rank_map['bachelor'] > max_rank:
                        highest_degree = edu.get('degree')
                        max_rank = rank_map['bachelor']

            results.append({
                "candidate_id": record.id,
                "highest_degree": highest_degree if highest_degree else "Unknown"
            })
        return results

    def search_experience_in_industry(self, db: Session, industry_keyword: str) -> List[Any]:
        return db.query(CVRecord).filter(
            CVRecord.experience.ilike(f"%{industry_keyword}%")
        ).all()

    def match_candidates_for_job_requirements(self, db: Session, requirements: dict) -> List[Any]:
        skill_list = requirements.get("skills", [])
        min_exp = requirements.get("min_experience_years", 0)

        query = db.query(CVRecord)
        for skill in skill_list:
            # For MySQL JSON array:
            query = query.filter(CVRecord.skills.contains([skill]))

        # If you track experience:
        # query = query.filter(CVRecord.total_years_experience >= min_exp)

        return query.all()


cv_query_service = MySQLCVQueryService()
