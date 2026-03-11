import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from backend.db.database import get_connection

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

scope = "user-read-recently-played"

def insert_listen(track):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO listening_events (track_name, artist_name, album_name, played_at)
        VALUES (%s, %s, %s, %s)
        """,
        (
            track["track_name"],
            track["artist"],
            track["album"],
            track["played_at"]
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

results = sp.current_user_recently_played(limit=49)

for item in results['items']:
    track = item['track']

    data = {
        "track_name": track['name'],
        "artist": track['artists'][0]['name'],
        "album": track['album']['name'],
        "played_at": item['played_at']
    }

    insert_listen(data)