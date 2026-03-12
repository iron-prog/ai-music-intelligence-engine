from backend.db.database import get_connection
from collections import Counter
from datetime import datetime


def build_user_features():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT track_name, artist_name, played_at
        FROM listening_events
    """)

    rows = cursor.fetchall()

    total_listens = len(rows)

    if total_listens == 0:
        return None

    artist_counts = Counter()
    night_listens = 0

    for track, artist, played_at in rows:

        artist_counts[artist] += 1

        hour = played_at.hour

        if hour >= 22 or hour <= 5:
            night_listens += 1

    unique_artists = len(artist_counts)

    exploration_rate = unique_artists / total_listens

    top_artist_count = artist_counts.most_common(1)[0][1]

    artist_loyalty = top_artist_count / total_listens

    night_ratio = night_listens / total_listens

    cursor.close()
    conn.close()

    return {
        "exploration_rate": exploration_rate,
        "artist_loyalty": artist_loyalty,
        "night_ratio": night_ratio,
        "total_listens": total_listens
    }