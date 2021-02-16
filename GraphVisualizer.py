#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:35:06 2021

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
from matplotlib.ticker import NullFormatter
import warnings
import imageio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as fc
import random as rn
from scipy import stats as st
from PIL import Image, ImageTk


class GraphVisualizer :
    
    def __init__(self,t,p):
        self.topwindow=t
        self.parameters=p
    
    def visualizePhysical(self,title):
        extra_window = tk.Toplevel(self.topwindow)
        extra_window.title(title)
        #label2 = tk.Label(extra_window, text="""Visualize Physical Network""")
        #label2.pack()
        objGraph = nx.Graph(data=True)
        f = open(self.parameters['pathphysicalfile'], 'r')
        nLine = 1

        # If the file is not empty it reads line by line and builds the graph
        for line in f:

            # Removes the "line feed" control character from line
            line = line.replace('\n', '')

            # Check if the line is part of the header
            # If the line is not a header
            if(True):
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
         # here the Graph has been created
        pos3=nx.drawing.layout.spring_layout(G=objGraph, center=[0,0])
        fig3=plt.figure(figsize=(18,6), facecolor='whitesmoke') 
        fig3.suptitle('Subgraph of the infected proteins in the range analyzed', 
                  y=0.93, fontsize=20)
    
        ax3=fig3.add_subplot(111)
        ax3.axes.get_xaxis().set_major_formatter(NullFormatter())
        ax3.axes.get_yaxis().set_major_formatter(NullFormatter())
        nx.draw_networkx(G=objGraph, ax=ax3, pos=pos3, with_labels=False,  
                     node_shape='o', node_color='mediumblue',
                     node_size=10, edge_color='gray', width=0.2)
    
        nx.draw_networkx(G=objGraph, ax=ax3, pos=pos3, node_shape='o', 
                     nodelist=objGraph.nodes(), labels=ip_label, font_weigth='b', 
                     font_color='black', node_color='red', node_size=50, 
                     font_size=15, edge_color='gray', width=0.2)
    
        colors3 = ["mediumblue", "red"]
        texts3 = ["Neighbors at distance %s" %k_radius, "Infected Protein"] 
        patches3 = [plt.plot([],[], marker="o", ms=10, ls="", mec=None, 
                         color=colors3[i], label="{:s}".format(texts3[i])
                         )[0]  for i in range(len(texts3))]
    
        plt.legend(handles=patches3,  loc='1', fontsize=15, 
               shadow=True, ncol=1, facecolor="w", numpoints=1 )
    
        plot3 = fc(fig3, master=extra_window)
        plot3.show()
        plot3.get_tk_widget().grid(row=12, column=3, rowspan=14)
    
         #figure = Figure(figsize=(5, 4), dpi=100)
         #pl = figure.add_subplot(1, 1, 1)
        #nx.drawing.layout.spring_layout(G=objGraph, center=[0,0], k=1)
        #pl.show()
        #canvas = FigureCanvasTkAgg(figure, extra_window)
       # canvas.show()
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
