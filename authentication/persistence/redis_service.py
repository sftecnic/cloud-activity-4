# authentication/persistence/redis_service.py
import os
import redis

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True
        )

    def set_token(self, token: str, user_id: str, expire: int = 3600):
        return self.redis_client.setex(token, expire, user_id)

    def get_user_id(self, token: str):
        return self.redis_client.get(token)

    def delete_token(self, token: str):
        return self.redis_client.delete(token)
