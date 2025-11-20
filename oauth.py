import requests
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

BASE_URL = "https://discord.com/api/v10"


def exchange_code(code: str):
    """Turns OAuth code into access_token"""
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(f"{BASE_URL}/oauth2/token", data=data, headers=headers)
    return r.json()


def get_user(token: str):
    """Fetches user information"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/users/@me", headers=headers)
    return r.json()


def get_guilds(token: str):
    """Fetches guilds the user is in"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/users/@me/guilds", headers=headers)
    return r.json()
