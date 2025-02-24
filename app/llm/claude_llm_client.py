from app.core.config import settings
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from app.core.logger import module_logger


class ClaudeClient:
    def __init__(self):
        self.anthropic = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-v1"

    def analyze_cv_text(self, cv_text: str) -> str:
        # Construct a prompt using the anthropic style
        prompt = f"""
        {HUMAN_PROMPT} 
        You are a CV parser. Extract the following info in JSON format:
        ["personal_info", "education", "experience", "skills", "projects", "certifications"].

        CV TEXT:
        {cv_text}

        Return strictly in JSON format with the above keys.

        {AI_PROMPT}
        """
        try:
            response = self.anthropic.completions.create(
                model=self.model,
                max_tokens_to_sample=1000,
                prompt=prompt,
                temperature=0.2,
            )
        except Exception as e:
            module_logger.error(f"Error processing CV: {e}")
            return f'Error processing CV: {e}'
        return response.completion


claude_client = ClaudeClient()
