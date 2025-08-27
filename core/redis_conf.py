# Python packages
import os

# Redis
import redis.asyncio as redis

# Redis client setup
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)
