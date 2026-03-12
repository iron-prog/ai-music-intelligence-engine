from sklearn.cluster import KMeans
import numpy as np

from backend.features.feature_builder import build_user_features


def classify_listening_behavior():

    features = build_user_features()

    if features is None:
        print("\nListening Behavior Analysis")
        print("No listening data available")
        return

    X = np.array([[
        features["exploration_rate"],
        features["artist_loyalty"],
        features["night_ratio"]
    ]])

    # Predefined centroids (simulated users)
    training_data = np.array([
        [0.8, 0.1, 0.2],  # Explorer
        [0.2, 0.7, 0.1],  # Artist Loyalist
        [0.4, 0.2, 0.8],  # Night Listener
        [0.4, 0.3, 0.3],  # Balanced
    ])

    model = KMeans(n_clusters=4, random_state=42)
    model.fit(training_data)

    cluster = model.predict(X)[0]

    styles = {
        0: "Explorer",
        1: "Artist Loyalist",
        2: "Night Listener",
        3: "Balanced Listener"
    }

    print("\nListening Behavior Analysis")
    print("---------------------------")

    print("Listening Style:", styles.get(cluster, "Unknown"))
    print("Cluster ID:", cluster)

    print("\nFeature Summary")
    print("Exploration Rate:", round(features["exploration_rate"], 2))
    print("Artist Loyalty:", round(features["artist_loyalty"], 2))
    print("Night Listening Ratio:", round(features["night_ratio"], 2))