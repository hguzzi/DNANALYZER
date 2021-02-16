# Package for the creation, manipulation,
# and study of the structure, dynamics,
# and functions of complex networks.
# https://networkx.github.io/
import networkx as nx


def adjList(G):
    '''Builds the adjacency list of graph G, also considering the weights of the edges.
        Parameters: 
            - G: weighted and undirected graph.
        Returns:
            - Dictionary:
                - key -> name of node v;
                - value -> adjacency list of node v as a dictionary:
                                - key -> name of node that has an edge with node v;
                                - value -> weight of edge.
            Example: {1:{2:0.5}, 2:{1:0.5, 3:0.6}, 3:{2:0.2}}.'''

    adj = {}  # Initializes adjacency list
    # Iterates the edges of the graph
    for e in G.edges:
        # e => [node1, node2]

        # If the node1 is already present in the adjacency list
        if e[0] in adj.keys():
            # Adds the node2 with the weight of the edge
            adj[e[0]][e[1]] = G[e[0]][e[1]]['weight']

        # If the node1 is not yet present in the adjacency list
        else:
            # Adds the node2 with the weight of the edge
            adj[e[0]] = {e[1]: G[e[0]][e[1]]['weight']}

        # If the node2 is already present in the adjacency list
        if e[1] in adj.keys():
            # Adds the node1 with the weight of the edge
            adj[e[1]][e[0]] = G[e[1]][e[0]]['weight']

        # If the node2 is not yet present in the adjacency list
        else:
            # Adds the node1 with the weight of the edge
            adj[e[1]] = {e[0]: G[e[1]][e[0]]['weight']}

    # Returns the adjacency list
    return adj


def nodeVol(node):
    '''Calculates the vol of a node.
        Parameters:
            - node: adjacency list of node v as a dictionary:
                - key -> name of node that has an edge with node v;
                - value -> weight of edge.
        Returns: the vol of the node (the sum of the weights of the edges incident to node v).'''

    # Initialize the vol variable
    vol = 0.0

    # Iterate the node in adjacency list
    for j in node.keys():
        # Calculate the vol
        vol = vol+node[j]

    # Return the vol of node
    return vol


def density(adj):
    '''Calculate the density of the graph from its adjacency list.
        The density in this case is calculated as the sum of the vol of the nodes,
         divided by the number of nodes.
        Parameters:
            - adj: adjacency list of graph.
        Returns:
            - Density of a weighted graph.'''

    # Store in N the number of nodes from adj
    N = len(adj.keys())
    # Initialize sumvol
    sumVol = 0

    # Iterate the node in adj
    for i in adj.keys():
        # Calculate the vol of node i
        # sumVol += nodeVol(adj[i])
        for j in adj[i].keys():
            sumVol = sumVol+adj[i][j]

    # Return the density of the graph
    return sumVol/N


def minVolNode(adj):
    '''Use the adjacency list to find the node with the lowest vol.
    Parameters:
        - adj: adjacency list of graph.
    Returns:
        - name of node with loweset vol.'''

    # Initialize the minvol variable
    minvol = float('inf')
    # Initialize the "node" variable
    node = None

    # Iterates the node
    for i in adj.keys():
        # Calculates the vol of node i
        vol = nodeVol(adj[i])

        # Compare the current calculated vol with stored
        # If current vol is lower than stored
        if vol <= minvol:
            # Store current vol in minvol
            minvol = vol
            # Store the name of node in "node"
            node = i

    # Return the name of node
    return node


def removeNode(node, adj):
    '''Removes a node and all its adjacent edges from an adjacency list.   
    Parameters:
        - node: the name of node
        - adj: adjacency list of graph. 

    Returns:
        - updated adjacency list of graph.'''

    # Pop from adj the value from the key 'node'
    # and store in 'nDict'
    nDict = adj.pop(node)
    # Pop from adj the nodes contained in nDict
    for i in nDict.keys():
        adj[i].pop(node)

    # Return updated adjacency list
    return adj


def extractDCS(G):
    '''Extracts the DCS from a weighted  and undirected graph, with Charikar algorithm.
        Parameters:
            - graph: weighted and undirected graph.
        Returns:
            - dcs: subgraph induced on the nodes of the densest weight of the graph.'''

    
    adj = adjList(G)  # Builds the adjacency list
    current_density = 0  # In this case it is the initial comparison density
    new_density = density(adj)  # Calculates the density of G.

    # RECURSIVE step
    # Eliminates the node of the lowest degree until the density of the subgraph of G increases
    while(new_density >= current_density):
        current_density = new_density
        adj_backup = adj.copy()
        # Find node with minimum degree
        n = minVolNode(adj)
        # Removes node with minimum degree from adjacency list
        adj = removeNode(n, adj)
        # Calculate the new density
        new_density = density(adj)

        # print("Previous iteration density: ", current_density,
        #       "--> Current iteration density: ", new_density)

        # Compare the current density with the maximum stored density
        if new_density < current_density:
            # The current desity is the new maximum density
            adj = adj_backup

    # Extract the nodes from the adjacency list
    nodes = list(adj.keys())
    
    # Extracts the subgraph from G composed of the nodes of "nodes" list
    # dcs is the densest subgraph
    dcs = G.subgraph(nodes)

    print("The densest subgraph consists of ", len(nodes), " nodes.")

    # Returns DCS graph
    return dcs
