from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session


class AbstractCVQueryService(ABC):
    """
    An abstract base class defining the interface for CV-related queries.
    """

    @abstractmethod
    def find_candidates_with_skill(self, db: Session, skill: str, partial: bool = False) -> List[Any]:
        """
        Return all CVs that list the specific skill in 'skills'.
        Partial matching or exact matching depends on 'partial'.
        """
        pass

    @abstractmethod
    def compare_education_levels(self, db: Session, candidate_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Compare education levels for certain candidate IDs.
        Return structured results with relevant details.
        """
        pass

    @abstractmethod
    def search_experience_in_industry(self, db: Session, industry_keyword: str) -> List[Any]:
        """
        Return CVs that mention the industry keyword in their experience.
        """
        pass

    @abstractmethod
    def match_candidates_for_job_requirements(self, db: Session, requirements: dict) -> List[Any]:
        """
        Match candidates based on a 'requirements' dict,
        e.g. required skills, minimum experience, etc.
        """
        pass
