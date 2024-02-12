from __future__ import annotations

from flask import Flask
from flask import render_template
from flask import Response

from api.spotify import SpotifyAPI
from api.spotify import SpotifyInfo

app = Flask(__name__)
spotify = SpotifyAPI()


@app.route("/")
def index() -> Response:
    current_info: SpotifyInfo = spotify.get_current_info()

    resp = Response(
        render_template("profile.svg", current_info=current_info),
        mimetype="image/svg+xml",
    )

    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp
