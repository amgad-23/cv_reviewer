import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY = ''
    ANTHROPIC_API_KEY = ''
    # data base
    DB_URL = ''
    # ocr
    TESSERACT_PATH = ''
    # redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    CONVERSATION_TTL = 3600
    REDIS_PASSWORD = None
    # logger
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE_PATH = 'app.json.log'

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", '.env')


settings = Settings()
