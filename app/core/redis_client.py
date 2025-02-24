import json

import redis

from app.core.config import settings


class BaseRedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True  # so Redis returns strings not bytes
        )

    def get(self, key: str, pepper_key: bytes = None) -> dict:
        """
        Retrieve the value for a given key from Redis.
        """
        value = self.redis_client.get(key)
        if value is None:
            context = {
                "history": [],
                "last_result": None,
            }
            # Save immediately so it exists in Redis
            self.set(key, json.dumps(context))
            return context
        return json.loads(value)

    def set(self, key: str, value: str) -> None:
        """
        Set or update a value for a given key in Redis.
        """
        self.redis_client.set(key, value, ex=settings.CONVERSATION_TTL)

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair from Redis. Returns True if deleted, False if the key does not exist.
        """
        result = self.redis_client.delete(key)
        return result > 0


redis_service = BaseRedisService()
