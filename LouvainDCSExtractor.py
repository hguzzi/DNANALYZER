# Package for the creation, manipulation,
# and study of the structure, dynamics,
# and functions of complex networks.
# https://networkx.github.io/
import networkx as nx

# Package that allows to extract,
# compare and evaluate communities from complex networks.
# https://cdlib.readthedocs.io/en/latest/
from cdlib import algorithms

import community as community_louvain
import networkx as nx

def extractLouvain(W):
    try:
        print("Start Modularity")
        
        coms = algorithms.louvain(W, weight='weight', resolution=1., randomize=False)
    except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)
            return -1
    return coms

# Calculate the density of a weighted graph
def densityWgraph(W):
    '''Calculate the density of a weighted graph.
        Input:
            - W: weighted graph.
        Output:
            - density: density of the graph.'''

    # List of weights of edges
    ww = []

    # Iterate the edges
    for i in W.edges():
        # Appends weight of edge in ww List
        ww.append(W.get_edge_data(i[0], i[1])['weight'])

    # Density formula
    density = sum(ww)/len(W.nodes())

    # Returns the density
    return density


# Extracts the DCS from the alignment graph of the dual networks, with Louvain algorithm
def extractDCS(U, W, algnGraph):
    '''Extracts the DCS from the alignment graph of the dual networks.
        Input:
            - U: unweighted graph (physical network);
            - W: weighted graph (conceptual network);
            - lgnGraaph: alignment graph.
        Output:
            - subDCS: DCS of the alignment graph. Subgraph induced on the nodes of the densest community of the alignment graph;
            - subU: subgraph of the physical network induced on DCS nodes.
            - subW: subgraph of the conceptual network induced on DCS nodes.
    '''
    # Louvain algorithm to extract communities from the alignment graph
    NodeClustering = algorithms.louvain(
        algnGraph, weight='weight', resolution=1., randomize=False)

    # Stores the maximum density found
    maxWeight = 0

    dcs = []  # Initializes DCS node list
    Un = []  # Initializes node list of the U subgraph of the DCS
    Wn = []  # Initializes the node list of the subgraph of W of the DCS
    # Iterates the communities, found in the alignment graph
    for i in NodeClustering.communities:
        Unt = []  # Temporary list of nodes of the subgraph of U contained in the community i
        Wnt = []  # temporary list of nodes of the subgraph of W contained in the community i
        # Iterates the nodes of the community i
        for j in i:
            # Aplits the node name to extract its node from U and W
            a = j.split("-")
            u = a[0]  # Unweighted network node
            Unt.append(u)  # Appends in temporary list
            w = a[1]  # Weighted network node
            Wnt.append(w)  # Appends in temporary list
        # Computes density of the subgraph of W
        # If the temporary list contains elements
        if len(Wnt) > 0:
            # Extracts from W a subgraph containing the nodes of Wnt
            subWt = W.subgraph(Wnt)
            # If the subgraph contains nodes
            if len(subWt.nodes) > 0:
                # Calculates the density
                dWs = densityWgraph(subWt)
            else:
                # If it didn't find any subgraphs, set the density to 0
                dWs = 0
        else:
            # If the temporary list is empty, set the density to 0
            dWs = 0

        # If the actual calculated density is greater than the stored one
        if dWs > maxWeight:
            # The current density is stored as maximum
            maxWeight = dWs
            # And the subgraphs found are stored
            dcs = i.copy()
            Un = Unt.copy()
            Wn = Wnt.copy()
    # Found the community of W with maximum density
    # Extracts from the alignment graph a community
    # containing the nodes of the maximum community of W
    subDCS = algnGraph.subgraph(dcs)
    # Extracts from W and U the subgraphs of the largest community
    subU = U.subgraph(Un)
    subW = W.subgraph(Wn)
    print("DCS --> nodes: ", len(subDCS.nodes), ", edges: ",
          len(subDCS.edges), ", density: ", maxWeight)
    # Returns DCS graph and subgraphs of U and W
    return subDCS, subU, subW


# Extracts the densest community of a graph, with Louvain algorithm
def densestCommunity(graph):
    '''Extracts the densest community of a graph, with Louvain algorithm.
        Input:
            - graph: weighted graph.
        Output:
            - graphDC: subgraph induced on the nodes of the densest community of the graph.'''
    # Louvain algorithm to extract communities from the graph
    NodeClustering = algorithms.louvain(
        graph, weight='weight', resolution=1., randomize=False)

    # Stores the maximum density found
    maxWeight = 0
    dcs = []  # Initializes DCS node list
    # Iterates the communities, found in the alignment graph
    for i in NodeClustering.communities:
        # Extracts from graph a subgraph containing the nodes of community i
        Sg = graph.subgraph(i)
        # # Calculates the density
        dWs = densityWgraph(Sg)
        # If the actual calculated density is greater than the stored one
        if dWs > maxWeight:
            # The current density is stored as maximum
            maxWeight = dWs
            # And the subgraphs found are stored
            dcs = i.copy()

    # Found the community of graph with maximum density
    # Extracts from graph a community
    # containing the nodes of the maximum community stored in dcs
    graphDC = graph.subgraph(dcs)
    print("Densest Community of weighted graph --> nodes: ", len(graphDC.nodes), ", edges: ",
          len(graphDC.edges), "; density: ", maxWeight)

    # Returns DCS graph
    return graphDC
