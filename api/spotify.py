from __future__ import annotations

import json
import os
from base64 import b64encode
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import find_dotenv
from dotenv import load_dotenv

from api import blobs


def ms_to_formatted_minutes(millis: int) -> str:
    seconds = millis / 1000
    minutes = seconds / 60
    formatted_time = f"{int(minutes):02}:{int(seconds % 60):02}"
    return formatted_time


@dataclass
class SpotifyInfo:
    data: dict[str, Any]

    @property
    def item(self) -> dict[str, Any]:
        if not "is_playing" in self.data:
            return self.data["items"][0]["track"]

        return self.data["item"]

    @property
    def playing(self) -> bool:
        return "is_playing" in self.data

    @property
    def artist_name(self) -> str:
        return self.item["artists"][0]["name"]

    @property
    def artist_url(self) -> str:
        return self.item["artists"][0]["external_urls"]["spotify"]

    @property
    def song_name(self) -> str:
        return self.item["name"]

    @property
    def song_url(self) -> str:
        return self.item["external_urls"]["spotify"]

    @property
    def cover(self) -> str:
        try:  # Edgecase: Playing ads
            if len(self.item["album"]["images"]) == 0:
                return blobs.PLACEHOLDER_IMAGE
        except:
            return blobs.PLACEHOLDER_IMAGE

        return b64encode(
            requests.get(self.item["album"]["images"][1]["url"]).content,
        ).decode("ascii")

    @property
    def progress(self) -> int:
        return self.data["progress_ms"]

    @property
    def duration(self) -> int:
        return self.item["duration_ms"]

    @property
    def progress_formatted(self) -> str:
        return (
            ms_to_formatted_minutes(self.progress)
            + "/"
            + ms_to_formatted_minutes(self.duration)
        )


class SpotifyAPI:
    REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
    RECENTLY_PLAYING_URL = (
        "https://api.spotify.com/v1/me/player/recently-played?limit=10"
    )

    def __init__(self) -> None:
        load_dotenv(find_dotenv())

        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.secret_id = os.getenv("SPOTIFY_SECRET_ID")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        self._token = ""

    @property
    def auth(self) -> str:
        return b64encode(f"{self.client_id}:{self.secret_id}".encode()).decode("ascii")

    @property
    def token(self) -> str:
        if not self._token:
            response = requests.post(
                SpotifyAPI.REFRESH_TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                },
                headers={"Authorization": f"Basic {self.auth}"},
            ).json()

            if "access_token" in response:
                self._token = response["access_token"]
            else:
                raise RuntimeError("Failed to get token from spotify API!")

        return self._token

    def get_data(self, endpoint: str) -> dict[str, Any]:
        with requests.Session() as sess:
            with sess.get(
                endpoint,
                headers={"Authorization": f"Bearer {self.token}"},
            ) as res:
                if res.status_code == 204:
                    return None  # No data returned.
                elif res.status_code == 401:
                    # Invalid token, do this request again.
                    self._token = ""
                    return self.get_data(endpoint)
                else:
                    return res.json()

    def get_current_info(self) -> SpotifyInfo:
        for endpoint in [SpotifyAPI.NOW_PLAYING_URL, SpotifyAPI.RECENTLY_PLAYING_URL]:
            if data := self.get_data(endpoint):
                open("data.json", "w").write(json.dumps(data))
                return SpotifyInfo(data=data)
        else:
            print("Failure to get data.")
