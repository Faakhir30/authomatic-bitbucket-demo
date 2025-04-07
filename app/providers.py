from authomatic.providers.oauth2 import OAuth2
from typing import Optional, Dict, Any
import httpx


class BitbucketOAuth2(OAuth2):
    """BitBucket Cloud OAuth 2.0 Provider Implementation"""

    user_authorization_url = "https://bitbucket.org/site/oauth2/authorize"
    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    user_info_url = "https://api.bitbucket.org/2.0/user"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_info_scope = ["account"]
        self.workspace = kwargs.get("workspace")

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Fetch user information from BitBucket API"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(self.user_info_url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_repositories(self, access_token: str) -> Dict[str, Any]:
        """Fetch repositories for the configured workspace"""
        if not self.workspace:
            raise ValueError("Workspace required for repository listing")

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}"
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_workspace_info(self, access_token: str) -> Dict[str, Any]:
        """Fetch workspace information"""
        if not self.workspace:
            raise ValueError("Workspace required")

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"https://api.bitbucket.org/2.0/workspaces/{self.workspace}"
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_user_permissions(self, access_token: str) -> Dict[str, Any]:
        """Fetch user permissions for the workspace"""
        if not self.workspace:
            raise ValueError("Workspace required for permissions check")

        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = (
                f"https://api.bitbucket.org/2.0/workspaces/{self.workspace}/permissions"
            )
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
