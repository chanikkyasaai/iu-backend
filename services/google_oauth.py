import httpx
from urllib.parse import urlencode
from utils import google_config


def get_google_auth_url():
    params = {
        "client_id": google_config.GOOGLE_CLIENT_ID,
        "redirect_uri": google_config.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    query_string = urlencode(params)
    return f"{google_config.GOOGLE_AUTH_URL}?{query_string}"


async def exchange_code_for_token(code: str):
    data = {
        "code": code,
        "client_id": google_config.GOOGLE_CLIENT_ID,
        "client_secret": google_config.GOOGLE_CLIENT_SECRET,
        "redirect_uri": google_config.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(google_config.GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()


async def get_user_info(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(google_config.GOOGLE_USERINFO_URL, headers=headers)
        response.raise_for_status()
        return response.json()
