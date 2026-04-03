from sklearn.cluster import KMeans
import numpy as np


def cluster_students(student_data):
    """
    student_data = [
        {
            "student": student_obj,
            "avg_marks": 78,
            "attendance": 90
        }
    ]
    """

    if len(student_data) < 2:
        return {
            "clusters": [],
            "counts": {}
        }

    X = np.array([
    [s["avg_marks"], s["attendance"]]
        for s in student_data
])

    # Dynamic cluster count
    n_clusters = min(3, len(student_data))

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X)

    cluster_names = {
        0: "Top Performers",
        1: "Average Students",
        2: "Needs Attention"
    }

    clustered_students = []
    counts = {
        "Top Performers": 0,
        "Average Students": 0,
        "Needs Attention": 0
    }

    for i, student in enumerate(student_data):
        cluster_name = cluster_names[labels[i]]

        clustered_students.append({
            "student": student["student"],
           "avg_marks": round(student["avg_marks"], 2),
           "attendance": round(student["attendance"], 2),
            "cluster": cluster_name
        })

        counts[cluster_name] += 1

    return {
        "clusters": clustered_students,
        "counts": counts
    }
