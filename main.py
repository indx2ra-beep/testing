from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from oauth import exchange_code, get_user, get_guilds
from config import CLIENT_ID, REDIRECT_URI

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login")
def login():
    url = (
        "https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=identify%20guilds"
    )
    return RedirectResponse(url)


@app.get("/oauth/callback")
def callback(request: Request, code: str):
    token_data = exchange_code(code)

    if "access_token" not in token_data:
        return {"error": "OAuth failed", "details": token_data}

    access_token = token_data["access_token"]

    user = get_user(access_token)
    guilds = get_guilds(access_token)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "guilds": guilds
        },
    )
