import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


def get_auth_url():
    scope = "user-read-playback-state user-modify-playback-state playlist-modify-public"
    
    return (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={scope}"
        f"&redirect_uri={REDIRECT_URI}"
    )


def exchange_code_for_token(code: str):
    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    ).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    return response.json()

class SpotifyService:

    def __init__(self):
        self.access_token = None  # later replace with storage

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def play_song(self, song: str):
        track = self._search_song(song)
        if not track:
            return {"error": "Song not found"}

        requests.put(
            "https://api.spotify.com/v1/me/player/play",
            headers=self._headers(),
            json={"uris": [track["uri"]]}
        )

        return {
            "status": "playing",
            "track": track["name"],
            "artist": track["artist"]
        }

    def _search_song(self, query: str):
        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=self._headers(),
            params={
                "q": query,
                "type": "track",
                "limit": 1
            }
        )

        items = response.json()["tracks"]["items"]
        if not items:
            return None

        track = items[0]

        return {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "uri": track["uri"]
        }

    def pause(self):
        requests.put(
            "https://api.spotify.com/v1/me/player/pause",
            headers=self._headers()
        )
        return {"status": "paused"}

    def execute_tool(name: str, args: dict):
        if name not in AVAILABLE_TOOLS:
            return {"error": "Tool not allowed"}

        return AVAILABLE_TOOLS[name](**args)
