from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from .session import get_session
from .providers import BitbucketOAuth2
from .config import get_settings

router = APIRouter(prefix="/api")


@router.get("/repositories")
async def get_repositories(session: Dict[str, Any] = Depends(get_session)):
    """Get repositories for the authenticated user's workspace"""
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session["provider"] != "bitbucket_modern":
        raise HTTPException(status_code=400, detail="Only available for OAuth 2.0")

    provider = BitbucketOAuth2(workspace=get_settings().bb_workspace)
    repositories = await provider.get_repositories(session["access_token"])
    return repositories


@router.get("/workspace")
async def get_workspace(session: Dict[str, Any] = Depends(get_session)):
    """Get workspace information"""
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session["provider"] != "bitbucket_modern":
        raise HTTPException(status_code=400, detail="Only available for OAuth 2.0")

    provider = BitbucketOAuth2(workspace=get_settings().bb_workspace)
    workspace = await provider.get_workspace_info(session["access_token"])
    return workspace


@router.get("/permissions")
async def get_permissions(session: Dict[str, Any] = Depends(get_session)):
    """Get user permissions for the workspace"""
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session["provider"] != "bitbucket_modern":
        raise HTTPException(status_code=400, detail="Only available for OAuth 2.0")

    provider = BitbucketOAuth2(workspace=get_settings().bb_workspace)
    permissions = await provider.get_user_permissions(session["access_token"])
    return permissions
