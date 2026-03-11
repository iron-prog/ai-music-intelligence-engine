from backend.ingestion.spotify_ingest import run_ingestion
from backend.analytics.session_detection import detect_sessions
from backend.analytics.discovery_analytics import discovery_stats
from backend.analytics.listening_patterns import listening_patterns
from backend.analytics.mood_analysis import mood_analysis

def run():

    print("\nStarting Music Intelligence Pipeline\n")

    tracks = run_ingestion()

    print("Tracks ingested:", len(tracks))

    detect_sessions(tracks)

    discovery_stats()

    listening_patterns()

    mood_analysis()

    print("\nPipeline completed")


if __name__ == "__main__":
    run()