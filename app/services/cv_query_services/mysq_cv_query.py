from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, String
from app.models.cv import CVRecord
from app.services.cv_query_services.abstract_cv_query import AbstractCVQueryService


class MySQLCVQueryService(AbstractCVQueryService):
    """
    Implementation of AbstractCVQueryService for MySQL with a JSON column.
    """

    def find_candidates_with_skill(self, db: Session, skill: str, partial: bool = False) -> List[Any]:
        """
        Returns candidates that have a specific skill.
        - If `partial=True`, searches for substrings (e.g., "pyth" matches "Python").
        - If `partial=False`, matches exact skill names stored in the JSON array.
        """
        if partial:
            # Case-insensitive search within JSON array
            return db.query(CVRecord).filter(
                func.lower(cast(CVRecord.skills, String)).like(f"%{skill.lower()}%")
            ).all()
        else:
            # Exact skill match inside JSON array
            return db.query(CVRecord).filter(
                func.JSON_CONTAINS(CVRecord.skills, f'"{skill}"')
            ).all()

    def compare_education_levels(self, db: Session, candidate_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Returns the highest degree for each candidate.
        """
        records = db.query(CVRecord).filter(CVRecord.id.in_(candidate_ids)).all()
        results = []

        rank_map = {'phd': 3, 'master': 2, 'bachelor': 1}

        for record in records:
            education_info = record.education  # JSON array
            highest_degree = None
            max_rank = 0

            if education_info and isinstance(education_info, list):
                for edu in education_info:
                    deg = edu.get('degree', '').lower()
                    for key, rank in rank_map.items():
                        if key in deg and rank > max_rank:
                            highest_degree = edu.get('degree')
                            max_rank = rank

            results.append({
                "candidate_id": record.id,
                "highest_degree": highest_degree if highest_degree else "Unknown"
            })
        return results

    def search_experience_in_industry(self, db: Session, industry_keyword: str) -> List[Any]:
        """
        Returns candidates that have experience in the specified industry.
        - Matches JSON fields like "experience[].Company" and "experience[].Job Title".
        """
        return db.query(CVRecord).filter(
            func.lower(cast(CVRecord.experience, String)).like(f"%{industry_keyword.lower()}%")
        ).all()

    def match_candidates_for_job_requirements(self, db: Session, requirements: dict) -> List[Any]:
        """
        Returns candidates that match job requirements.
        - Filters by required skills.
        - Optionally filters by minimum years of experience.
        """
        skill_list = requirements.get("skills", [])
        min_exp = requirements.get("min_experience_years", 0)

        query = db.query(CVRecord)

        for skill in skill_list:
            query = query.filter(
                func.JSON_CONTAINS(CVRecord.skills, f'"{skill}"')
            )

        # If total experience is stored, filter by years
        # query = query.filter(CVRecord.total_years_experience >= min_exp)

        return query.all()

    def get_all_cv_records(self, db: Session):
        """
        Fetches all CV records from the database.
        """
        try:
            records = db.query(CVRecord).all()
            return records
        except Exception as e:
            print(f"Error fetching CV records: {e}")
            return []


# Create an instance
cv_query_service = MySQLCVQueryService()
