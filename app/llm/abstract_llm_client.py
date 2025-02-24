from abc import ABC


class AbstractLLMClient(ABC):
    def analyze_cv_text(self, text: str) -> str:
        pass

    def analyze_user_query(self, user_message: str) -> dict:
        pass

