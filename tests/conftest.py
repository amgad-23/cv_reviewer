import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import SessionLocal, Base, engine
import redis.asyncio as redis
from unittest.mock import AsyncMock


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create and drop tables for tests"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """Provides FastAPI test client"""
    return TestClient(app)


@pytest.fixture()
def db_session():
    """Provides a test database session"""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture()
def mock_redis():
    """Mocks Redis connection for rate limiting and chatbot storage"""
    redis_mock = AsyncMock()
    redis_mock.get.return_value = None  # Default to "not found" in Redis
    return redis_mock
