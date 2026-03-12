from collections import Counter
from backend.db.database import get_connection


def compute_discovery_intelligence():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT track_name, artist_name
        FROM listening_events
    """)

    rows = cursor.fetchall()

    total_listens = len(rows)

    if total_listens == 0:
        print("\nDiscovery Intelligence\nNo listening data available.")
        return

    artist_counts = Counter()
    track_counts = Counter()

    for track, artist in rows:
        artist_counts[artist] += 1
        track_counts[track] += 1

    unique_artists = len(artist_counts)
    unique_tracks = len(track_counts)

    new_artist_listens = sum(1 for c in artist_counts.values() if c == 1)
    repeat_artist_listens = total_listens - new_artist_listens

    exploration_rate = new_artist_listens / total_listens
    repeat_rate = repeat_artist_listens / total_listens

    top_artist, top_count = artist_counts.most_common(1)[0]

    loyalty_score = top_count / total_listens
    discovery_score = unique_artists / total_listens

    print("\nDiscovery Intelligence")

    print(f"Exploration Rate: {exploration_rate:.2f}")
    print(f"Repeat Rate: {repeat_rate:.2f}")
    print(f"Discovery Score: {discovery_score:.2f}")
    print(f"Top Artist: {top_artist}")
    print(f"Artist Loyalty Score: {loyalty_score:.2f}")

    cursor.close()
    conn.close()