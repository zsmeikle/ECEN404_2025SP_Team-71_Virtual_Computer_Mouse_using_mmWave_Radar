import numpy as np
from sklearn.cluster import KMeans

# Step 1: Generate a random array of points
np.random.seed(42)  # For reproducibility
data = np.random.rand(100, 2)  # 100 points in 2D space

# Step 2: Apply K-Means clustering
k = 2  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(data)

# Step 3: Get cluster labels and compute mean of each cluster
labels = kmeans.labels_
cluster_means = {}

for i in range(k):
    cluster_points = data[labels == i]  # Select points belonging to cluster i
    cluster_mean = np.mean(cluster_points, axis=0)  # Compute mean
    cluster_means[i] = {"mean": cluster_mean, "selected_points": None}

# Step 4: Select all points that are "close" to the cluster mean
selected_points = {}
threshold_factor = 0.5  # Adjust as needed to control the selection range

for i in range(k):
    mean = cluster_means[i]["mean"]
    cluster_points = data[labels == i]  # Get points in the cluster
    distances = np.linalg.norm(cluster_points - mean, axis=1)
    
    # Define threshold based on a percentage of max distance in cluster
    threshold = threshold_factor * np.max(distances)
    
    # Select points that are within the threshold distance from the mean
    close_points = cluster_points[distances <= threshold]
    cluster_means[i]["selected_points"] = close_points
    selected_points[i] = close_points  # Store in dictionary

# Output
for cluster, points in selected_points.items():
    print(f"Cluster {cluster} selected points array:\n", points, "\n")