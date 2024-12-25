from __future__ import annotations

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from api import blobs
from api.services.discord import DiscordAPI
from api.services.discord import DiscordInfo
from api.services.spotify import SpotifyAPI
from api.services.spotify import SpotifyInfo

app = FastAPI()
templates = Jinja2Templates(directory="api/templates")

spotify = SpotifyAPI()
discord = DiscordAPI()


@app.route("/")
async def root():
    return {"status": ":3"}


@app.route("/spotify")
def spotify_info(request: Request) -> HTMLResponse:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = templates.TemplateResponse(
        request=request,
        name="spotify.svg",
        context={"current_info": current_info},
    )

    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp


@app.route("/spotify-lite")
def spotify_info(request: Request) -> HTMLResponse:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = templates.TemplateResponse(
        request=request,
        name="spotify_lite.svg",
        context={"current_info": current_info},
    )

    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp


@app.route("/discord")
def discord_info(request: Request) -> HTMLResponse:
    current_info: DiscordInfo = discord.get_current_info()

    resp = templates.TemplateResponse(
        request=request,
        name="discord.svg",
        context={"current_info": current_info, "blobs": blobs},
    )
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp


@app.route("/spotify.json")
def spotify_info_json() -> SpotifyInfo:
    current_info: SpotifyInfo = spotify.get_current_info()
    return current_info.data


@app.route("/discord.json")
def discord_info_json() -> DiscordInfo:
    current_info: DiscordInfo = discord.get_current_info()
    return current_info.data
