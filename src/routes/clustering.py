from fastapi import APIRouter,Response
from src.db import db
from sklearn.cluster import KMeans
import ast

router = APIRouter(prefix="/clustering")

# 
@router.get("/") 
def generateClusters():
     with db.cursor() as cursor:

        # Get the users and their embedding vectors
        cursor.execute("""
            SELECT id, embedding
            FROM users
            WHERE embedding IS NOT NULL
        """)
        users = cursor.fetchall()
        print("Calculating clusters for %s users." % len(users))

        # Create an array of embeddings for the k-means calculator
        # Convert their type from string to list
        embeddings=[ast.literal_eval(user[1]) for user in users]

        # Calculate the K-means clusters
        n_clusters = 20  
        kmeans = KMeans(n_clusters)
        cluster_labels = kmeans.fit_predict(embeddings)
        print("Created %s clusters." % len(kmeans.cluster_centers_))

        # Delete the previous clusters
        cursor.execute("TRUNCATE clusters CASCADE") 

        # Insert the new clusters
        cursor.executemany(
            "INSERT INTO clusters (id, centroid) VALUES (%s, %s)",
            [(index, vector.tolist()) for index, vector in enumerate(kmeans.cluster_centers_)]
        )

        # Update the cluster ids of the users
        cursor.executemany(
            """
                UPDATE users
                SET "clusterId" = %s
                WHERE id=%s
            """,
            [(clusterId.item(),users[userIndex][0]) for userIndex, clusterId in enumerate(cluster_labels)]
        )
        print("Updated the cluster id of %s users." % len(cluster_labels))

        # End
        return Response(status_code=200)