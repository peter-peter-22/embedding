from fastapi import APIRouter,Response
from src.db import connect
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import matplotlib.colors as colors

router = APIRouter()

# Visalize the social graph clusters with pyplot
@router.get("/visualize_clusters") 
def visualize_graph_clusters():
    with connect() as conn:
        with conn.cursor() as cursor:
            # Create the graph.
            G = nx.DiGraph()

            # Get the clusters.
            clusters = get_clusters(cursor)
            print("Fetched %s clusters." % len(clusters))

            # Add the clusters to the graph.
            clusters_to_graph(G, clusters)
            print("Added the clusters to the graph.")

            # Get the grouped connections between the clusters.
            edges = get_edges(cursor)
            print("Fetched %s edges." % len(edges))

            # Add the edges to the graph.
            edges_to_graph(G,edges)
            print("Added the edges to the graph.")

            # Calculate the positions of the nodes
            calculate_node_positions(G,clusters)
            print("Node positions calculated.")

            # Display the graph.
            display(G)
            print("File saved.")

            # End
            return Response(status_code=200)
        
def get_clusters(cursor):
    """
    Fetch the user clusters and their metadata.

    Args:
        cursor (cursor): The database cursor.

    Returns:
        (clusterId (int), member_interests (int), member_count (int), name (string))[]
    """

    cursor.execute("""
        WITH formatted_users AS (
        	SELECT "clusterId", COALESCE(interests[1],'null') AS interest 
        	FROM users
        ), sub_groups AS (
        	SELECT "clusterId", interest, count(*) 
        	FROM formatted_users
        	GROUP BY "clusterId", interest
        ), groups AS (
        	SELECT 
        		"clusterId", 
        		SUM(count) AS member_count, 
        		array_agg(json_build_object('name',interest,'count',count)) AS member_interests
        	FROM sub_groups
        	GROUP BY "clusterId"
        )
        SELECT 
        	"clusterId",
        	member_interests,
        	member_count,
        	(	
        		SELECT interest 
        	 	FROM sub_groups 
        		WHERE sub_groups."clusterId" = groups."clusterId"
        		ORDER BY sub_groups.count DESC
        		limit 1
        	) AS name
        FROM groups 
    """)
    return cursor.fetchall()        

def clusters_to_graph(G,clusters):
    """
    Add the clusters to the graph as nodes.

    Args:
        G (DiGraph): The graph to edit.
        clusters: The clusters and their metadata.
    """

    # Define a colormap for the nodes
    node_cmap = plt.cm.get_cmap('tab20', len(clusters))

    # Add each cluster to the graph as nodes.
    for i, cluster in enumerate(clusters):
        cluster_id, members_interests, member_count, name = cluster
        # List the interests of the members.
        interests_summary="\n".join([" - %s: %s" % (row.get("name"), row.get("count")) for row in members_interests])
        G.add_node(
            cluster_id, 
            label=name, 
            size=member_count, # The member count defines the group size.
            title="""Members: %s,
            Interests:
            %s""" % (member_count, interests_summary), 
            color=colors.rgb2hex(node_cmap(i)) # Unique color.
        )

def get_edges(cursor):
    """
    Fetch the grouped connections between the clusters.

    Args:
        cursor (cursor): The database cursor.

    Returns:
        (edge_from (int), edge_to (int), count (int))[]
    """

    cursor.execute("""
        SELECT follower."clusterId" edge_from, followed."clusterId" edge_to, count(follows)
        FROM follows
        INNER JOIN users follower ON follower.id=follows."followerId"
        INNER JOIN users followed ON followed.id=follows."followedId"
        GROUP BY followed."clusterId", follower."clusterId"
    """)
    return cursor.fetchall()

def edges_to_graph(G,edges):
    """
    Add the edges to the graph.

    Args:
        G (DiGraph): The graph to edit.
        edges: The edges and their metadata.
    """

    # Get the max weight
    biggest_edge = max(edges, key=lambda x: x[2])
    max_weight=biggest_edge[2]

    # Create the colormap of the edges.
    edge_cm= plt.cm.get_cmap('RdYlGn')

    # Add the edges to the graph
    for follow in edges:
        edge_from, edge_to, count = follow
        G.add_edge(edge_from, edge_to, title=str(count), color=colors.rgb2hex(edge_cm(count/max_weight)))

def calculate_node_positions(G, clusters):
    """
    Add the clusters to the graph as nodes.

    Args:
        G (DiGraph): The graph to edit.
        clusters: The clusters and their metadata.
    """

    # Get the largest size, to define the spacing between the nodes.  
    largest_group=max(clusters, key=lambda x: x[2])
    largest_size=float(largest_group[2])

    # Multiplier of the space between the nodes.
    space=10*largest_size

    # Calculate the positions.
    pos = nx.spring_layout(G,scale=space)

    # Apply the positions to the nodes.
    for node in G.nodes:
        x, y = pos[node] # Get the position from spring_layout.
        nodeData=G.nodes[node]
        nodeData["x"]=x
        nodeData["y"]=y

def display(G):
    """
    Display the graph with pyvis.

    Args:
        G (DiGraph): The graph to display.
    """
    # Create the network
    net = Network(height="750px", width="100%", directed=True, notebook=False)

    # Apply the graph.
    net.from_nx(G)

    # Prevent unnecessary movement.
    net.toggle_physics(False)

    # Make the edges curved, to prevent them from covering each other.
    net.set_edge_smooth("continuous")

    # Save
    net.save_graph('visuals/clusters.html')
