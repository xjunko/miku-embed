from __future__ import annotations

from flask import Flask
from flask import render_template
from flask import Response

from api import blobs
from api.services.discord import DiscordAPI
from api.services.discord import DiscordInfo
from api.services.spotify import SpotifyAPI
from api.services.spotify import SpotifyInfo


@app.route("/spotify")
def spotify_info() -> Response:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = Response(
        render_template("spotify.svg", current_info=current_info),
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
    return current_info


@app.route("/discord.json")
def discord_info_json() -> DiscordInfo:
    current_info: DiscordInfo = discord.get_current_info()
    return current_info
