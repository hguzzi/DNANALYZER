# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 11:33:37 2019
@author: Pietro Hiram Guzzi
External packages
tkinter
datetime
matplotlib
pandas
networkx
netwulf
cdlib
"""

import matplotlib
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import *
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk,  scrolledtext 
from tkinter import *
import pandas as pd
import networkx as nx
import numpy as np
from ExecutionWindow import *
from netwulf import visualize


finestra = tk.Tk()
finestra.geometry('500x850')
finestra.title('Dual-Network Analyzer')
Label (text="   ", font=("Helvetica",18)).grid(row=0, column=1)
#statusbar = tk.Label(finestra, text="on the way…", bd=1, relief=tk.SUNKEN, anchor=tk.W)

#statusbar.pack(side=tk.BOTTOM, fill=tk.X)


#TODO: SISTEMARE LA GRANDEZZA ED INSERIRE IL LOGGER DEGLI ALTRI.
#text_area = scrolledtext.ScrolledText(finestra,  
                                     # wrap = tk.WORD,  
                                     # width = 60,  
                                     # height = 10,  
                                     # font = ("Times New Roman", 
                                     #         8)) 
  
#text_area.grid(row=22, column = 3, pady = 10, padx = 10) 

# Global Variables
global pathphysicalfile, pathconceptualfile, pathsimilarityfile, delta, qudilouvain,combovalue

global parameters
parameters  = dict()

#------------Scelta Dataset da CSV----------------#
#testo = Label (text=" Select Physical Network", fg="green", bg="black", font=("Helvetica",15)).grid(row=7, column=1, pady=10, padx=20)


# apri_file in partenza
testo = Label (text=" Step 1 ", font=("Helvetica",10)).grid(row=8, column=1, pady=10)
def open_physicalnetwork() :
    
    parameters['pathphysicalfile']= filedialog.askopenfilename()
    Label (text='Selected', font=("Helvetica",8)).grid(row=8, column=2, padx=10, pady=10)
    #text_area.insert(tk.INSERT,'Selected File')

Button(finestra, text="Select Physical Network", command=open_physicalnetwork).grid(row=9, column=1, padx=10, pady=10)

#testo = Label (text=" Select File  ", font=("Helvetica",10)).grid(row=11, column=1, pady=10)
#--------------Scelta dataset uniprot da CSV
#testo = Label (text=" Select Conceptual Network ", fg="green", bg="black", font=("Helvetica",15)).grid(row=12, column=1, pady=10, padx=20)
# apri_file2 in partenza
testo = Label (text=" Step 2 ", font=("Helvetica",10)).grid(row=12, column=1, pady=10)

def open_conceptualnetwork() :
    #global path2
    parameters['pathconceptualfile']= filedialog.askopenfilename()
    Label (text='Selected Conceptual Network', font=("Helvetica",12)).grid(row=12, column=2, padx=10, pady=10)

Button(finestra, text="Select Conceptual Network", command=open_conceptualnetwork).grid(row=13, column=1, padx=10, pady=10)

testo = Label (text=" Step 3  ", font=("Helvetica",10)).grid(row=15, column=1, pady=10)
# apre il file di similaritya
def open_similarity() :
    #global path3
    parameters['pathsimilarityfile']= filedialog.askopenfilename()
    Label (text='Selected Similarity File', font=("Helvetica",10)).grid(row=15, column=2, padx=10, pady=10)

Button(finestra, text="Select Similarity File", command=open_similarity).grid(row=16, column=1, padx=10, pady=10)

#testo = Label (text="   ", font=("Helvetica",10)).grid(row=17, column=1, pady=10)


'''Scelta del Parametro Delta e di Q di Louvain
    consentono la scelta del virus da analizzare
'''
testo = Label (text=" Step 4 - Delta ", font=("Helvetica",10)).grid(row=17, column=1, pady=10)
def delta() :
    #global delta
    parameters['delta']=e1.get()
    
e1=Entry(finestra)
e1.grid(row=18, column=1,padx=10, pady=4)
Button(finestra,text="Save Delta",command=delta).grid(row=19,column=1,padx=10, pady=4)
 
testo = Label (text=" Step 5 - Only for Louvain ", font=("Helvetica",10)).grid(row=20, column=1, pady=10)
def qudilouvain() :
    #global qudilouvain
    parameters['qudilouvain']=e2.get()
    
e2=Entry(finestra)
e2.grid(row=21, column=1,padx=10, pady=4)
Button(finestra,text="Save Q",command=qudilouvain).grid(row=22,column=1,padx=10, pady=4)
 
#testo = Label (text=" Select Method ",  font=("Helvetica",10)).grid(row=23, column=1, pady=10, padx=20)
#TODO: fare in modo che sia disattivato la modifica.
#def callbackFunc(event):
#     combovalue=comboExample.get()
#     parameters['algorithm']=combovalue
#     print(comboExample.get())
#comboExample = ttk.Combobox(finestra, 
 #                           values=[
 #                                   "Charikar Algorithm", 
 #                                   "Louvain"])
#comboExample.grid(row=24, column=1,padx=10, pady=4)  
#comboExample.bind("<<ComboboxSelected>>", callbackFunc)

#TODO: MPDOFICARE LA SCLETA AFFICNE SIA FOLDER E NON FILE
    
    
 # Creating scrolled text  
# area widget 

#testo = Label (text=" Output Folder ", fg="green", bg="black", font=("Helvetica",15)).grid(row=25, column=1, pady=10, padx=20)
#def open_outputfolder() :
    #global path3
#    parameters['outputfolder']= filedialog.askopenfilename()
#    Label (text='Selected outputfolder', font=("Helvetica",10)).grid(row=16, column=2, padx=10, pady=10)
     #G = nx.barabasi_albert_graph(100,m=1)
     #visualize(G)

#Button(finestra, text="Output Folder", command=open_outputfolder).grid(row=27, column=1, padx=10, pady=10)




   
def start():
    # insert here le chiamate.
    print(parameters)
    
    
    ### RICHIAMARE I MODULI
    
    ### ESEGUIRE
    ex=ExecutionWindow(finestra,parameters)
    ex.runCharikar()
  #  extra_window = tk.Toplevel(finestra)
   # label2 = tk.Label(extra_window, text="""this is extra_window
     #                  closing this will not affect root""")
    #label2.pack()

    #
    #
    return
Button(finestra, text="Start Charikar", command=start).grid(row=40, column=1, pady=10, padx=200)
def start():
    # insert here le chiamate.
    print(parameters)
    
    
    ### RICHIAMARE I MODULI
    
    ### ESEGUIRE
    exl=ExecutionWindow(finestra,parameters)
    exl.runLuvain()
  #  extra_window = tk.Toplevel(finestra)
   # label2 = tk.Label(extra_window, text="""this is extra_window
     #                  closing this will not affect root""")
    #label2.pack()

    #
    #
    return
Button(finestra, text="Start Louvain", command=start).grid(row=42, column=1, pady=10, padx=200)


def uscita() :

	if messagebox.askyesno('Uscita', 'Do you want to terminate the program?'):
		finestra.destroy()

Button(finestra, text="Exit", command=uscita).grid(row=44, column=1, padx=00)


finestra.mainloop()
