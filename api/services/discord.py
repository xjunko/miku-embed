from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class DiscordInfo:
    data: dict[str, Any]

    @property
    def user(self) -> dict[str, Any]:
        return self.data["discord_user"]

    @property
    def status(self) -> str:
        return {
            "online": "Online",
            "idle": "Idle",
            "dnd": "Do not Disturb",
            "offline": "Offline",
        }[self.data["discord_status"]]

    @property
    def color(self) -> str:
        color_rgb: tuple[int, int, int] = {
            "online": (0, 255, 0),
            "idle": (255, 255, 25),
            "dnd": (255, 0, 0),
            "offline": (255, 128, 128),
        }[self.data["discord_status"]]

        return "#{:02x}{:02x}{:02x}".format(*color_rgb)

    @property
    def description(self) -> str:
        return "Currently online"

    @property
    def name(self) -> str:
        return self.user["display_name"]

    @property
    def avatar(self) -> str:
        return f"https://cdn.discordapp.com/avatars/{self.user['id']}/{self.user['avatar']}.png?size=128"


class DiscordAPI:
    LANYARD_API: str = "https://api.lanyard.rest/v1/users/"

    def __init__(self) -> None:
        self.discord_id: int = os.getenv("DISCORD_ID")

    def get_current_info(self) -> DiscordInfo:
        with requests.Session() as sess:
            with sess.get(DiscordAPI.LANYARD_API + str(self.discord_id)) as res:
                if not res or res.status_code != 200:
                    return DiscordInfo(data={})

                return DiscordInfo(data=res.json()["data"])
