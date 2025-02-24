# CV Analysis Backend

A FastAPI backend for extracting structured information from resumes/CVs using OCR and an LLM (OpenAI GPT or Claude). It
also offers a simple chatbot interface to query the CV data.

## Features

- Upload PDF or Word documents
- Automatic text extraction (via PDF parsing and/or OCR)
- Structured CV parsing (via GPT or Claude)
- Database storage (SQLite by default)
- Query endpoints (search by skill, industry, etc.)
- Chatbot interface

## Requirements

- Python 3.8+
- [Tesseract OCR](path/to/tesseract)
- [OpenAI API key](https://beta.openai.com/signup/) or [Claude API key](https://claude.ai/)

## project structure

```
.
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── redis_client.py
│   ├── llm/
│   │   ├── claude_llm_client.py
│   │   ├── mimic_llm_client.py
│   │   └── openai_llm_client.py
│   ├── models/
│   │   ├── cv.py
│   ├── routers/
│   │   ├── chatbot.py
│   │   ├── query.py
│   │   ├── upload.py
│   ├── services/
│   │   ├── cv_query_service/
│   │   │   ├── __init__.py
│   │   │   ├── abstract_cv_query.py
│   │   │   └── mysq_cv_query.py
│   │   ├── __init__.py
│   │   ├── chatbot_service.py
│   │   ├── ocr_service.py
│   │   ├── parse_service.py
│   │   └── parse_user_intent.py
│   ├── tmp/
│   │   └── cv_files.pdf
│   ├── main.py
│   └── db.py
├── data/
│   ├── sample_cvs/
│   │   ├── cv1.pdf
│   │   ├── cv2.pdf
│   │   └── cv3.pdf
├── tests/
├── __init__.py
│   ├── test_unit/
│   │   ├── test_ocr.py
│   │   ├── test_llm.py
│   │   ├── test_parsing.py
│   ├── test_integration/
│   │   ├── test_upload.py
│   │   ├── test_query.py
│   │   ├── test_chatbot.py
│   ├── test_performance.py
│   ├── test_security.py
│   ├── test_error_handling.py
│   ├── test_rate_limit.py
│   ├── test_e2e.py
│   └── conftest.py
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourname/cv_analysis_backend.git
   cd cv_analysis_backend
    ```

## setup by python

### prerequisites
- install wsl (windows subsystem for linux) and install ubuntu 20.04 for redis server
```powershell
wsl --install
wsl --set-version Ubuntu-20.04 2
wsl -d Ubuntu-20.04
wsl.exe -d Ubuntu
```
```bash
sudo apt update
sudo apt install redis
redis-server --daemonize yes
```
for confirmation
```bash
redis-cli ping
```

2. **create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install the requirements**

   ```bash
    pip install -r requirements.txt
    ```
4. **Set the environment variables**
   create a .env file in the root directory and add the following variables:
   follow the .env.example file


6. **Run the server**

   ```bash
   uvicorn main:app --reload
   ```

## setup by docker

2. **Build the Docker image**

   ```bash
   docker build -t cv_analysis_backend .
   ```
3. **Run the Docker container**

   ```bash
    docker run -d -p 8000:8000 cv_analysis_backend
    ```
4. **Set the environment variables**
   create a .env file in the root directory and add the following variables:
   follow the .env.example file

## setup by docker-compose

2. **Run the Docker container**

   ```bash
    docker-compose up -d
    ```
3. **Set the environment variables**
   create a .env file in the root directory and add the following variables:
   follow the .env.example file
4. **Run by docker-compose**

   ```bash
    docker-compose up -d
    ```

## Usage

- The API documentation is available at `http://localhost:8000/swagger`.
- Upload a resume/CV document to extract text and parse the structured data at `http://localhost:8000/v1/upload-cv`.
- the Chatbot interface for querying CV information is available at `http://localhost:8000/v1/chatbot`.
- the base Chatbot interface for talking is available at `http://localhost:8000/v1/base-chatbot/`.
- the Chatbot interface for querying candidates with skill information is available
  at `http://localhost:8000/v1/candidates-with-skill`.
- the Chatbot interface for querying candidates experience in industry information is available
  at `http://localhost:8000/v1/experience-in-industry`.
- the Chatbot interface for querying matching candidates information is available
  at `http://localhost:8000/v1/match-candidates`.
- check on all cv queries at `http://localhost:8000/v1/all-cv-records`.
