from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from authomatic import Authomatic
from authomatic.adapters import BaseAdapter
import aioredis
import json
import secrets
from typing import Optional, Dict, Any

from .config import get_settings, OAUTH_CONFIG
from .routes import router as api_router
from .session import (
    get_session,
    save_session,
    init_redis_pool,
    close_redis_pool,
    get_redis,
)

app = FastAPI(title="BitBucket OAuth Migration Demo")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(api_router)

# Initialize Authomatic
authomatic = Authomatic(OAUTH_CONFIG, get_settings().secret_key)


@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection pool on startup"""
    init_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection pool on shutdown"""
    await close_redis_pool()


class FastAPIAdapter(BaseAdapter):
    """Adapter for using Authomatic with FastAPI"""

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response
        self._url = str(request.url)
        self._cookies = {}

    async def get_response(self) -> Response:
        return self.response

    async def save_response(self, response: Response):
        self.response = response

    async def write(self, content: str):
        """Write content to response"""
        self.response.body = content.encode("utf-8")

    async def set_header(self, key: str, value: str):
        """Set response header"""
        self.response.headers[key] = value

    async def set_status(self, status: int):
        """Set response status code"""
        self.response.status_code = status


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Home page with login options"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login/{provider}")
async def login(
    provider: str,
    request: Request,
    response: Response,
    redis: aioredis.Redis = Depends(get_redis),
):
    """Handle OAuth login for both legacy and modern BitBucket"""
    if provider not in OAUTH_CONFIG:
        raise HTTPException(status_code=404, detail="Provider not found")

    adapter = FastAPIAdapter(request, response)
    result = authomatic.login(adapter, provider)

    if result:
        if result.error:
            raise HTTPException(status_code=400, detail=result.error.message)

        if result.user:
            result.user.update()
            user_data = {
                "id": result.user.id,
                "name": result.user.name,
                "email": result.user.email,
                "provider": provider,
                "access_token": result.user.access_token,
            }

            await save_session(response, user_data, redis)
            return RedirectResponse(url="/dashboard", status_code=303)

    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session: Dict[str, Any] = Depends(get_session)):
    """Dashboard showing BitBucket data"""
    if not session:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": session}
    )
