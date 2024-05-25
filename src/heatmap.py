#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to plot the heatmap of annotations and boundaries

The tasks of this script are:
1 Read the joined file
2 Plot the heatmap of annotations and boundaries
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(filename, title):
    print('Running heatmap for '+filename+ '...')
    df = pd.read_csv(os.path.join('..', 'data', 'processed', 'join', filename+'.csv'))
    # Select only the first quarter note of each measure
    ticks = df.loc[df['quarter note']==1]  
    dfplot = df.drop(['reference','measure', 'quarter note', 'timestamp', 'Unnamed: 0'],axis = 1)
    # Transpose the DataFrame to have a row for each colums
    dfplot = dfplot.reset_index().transpose().drop('index', axis=0)
    # Plot the heatmap
    plt.figure(figsize=(20,6))   
    plt.title(title)
    sns.heatmap(dfplot, cmap="crest")
    plt.grid(axis = 'x')
    plt.title('Work '+ title)
    plt.xlabel ('Measure')
    plt.ylabel('Participant')
    plt.xticks(ticks.index, ticks.measure, fontsize=8, rotation = 45)
    # Save it to output file
    plt.savefig(os.path.join('..', 'results', 'figures', 'heatmap_'+filename+'.png'))
    plt.close()