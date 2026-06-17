import httpx
from urllib.parse import urlencode
from app.core.config import settings


class GitHubOAuth:
    AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_URL = "https://api.github.com/user"

    def build_authorize_url(self, state: str) -> str:
        params = urlencode({
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_REDIRECT_URI,
            "scope": "read:user",
            "state": state,
        })
        return f"{self.AUTHORIZE_URL}?{params}"

    async def exchange_code(self, code: str) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.TOKEN_URL,
                headers={"Accept": "application/json"},
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GITHUB_REDIRECT_URI,
                },
            )
        resp.raise_for_status()
        return resp.json()["access_token"]

    async def fetch_user(self, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self.USER_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                },
            )
        resp.raise_for_status()
        return resp.json()