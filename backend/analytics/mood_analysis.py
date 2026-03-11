import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from statistics import mean


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
            scope=scope,
            open_browser=False
        )
    )


def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def mood_analysis():

    sp = get_spotify_client()

    results = sp.current_user_recently_played(limit=50)

    track_ids = []

    for item in results["items"]:

        track = item["track"]

        if track and track["id"]:
            track_ids.append(track["id"])

    # remove duplicates
    track_ids = list(set(track_ids))

    features = []

    # batch requests (Spotify safe)
    for chunk in chunk_list(track_ids, 20):

        try:
            audio = sp.audio_features(chunk)

            if audio:
                features.extend(audio)

        except Exception as e:
            print("Spotify audio feature request failed:", e)

    energy = []
    valence = []
    danceability = []

    for f in features:

        if not f:
            continue

        energy.append(f["energy"])
        valence.append(f["valence"])
        danceability.append(f["danceability"])

    print("\nMood Analysis")
    print("-------------")

    if not energy:
        print("Audio features unavailable from Spotify API")
        return

    avg_energy = round(mean(energy), 2)
    avg_valence = round(mean(valence), 2)
    avg_danceability = round(mean(danceability), 2)

    print("Average Energy:", avg_energy)
    print("Average Valence:", avg_valence)
    print("Average Danceability:", avg_danceability)

    if avg_valence > 0.6:
        mood = "Happy / Positive"
    elif avg_valence > 0.4:
        mood = "Balanced"
    else:
        mood = "Calm / Melancholic"

    print("Overall Listening Mood:", mood)