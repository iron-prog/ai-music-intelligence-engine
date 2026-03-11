from backend.db.database import get_connection
from collections import Counter


def listening_patterns():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT artist_name, played_at
        FROM listening_events
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    artist_counts = Counter()
    hour_counts = Counter()

    for artist, played_at in rows:

        artist_counts[artist] += 1
        hour_counts[played_at.hour] += 1

    print("\nListening Patterns")
    print("------------------")

    print("Top Artists:")
    for artist, count in artist_counts.most_common(5):
        print(artist, count)

    print("\nMost Active Listening Hour:")
    hour, count = hour_counts.most_common(1)[0]
    print(hour, ":00 with", count, "listens")