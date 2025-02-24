import random
import json

from app.llm.abstract_llm_client import AbstractLLMClient

user_intents = ['find_skill', 'search_industry', 'compare_education', 'job_requirements']


class MockLLMClient(AbstractLLMClient):


    def analyze_cv_text(self, cv_text: str) -> str:
        """
        Mimics the response of an LLM parsing a CV.
        Returns a JSON string with the keys:
        {{
                "personal_info": {{
                    "name": "John Doe",
                    "email": "john.doe@email.com",
                    "phone": "+1 123-456-7890"
                }},
                "education": [
                    {{
                        "degree": "Bachelor of Science in Computer Science",
                        "institution": "MIT",
                        "years": "2015 - 2019"
                    }}
                ],
                "experience": [
                    {{
                        "job_title": "Python Developer",
                        "company": "Google",
                        "duration": "2019 - Present"
                    }}
                ],
                "skills": ["Python", "Django", "AWS"],
                "projects": [
                    {{
                        "project_name": "Stock Prediction AI",
                        "description": "A machine learning model to predict stock prices."
                    }}
                ],
                "certifications": [
                    {{
                        "certification_name": "AWS Certified Solutions Architect",
                        "institution": "Amazon",
                        "year": "2021"
                    }}
                ]
            }}

        For testing, we ignore the input cv_text and just return a dummy structure.
        """
        # Example static JSON response:
        response_dict = {
            "personal_info": {
                "name": "John Doe",
                "email": "test@test.com",
                "phone": "+1 123-456-7890"
            },
            "education": [
                {
                    "degree": "Bachelor of Science in Computer Science",
                    "institution": "MIT",
                    "years": "2015 - 2019"
                }
            ],
            "experience": [
                {
                    "job_title": "Python Developer",
                    "company": "Google",
                    "duration": "2019 - Present"
                }
            ],
            "skills": ["Python", "Django", "AWS"],
            "projects": [
                {
                    "project_name": "Stock Prediction AI",
                    "description": "A machine learning model to predict stock prices."
                }
            ],
            "certifications": [
                {
                    "certification_name": "AWS Certified Solutions Architect",
                    "institution": "Amazon",
                    "year": "2021"
                }
            ]
        }
        return json.dumps(response_dict)

    def analyze_user_query(self, user_message: str) -> str:
        """
        Mimics the response of an LLM parsing a user query.
        Returns a JSON string with the keys:
        {{
            "intent": "find_skill" | "search_industry" | "compare_education" | "job_requirements",
            "parameters": {{
                "skill": "Python" (for find_skill),
                "industry": "Finance" (for search_industry),
                "candidate_ids": [1, 2, 3] (for compare_education),
                "requirements": {{
                    "skills": ["Python", "Django"],
                    "min_experience_years": 3
                }} (for job_requirements)
            }}
        }}

        Example 1:
        User: "Find me Python developers."
        Response:
        {{
            "intent": "find_skill",
            "parameters": {{"skill": "Python"}}
        }}

        Example 2:
        User: "Who worked in the finance industry?"
        Response:
        {{
            "intent": "search_industry",
            "parameters": {{"industry": "Finance"}}
        }}

        Example 3:
        User: "Compare the education of those candidates."
        Response:
        {{
            "intent": "compare_education",
            "parameters": {{"candidate_ids": []}}
        }}

        Example 4:
        User: "Find Python and Django developers with at least 3 years of experience."
        Response:
        {{
            "intent": "job_requirements",
            "parameters": {{
                "skills": ["Python", "Django"],
                "min_experience_years": 3
            }}
        }}

        """
        # Example static JSON response:
        response_dict = {
            "intent": random.choice(user_intents),
            "parameters": {
                "skill": "Python",
                "industry": "Finance",
                "candidate_ids": [1, 2, 3],
                "requirements": {
                    "skills": ["Python", "Django"],
                    "min_experience_years": 3
                }
            }
        }
        return json.dumps(response_dict)
