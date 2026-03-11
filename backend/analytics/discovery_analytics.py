from backend.db.database import get_connection


def get_listens():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT track_name, artist_name, played_at
        FROM listening_events
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def discovery_stats():

    listens = get_listens()

    artists = set()
    tracks = set()

    for track, artist, _ in listens:
        artists.add(artist)
        tracks.add(track)

    print("\nDiscovery Analytics")
    print("-------------------")
    print("Total listens:", len(listens))
    print("Unique artists:", len(artists))
    print("Unique tracks:", len(tracks))


def top_artists():

    listens = get_listens()

    counts = {}

    for _, artist, _ in listens:
        counts[artist] = counts.get(artist, 0) + 1

    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\nTop Artists")
    print("-----------")

    for artist, count in top:
        print(artist, ":", count)


def main():

    discovery_stats()
    top_artists()


if __name__ == "__main__":
    main()