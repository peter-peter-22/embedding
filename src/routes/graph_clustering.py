from fastapi import APIRouter,Response
from src.db import connect
import networkx as nx
from community import best_partition
import matplotlib.pyplot as plt
import matplotlib
from pyvis.network import Network

router = APIRouter()

# Generate user clusters and update the users.
@router.get("/clustering") 
def generateClusters():
    with connect() as conn:
        with conn.cursor() as cursor:
            # Commit database inserts automatically
            conn.autocommit=True
            # Create graph
            G = nx.DiGraph()

            # Select all users and insert their ids into the graph as nodes
            cursor.execute("""
                SELECT id FROM users 
            """)
            users_nodes = [user[0] for user in cursor.fetchall()]
            G.add_nodes_from(users_nodes)
            print("Calculating graph clustering for %s users." % len(users_nodes))

            # Select all follows and insert them into the graph as edges
            cursor.execute("""
                SELECT "followerId", "followedId"
                FROM follows
            """)
            follow_edges = cursor.fetchall()
            G.add_edges_from(follow_edges,weight=1)
            print("Follow edges: %s" % len(follow_edges))

            # @todo add likes

            # Calculate the clustering
            partition = best_partition(G.to_undirected(),resolution=2.5)  # Louvain works on undirected graphs
            clusters = [(id,) for id in set(partition.values())]
            print("Created %s partitions." % len(clusters))

            # Delete previous clusters
            cursor.execute("DELETE FROM clusters")

            # Insert new clusters
            cursor.executemany("INSERT INTO clusters (id) VALUES (%s)",clusters)

            # Update the cluster id of the users
            cursor.executemany("""
                UPDATE users
                SET "clusterId" = %s
                WHERE id = %s
            """,
            [(cluster_id, node) for node, cluster_id in partition.items()]
            )

            # End
            return Response(status_code=200)