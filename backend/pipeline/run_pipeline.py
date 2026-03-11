from backend.ingestion.spotify_ingest import fetch_recent_tracks
from backend.analytics.session_detection import detect_sessions
from backend.analytics.discovery_analytics import discovery_stats


def run():

    print("\nStarting Music Intelligence Pipeline\n")

    tracks = fetch_recent_tracks()

    print("Tracks ingested:", len(tracks))

    sessions = detect_sessions(tracks)

    print("Sessions detected:", len(sessions))

    discovery_stats()

    print("\nPipeline completed successfully")


if __name__ == "__main__":
    run()