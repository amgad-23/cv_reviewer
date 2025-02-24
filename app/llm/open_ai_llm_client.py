import json
import openai
from app.core.config import settings
from app.core.logger import module_logger
from app.llm.abstract_llm_client import AbstractLLMClient


class LLMClient(AbstractLLMClient):
    def __init__(self):
        # Configure OpenAI
        openai.api_key = settings.OPENAI_API_KEY

    def analyze_cv_text(self, text: str) -> str:
        """
        Example function to send CV text to GPT for structured analysis.
        Returns a JSON or string with extracted fields.
        """
        prompt = f"""
        You are a highly accurate CV parser. Extract the following information from the provided CV text and return a **clean, structured JSON output**:

        ### **Required Fields:**
        - **personal_info** → `{{
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1 123-456-7890"
        }}`
        - **education** → List of education entries: `{{
            "degree": "Bachelor of Science in Computer Science",
            "institution": "MIT",
            "years": "2015 - 2019"
        }}`
        - **experience** → List of work experience: `{{
            "job_title": "Python Developer",
            "company": "Google",
            "duration": "2019 - Present"
        }}`
        - **skills** → A **flat list of technical skills only** (DO NOT include "soft skills" or categories like "Technical" or "Soft").
        - **projects** → List of projects (if available).
        - **certifications** → List of certifications.

        ### **CV TEXT:**
        {text}

        ### **🔍 Output Format:**
        Ensure the **output is valid JSON**, following this structure:
        ```json
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
        ```
        **Return only the structured JSON output and nothing else.** If any field is missing in the CV, return an **empty list (`[]`) or `null` instead of omitting it.**
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
        except Exception as e:
            module_logger.error(f"Error analyzing CV text: {e}")
            return f"Error analyzing CV text: {e}"
        return response.choices[0].message["content"]

    def analyze_user_query(self, user_message: str) -> dict:
        """
        Uses GPT to understand user intent (e.g., find_skill, search_industry).
        Returns structured JSON output with intent and parameters.
        """
        prompt = f"""
        You are a CV Analysis Chatbot. Your task is to understand user queries and categorize them.
        Extract the following **intents** from the user query:
        - "find_skill" -> If the user is asking to find candidates with a specific skill (e.g., "Find Python developers").
        - "search_industry" -> If the user is looking for candidates with experience in a particular industry (e.g., "Find candidates who worked in finance").
        - "compare_education" -> If the user wants to compare education levels (e.g., "Compare education of the last candidates").
        - "job_requirements" -> If the user provides job requirements and wants matching candidates (e.g., "Find Python and Django devs with 3+ years of experience").

        Return the result in **JSON format**:
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

        User Query:
        {user_message}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            return json.loads(response.choices[0].message["content"])

        except Exception as e:
            module_logger.error(f"Error analyzing user query: {e}")
            return {"intent": "unknown", "parameters": {}}


llm_client = LLMClient()
