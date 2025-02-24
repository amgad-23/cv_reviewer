import os
from huggingface_hub import InferenceApi
from dotenv import load_dotenv

load_dotenv()


class HFInferenceClient:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.inference = InferenceApi(
            repo_id="tiiuae/falcon-7b-instruct",  # or any other instruct-capable model
            token=self.api_key
        )

    def analyze_cv_text(self, text: str) -> str:
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

        # InferenceApi usage can differ depending on the model
        # For generative text models:
        response = self.inference(prompt, max_length=300, temperature=0.3)
        return response  # often the raw text is in the returned object


# Usage example
if __name__ == "__main__":
    cv_text = "Jane Smith, phone 987-654-3210, Data Scientist at ACME, etc."
    hf_client = HFInferenceClient()
    parsed = hf_client.analyze_cv_text(cv_text)
    print(parsed)
