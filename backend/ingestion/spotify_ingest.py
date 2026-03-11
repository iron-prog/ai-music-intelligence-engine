import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime

from backend.db.database import get_connection
from backend.models.listen import Listen


load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

scope = "user-read-recently-played"


def get_spotify_client():

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope
        )
    )


def fetch_recent_tracks():

    sp = get_spotify_client()

    results = sp.current_user_recently_played(limit=50)

    tracks = []

    for item in results["items"]:

        track = item["track"]

        played_at = datetime.fromisoformat(
            item["played_at"].replace("Z", "+00:00")
        )

        listen = Listen(
            track_name=track["name"],
            artist_name=track["artists"][0]["name"],
            album_name=track["album"]["name"],
            played_at=played_at
        )

        tracks.append(listen)

    return tracks


def run_ingestion():

    tracks = fetch_recent_tracks()

    conn = get_connection()
    cursor = conn.cursor()

    for track in tracks:

        cursor.execute(
            """
            INSERT INTO listening_events (track_name, artist_name, album_name, played_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                track.track_name,
                track.artist_name,
                track.album_name,
                track.played_at
            )
        )

    conn.commit()
    cursor.close()
    conn.close()

    return tracks


if __name__ == "__main__":
    run_ingestion()