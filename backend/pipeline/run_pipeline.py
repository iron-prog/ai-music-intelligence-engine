from backend.ingestion.spotify_ingest import run_ingestion
from backend.analytics.session_detection import detect_sessions
from backend.analytics.discovery_analytics import discovery_stats
from backend.analytics.listening_patterns import listening_patterns
from backend.analytics.mood_analysis import mood_analysis
from backend.intelligence.discovery_engine import compute_discovery_intelligence
from backend.intelligence.habit_clustering import classify_listening_behavior

def run():

    print("\nStarting Music Intelligence Pipeline\n")

    tracks = run_ingestion()

    print("Tracks ingested:", len(tracks))

    detect_sessions(tracks)

    discovery_stats()

    listening_patterns()

    mood_analysis()

    compute_discovery_intelligence()

    classify_listening_behavior()

    print("\nPipeline completed")


if __name__ == "__main__":
    run()