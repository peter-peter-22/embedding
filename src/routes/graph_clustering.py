from fastapi import APIRouter,Response
from src.db import connect
import networkx as nx
from community import best_partition
import matplotlib.pyplot as plt
import matplotlib
from pyvis.network import Network

router = APIRouter()

# The weight of a like in an edge.
like_weight=0.1
# The weight of a follow in a edge.
follow_weight=1

# Generate user clusters and update the users.
@router.get("/clustering") 
def generateClusters():
    with connect() as conn:
        with conn.cursor() as cursor:
            # Commit database inserts automatically
            conn.autocommit=True

            # Create graph
            G = nx.DiGraph()

            # Add the nodes
            add_nodes(cursor,G)

            # Add the edges
            add_edges(cursor,G)

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
        
def add_edges(cursor,G):
    """
    Select the posts and likes as weighted edges and add them to the graph.

    Args:
        cursor (cursor): The DB cursor.
        G (DiGraph): The graph to edit.
    """

    # Select all follows and likes as weighted edges.
    cursor.execute("""
        WITH follow_edges AS (
        	SELECT 
        		"followerId" edge_start,
        		"followedId" edge_end,
        		%s weight
        	FROM follows
        ), like_edges AS (
        	SELECT
        		likes."userId" edge_start,
        		posts."userId" edge_end,
        		count(*) * %s weight
        	FROM likes
        	INNER JOIN posts ON likes."postId"=posts.id
        	GROUP BY edge_start, edge_end
        )
        SELECT 
        	edge_start,
        	edge_end,
        	sum(weight) weight
        FROM (
        	SELECT * from follow_edges
        	UNION ALL
        	SELECT * from like_edges
        )
        GROUP BY edge_start, edge_end
    """ % (follow_weight, like_weight))
    connection_edges = cursor.fetchall()

    # Add them to the graph.
    G.add_weighted_edges_from([(start,end,float(weight)) for start,end,weight in connection_edges])
    print("Connection edges: %s" % len(connection_edges))

def add_nodes(cursor,G):
    """
    Select the users and add them to the graph as nodes.

    Args:
        cursor (cursor): The DB cursor.
        G (DiGraph): The graph to edit.
    """

    # Select all users,
    cursor.execute("""
        SELECT id FROM users 
    """)

    # Get the user ids.
    users_nodes = [user[0] for user in cursor.fetchall()]
    
    # Add them to the graph.
    G.add_nodes_from(users_nodes)
    print("Calculating graph clustering for %s users." % len(users_nodes))
