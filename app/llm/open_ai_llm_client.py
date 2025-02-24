import openai
from app.core.config import settings
from app.core.logger import module_logger


class LLMClient:
    def __init__(self):
        # Configure OpenAI
        openai.api_key = settings.OPENAI_API_KEY

    def analyze_cv_text(self, text: str) -> str:
        """
        Example function to send CV text to GPT for structured analysis.
        Returns a JSON or string with extracted fields.
        """
        prompt = f"""
        You are a CV parser. Extract the following information from the CV text:
        - Personal Info (Name, Email, Phone if present)
        - Education (Degrees, Institutions, Years)
        - Work Experience (Job titles, companies, durations)
        - Skills (technical, soft, etc.)
        - Projects
        - Certifications

        CV TEXT:
        {text}

        Return the result in JSON format with keys:
        ["personal_info", "education", "experience", "skills", "projects", "certifications"]
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


llm_client = LLMClient()
