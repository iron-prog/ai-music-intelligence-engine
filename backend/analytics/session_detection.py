from backend.db.database import get_connection
from datetime import timedelta


SESSION_GAP = timedelta(minutes=30)


def get_listens():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT track_name, artist_name, played_at
        FROM listening_events
        ORDER BY played_at
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def detect_sessions(listens):

    sessions = []
    current_session = []

    last_time = None

    for track_name, artist_name, played_at in listens:

        if last_time is None:
            current_session.append((track_name, artist_name, played_at))
        else:
            gap = played_at - last_time

            if gap > SESSION_GAP:
                sessions.append(current_session)
                current_session = []

            current_session.append((track_name, artist_name, played_at))

        last_time = played_at

    if current_session:
        sessions.append(current_session)

    return sessions


def main():
    listens = get_listens()

    sessions = detect_sessions(listens)

    for i, session in enumerate(sessions, start=1):
        print(f"\nSession {i}")

        for track in session:
            print(track)


if __name__ == "__main__":
    main()