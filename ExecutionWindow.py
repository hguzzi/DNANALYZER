#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 09:25:35 2021

@author: pietrohiramguzzi


"""
from datetime import datetime
import matplotlib
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import *
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import pandas as pd
import networkx as nx
import numpy as np
import os
import LouvainDCSExtractor as ldcs
from DualNetworkAligner import buildGraph, pairwiseAlignment
from CharikarDCSExtractor import extractDCS
from GraphVisualizer import *
from netwulf import visualize

class ExecutionWindow :
    '''
    init builds a novel execution window
    t is the top tk window
    p is the dictionary containig the parameters for the execution
    '''
    def __init__(self, t, p):
        self.topwindow=t
        self.parameters=p
       
        #self.runCharikar()
        
    def runCharikar(self):
            print('Start Charikar')
            #outputDirectoryPath=self.parameters['outputfolder']
            outputDirectoryPath=os.getcwd()
            alignmentGraphPickle = outputDirectoryPath+"alignmentGraph.gz2"
# Compressed Pickle file of the DCS graph
            dcsGraphPickle = outputDirectoryPath+"dcs.gz2"
# Txt file of the DCS graph
            GraphAlignment=outputDirectoryPath+"alignment.txt"
            dcsGraphTxt = outputDirectoryPath+"dcs.txt"

        #try:
            extra_window = tk.Toplevel(self.topwindow)
            extra_window.title("Visualizer")
            label2 = tk.Label(extra_window, text="""Charikar""")
            label2.pack()
            
            # STEP ONE: build the graphs

# Builds the weighted graph W
            print(datetime.now(), " --> build weighted graph W...")
            W = buildGraph(self.parameters['pathconceptualfile'], skipLines=0,
               splitSep=" ", weightedEdges=True)
            print(datetime.now(), " --> W: nodes ",
                  len(W.nodes()), " edges: ", len(W.edges()))
            visualize(W)
# Stores the weighted graph in a pickle file
# nx.write_gpickle(W, weightedGraphPickle) # UNCOMMENT this line if you want to save a graph

# Builds the unweighted graph U
            print(datetime.now(), " --> build unweighted graph U...")
            print(self.parameters['pathphysicalfile'])
            U = buildGraph(self.parameters['pathphysicalfile'], skipLines=0,
               splitSep=" ", weightedEdges=False)
            print(datetime.now(), " --> U: nodes ",
                 len(U.nodes()), " edges: ", len(U.edges()))
            visualize(U)
# Stores the unweighted graph in a pickle file
# nx.write_gpickle(U, unweightedGraphPickle) # UNCOMMENT this line if you want to save a graph

# STEP TWO
# Builds the alignment graph A
            print(datetime.now(), " --> build alignment graph A...")
            A = pairwiseAlignment(U, W, k=5, simTxt=self.parameters['pathsimilarityfile'], skipLines=0, splitSep="-")
            print(datetime.now(), " --> alignGraph A: nodes ",
            len(A.nodes()), " edges: ", len(A.edges()))
            # Stores the alignment graph in a pickle file
#nx.write_gpickle(A, alignmentGraphPickle) # COMMENT this line if you don't want to save a graph

# LAST STEP
# Extracts the DCS from the alignment graph
            print(datetime.now(), " --> Search DCS in alignment graph...")
            dcsA = extractDCS(A)
# Stores the DCS graph of A in a pickle file
            nx.write_gpickle(dcsA, dcsGraphPickle)
            dcsnx=nx.Graph(dcsA)
            visualize(dcsnx)
# Stores the DCS graph of A in a text file
            print(A)
#with open(GraphAlignment,"w") as txt:    
#   for edg1, edg2 in A.nodes:
#        print(edg1+" "+edg2+" "+str(A[edg1][edg2]['weight']))
        #print(edg1)
        #txt.write(edg1+" "+edg2+" "+str(A[edg1][edg2]['weight'])+"\n")
            print(GraphAlignment)
            nx.write_weighted_edgelist(A, GraphAlignment)


        #except: print('Error')
               
            return
    
    def runLuvain(self):
        try: 
           # extra_window = tk.Toplevel(self.topwindow)
           # label2 = tk.Label(extra_window, text="""Louvain""")
           # label2.pack()
            print('Start Louvain')
            outputDirectoryPath="."
            outputDirectoryPath="/Users/pietrohiramguzzi/Desktop/2021-BMC-BBCCExtended/"
            alignmentGraphPickle = outputDirectoryPath+"alignmentGraph.gz2"
# Compressed Pickle file of the DCS graph
            dcsGraphPickle = outputDirectoryPath+"dcs.gz2"
# Txt file of the DCS graph
            GraphAlignment=outputDirectoryPath+"alignment.txt"
            dcsGraphTxt = outputDirectoryPath+"dcs.txt"

        #try:
           # extra_window = tk.Toplevel(self.topwindow)
           # extra_window.title("Visualizer")
           # label2 = tk.Label(extra_window, text="""Charikar""")
          #  label2.pack()
            
            # STEP ONE: build the graphs

# Builds the weighted graph W
            print(datetime.now(), " --> build weighted graph W...")
            W = buildGraph(self.parameters['pathconceptualfile'], skipLines=0,
               splitSep=" ", weightedEdges=True)
            print(datetime.now(), " --> W: nodes ",
                  len(W.nodes()), " edges: ", len(W.edges()))
            #visualize(W)
# Stores the weighted graph in a pickle file
# nx.write_gpickle(W, weightedGraphPickle) # UNCOMMENT this line if you want to save a graph

# Builds the unweighted graph U
            print(datetime.now(), " --> build unweighted graph U...")
            print(self.parameters['pathphysicalfile'])
            U = buildGraph(self.parameters['pathphysicalfile'], skipLines=0,
               splitSep=" ", weightedEdges=False)
            print(datetime.now(), " --> U: nodes ",
                 len(U.nodes()), " edges: ", len(U.edges()))
            #visualize(U)
# Stores the unweighted graph in a pickle file
# nx.write_gpickle(U, unweightedGraphPickle) # UNCOMMENT this line if you want to save a graph

# STEP TWO
# Builds the alignment graph A
            print(datetime.now(), " --> build alignment graph A...")
            A = pairwiseAlignment(U, W, k=self.parameters['delta'], simTxt=self.parameters['pathsimilarityfile'], skipLines=0, splitSep="-")
            print(datetime.now(), " --> alignGraph A: nodes ",
            len(A.nodes()), " edges: ", len(A.edges()))
            
            # Stores the alignment graph in a pickle file
#nx.write_gpickle(A, alignmentGraphPickle) # COMMENT this line if you don't want to save a graph

# LAST STEP
        # LAST STEP
# Extracts the DCS from the alignment graph
            print(datetime.now(), " --> Search Communities in alignment graph...")
            print(type(A))
            dcsA = ldcs.extractLouvain(nx.Graph(A))
            print(datetime.now,'End Louvain')
# Stores the DCS graph of A in a pickle file
            #nx.write_gpickle(dcsA, dcsGraphPickle)
            print(datetime.now(),'Start Visualisation')
            #dcsnx=nx.Graph(dcsA)
            #visualize(dcsnx)
# Stores the DCS graph of A in a text file
            print(dcsA)
#with open(GraphAlignment,"w") as txt:    
#   for edg1, edg2 in A.nodes:
#        print(edg1+" "+edg2+" "+str(A[edg1][edg2]['weight']))
        #print(edg1)
        #txt.write(edg1+" "+edg2+" "+str(A[edg1][edg2]['weight'])+"\n")
            print(GraphAlignment)
            nx.write_weighted_edgelist(A, GraphAlignment)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)        
            return -1
        return
    
if __name__ == '__main__':
    e=ExecutionWindow(tk,{})
    #e.runCharikar()
      
        