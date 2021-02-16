# Package for the creation, manipulation,
# and study of the structure, dynamics,
# and functions of complex networks.
# https://networkx.github.io/
import networkx as nx

# Utility packages
import sys


# Builds the similarity file of dual networks that have nodes with the same label
def buildSimFile(graph, filePath):
    '''Builds the similarity file of dual networks that have nodes with the same label,
         using the order of the weighted graph nodes as ordering.
        Parameters:
            - graph: weighted graph;
            - filePath: file name, complete with path, in which to store the similarities.'''

    # REMOVE
    # Node name array
    simList = []
    for i in graph.nodes:
        simList.append([i, i])

    # Opens filePath in write mode
    with open(filePath, 'w', encoding='utf-8') as txt:
        # Iterates simList
        for i in simList:
            # Appends i to text file
            # The first element of the line is from the unweighted graph,
            # the second from the weighted graph
            txt.write(i[0]+"-"+i[1]+"\n")
    # END REMOVE

    # Opens filePath in write mode
    with open(filePath, 'w', encoding='utf-8') as txt:
        # Iterates simList
        for i in graph.nodes:
            # Appends i to text file
            # The first element of the line is from the unweighted graph,
            # the second from the weighted graph
            txt.write(i+"-"+i+"\n")


# Normalize the weight of edges in a graph
def normWeight(objGraph):
    '''Normalize the weight of edges in a graph.
        Parameters:
            - objGraph: graph object of the Networkx.Graph class.
        Returns:
            - objGraph: normalized graph object of the Networkx.Graph class.'''

    # Array of edges weights
    weight = []

    # Iterates over edges of graph
    for i in objGraph.edges():
        # Appends to weight array the edge i
        weight.append(objGraph.get_edge_data(i[0], i[1])['weight'])

    # Finds the biggest item of weight array
    maxWeight = max(weight)

    # Iterates over edges of graph again
    for j in objGraph.edges():

        # Choose the correct formula based on the meaning
        # of weighted edge for the specific test.

        # Formula for calculating the new normalized weight of edge i
        w = objGraph.get_edge_data(j[0], j[1])['weight']/maxWeight

        # Alternative formula for calculating the new normalized weight of the edge i
        #w = 1.0 - (objGraph.get_edge_data(j[0], j[1])['weight']/maxWeight)

        # Replaces the new weight value with the previous one
        objGraph.add_edge(j[0], j[1], weight=w)

    # Returns the normalized graph
    return objGraph


# Builds a undirected graph from a text file
def buildGraph(pathGraph, skipLines=1, splitSep=" ", weightedEdges=False):
    '''Builds a undirected graph from a text file.
        Parameters:
            - pathGraph: path of the file (txt) containing the graph building information (row file example: NameNode1 NameNode2 EdgeWeight);
            - skiplines: number header lines of the file to be skipped (default: 1);
            - splitSep: separator character for to split a line into substrings (default: " ");
            - weightedEdges: boolean indicating whether the edges of the graph are weighted (default: False).
        Returns:
            - objGraph: graph object of the Networkx.Graph class.'''

    # Creates an empty graph
    objGraph = nx.Graph(data=True)

    # Creates an unweighted graph
    if(weightedEdges == False):

        try:
            # Opens the file as read-only
            f = open(pathGraph, 'r')
        except:
            # Handle the bad path exception
            sys.exit("ERROR! Unable to open file: "+pathGraph)

        # Lines counter, to skip the header
        nLine = 1

        # If the file is not empty it reads line by line and builds the graph
        for line in f:

            # Removes the "line feed" control character from line
            line = line.replace('\n', '')

            # Check if the line is part of the header
            # If the line is not a header
            if(skipLines < nLine):
                # Splits a line into substrings that are based on the character in splitSep
                lineSplit = line.split(' ')
                #print(lineSplit)
                # If the split produced two substrings
                # (the two substrings represent the two connected nodes)
                # if(len(lineSplit) == 2):
                objGraph.add_edge(lineSplit[0], lineSplit[1])
                # If the split produced no substrings
                # else:
                # Return an error string
                #sys.exit("ERROR in a line of the file: "+pathGraph)

            # If the line is a header
            else:
                # Skips line and increases the line counter
                nLine += 1

        # Closes the file f
        f.close()

    # Creates a weighted graph
    else:
        try:
            # Opens the file as read-only
            f = open(pathGraph, 'r')
        except:
            # Handle the bad path exception
            sys.exit("ERROR! Unable to open file: "+pathGraph)

        # Lines counter, to skip the header
        nLine = 1

        # If the file is not empty it reads line by line and builds the graph
        for line in f:

            # Removes the "line feed" control character from line
            line = line.replace('\n', '')

            # Check if the line is part of the header
            # If the line is not a header
            if(skipLines < nLine):
                # Splits a line into substrings that are based on the character in splitSep
                lineSplit = line.split(splitSep)

                # If the split produced three substrings
                # (the first two substrings represents the two connected nodes,
                # the last, the weight of the edge)
                if(len(lineSplit) == 3):
                    # Adds a weighted edge with its nodes to the graph
                    objGraph.add_edge(
                        lineSplit[0], lineSplit[1], weight=float(lineSplit[2]))
                # If the split produced no substrings
                else:
                    # Return an error string
                    sys.exit("ERROR in a line of the file "+pathGraph)

            # If the line is a header
            else:
                # Skips line and increases the line counter
                nLine += 1

        # Closes the file f
        f.close()

        # Normalizes the weight of the edges
        objGraph = normWeight(objGraph)

    # Returns the built graph
    return objGraph


# Alignment algorithm
def pairwiseAlignment(U, W, k, simTxt, skipLines, splitSep):
    '''Pairwise local aligner for dual networks.
        Parameters:
            - U: unweighted graph (physical network);
            - W: weighted graph (conceptual network);
            - simTxt: similarity files, example row -> "Unode-Wnode". 
                The TXT file indicates which node of the physical network corresponds 
                in the conceptual network;
            - skipLines: number header lines of simTxt to be skipped;
            - splitSep: separator character for to split a line of simTxt into substrings;
        Returns:
            - algnGraph: graph of the Graph class of the Networkx library.'''

    # Creates an empty graph
    algnGraph = nx.Graph(data=True)
    # Node pair array to compare
    sim = []
    # Matched node pair counter
    match = 0
    # Gap node pair counter
    gap = 0
    # Mismatch node pair counter
    # mismatch = 0

    # Fills sim array from simTxt file and add nodes in algnGraph
    # Opens the file as read-only
    with open(simTxt, 'r', encoding='utf-8') as txt:
        # Lines counter, to skip the header
        nLine = 1
        # If the file is not empty it reads line by line and builds the sim array
        for row in txt:
            # Check if the line is part of the header
            # If the line is not a header
            if nLine > skipLines:
                # Remove the "line feed" control character from line
                row = row.replace('\n', '')

                # N.B. necessary for the correct application of the Louvain method
                # of community research.
                # The nodes of the alignment graph must be inserted in the same order
                # as those of the weighted graph.

                # Adds a new node in the alignment graph that has
                # the row content as its name
                algnGraph.add_node(row)

                # Splits a row into substrings that are based on the character in splitSep
                n = row.split('-')
                # Appends the substrings in sim
                # n[0] -> node of unweighted graph;
                # n[1] -> Corresponding node of weighted graph
                sim.append([n[0], n[1]])

            # Increases the line counter
            nLine = nLine+1

    # Edges building
    # Scans the sim array in the following way to not compare the same nodes
    while len(sim) > 1:
        # Removes and returns the first item of sim
        i = sim.pop(0)
        # Node of unweighted graph
        u1 = i[0]
        # Node of weighted graph
        w1 = i[1]
        # Node of alignGraph
        a1 = u1+"-"+w1
        # Rescans the sim array, without first item
        # (for the operation of pop done first)
        for j in sim:
            # Node of unweighted graph
            u2 = j[0]
            # Node of weighted graph
            w2 = j[1]
            # Node of alignGraph
            a2 = u2+"-"+w2

            # If there is an edge between the two nodes in weighted graph
            if(W.has_edge(w1, w2) == True):
                # And if there is an edge between the two nodes in unweighted graph
                if(U.has_edge(u1, u2) == True):
                    # MATCH was found
                    # Takes the value of the edge weight of the nodes of the weighted graph
                    edgeW = W.get_edge_data(w1, w2)['weight']
                    # Adds an edge with this weight to the corresponding pair of nodes
                    # in the alignment graph
                    algnGraph.add_edge(a1, a2, weight=edgeW)

                    # Increase matched node pair counter
                    match = match+1  # match += 1

                # If only the nodes of the weighted graph are adjacent
                # Checks GAP o MISMATCH
                else:
                    try:
                        # Calculates the shortest path between the two nodes of the unweighted graph
                        path = nx.shortest_path_length(U, u1, u2)

                        # N.B. If no path exists between source and target, raises exception

                    except:
                        # Catch exception
                        path = 1000000

                    # If the path is less than a specific parameter k
                    if(path <= k):
                        # GAP was found
                        # Takes the value of the edge weight of the nodes of the weighted graph
                        edgeW = W.get_edge_data(w1, w2)['weight']

                        # Alternative method for calculating the weight of the edge in case of GAP
                        # d = 1 - (path-1)/k
                        # New edge weight of the alignment graph
                        # w = edgeW*d

                        # Adds an edge with this weight to the corresponding pair of nodes
                        # in the alignment graph
                        algnGraph.add_edge(a1, a2, weight=edgeW)

                        # Increases gap node pair counter
                        gap = gap+1  # gap += 1

                    # else: MISMATCH was found
                    # mismatch += 1
            # else: MISMATCH was found
            # mismatch += 1

    print("Match: ", match, ", Gap: ", gap)  # ", Mismatch: ", mismatch)

    # Returns the alignment graph
    return algnGraph
