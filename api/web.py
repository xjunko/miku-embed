from __future__ import annotations

from flask import Flask
from flask import render_template
from flask import Response

from api import blobs
from api.services.discord import DiscordAPI
from api.services.discord import DiscordInfo
from api.services.spotify import SpotifyAPI
from api.services.spotify import SpotifyInfo

app = Flask(__name__)

spotify = SpotifyAPI()
discord = DiscordAPI()


@app.route("/")
def index() -> Response:
    return {"status": ":3"}


@app.route("/spotify")
def spotify_info() -> Response:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = Response(
        render_template("spotify.svg", current_info=current_info),
        mimetype="image/svg+xml",
    )

    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp


@app.route("/spotify-lite")
def spotify_lite_info() -> Response:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = Response(
        render_template("spotify_lite.svg", current_info=current_info),
        mimetype="image/svg+xml",
    )

    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp

@app.route("/spotify-lite-white")
def spotify_lite_white_info() -> Response:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = Response(
        render_template("spotify_lite_white.svg", current_info=current_info),
        mimetype="image/svg+xml",
    )

    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp



@app.route("/discord")
def discord_info() -> Response:
    current_info: DiscordInfo = discord.get_current_info()

    resp = Response(
        render_template("discord.svg", current_info=current_info, blobs=blobs),
        mimetype="image/svg+xml",
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
