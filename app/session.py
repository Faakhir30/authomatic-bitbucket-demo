from fastapi import Request, Response, HTTPException, Depends
from typing import Dict, Any, Optional
import json
import secrets
import aioredis

from .config import get_settings

# Redis connection pool
redis_pool = None


def init_redis_pool():
    """Initialize Redis connection pool"""
    global redis_pool
    if not redis_pool:
        redis_pool = aioredis.ConnectionPool.from_url(
            get_settings().redis_url, decode_responses=True
        )
    return redis_pool


async def close_redis_pool():
    """Close Redis connection pool"""
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()
        redis_pool = None


async def get_redis():
    """Get Redis connection from pool"""
    pool = init_redis_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Redis not initialized")
    return aioredis.Redis(connection_pool=pool)


async def get_session(
    request: Request, redis: aioredis.Redis = Depends(get_redis)
) -> Dict[str, Any]:
    """Get session data from Redis"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {}

    data = await redis.get(f"session:{session_id}")
    return json.loads(data) if data else {}


async def save_session(
    response: Response,
    session_data: Dict[str, Any],
    redis: aioredis.Redis = Depends(get_redis),
    session_id: Optional[str] = None,
) -> None:
    """Save session data to Redis"""
    if not session_id:
        session_id = secrets.token_urlsafe(32)
        response.set_cookie(
            "session_id",
            session_id,
            httponly=True,
            secure=not get_settings().debug,
            samesite="lax",
        )

    await redis.setex(
        f"session:{session_id}", 3600, json.dumps(session_data)  # 1 hour expiration
    )
