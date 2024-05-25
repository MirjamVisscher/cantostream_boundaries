#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to perform the clustering based on the distances

The tasks of this script are:
1 Read the distances matrix
2 Compute Ward hierachical clustering
3 Plot the distance matrix along the clustering
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

def clustering_paper(filename, method):
    # plt.style.use('seaborn-v0_8-whitegrid')
    plt.style.use('grayscale')
    plt.figure(figsize=(6, 6), facecolor='white')
    print('Running clustering for '+filename+ ' '+method+'...')
    df = pd.read_csv(os.path.join('..', 'data', 'processed', 'distances', filename+'.csv'), index_col=0)
    plt.subplot(111)
    # Compute Ward hierachical clustering
    hier = linkage(squareform(df), method=method, optimal_ordering=True)
    # # Plot the clustering map
    hierarchy.dendrogram(hier, labels = df.index, color_threshold = 0.12, orientation='right', )
    # Save it to log file
    plt.figtext(0.6,0.8,'cluster 1', color= 'grey', fontsize='x-large')
    plt.figtext(0.6,0.55,'cluster 2', color= 'grey', fontsize='x-large')
    plt.figtext(0.6,0.3,'cluster 3', color= 'grey', fontsize='x-large')
    for i in (10,100,232):
        plt.axhline(y=i, color='grey', linestyle='--', linewidth = 1)
    plt.subplots_adjust(left=0.2)  # Adjusted margins
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(False)
    plt.xlabel('distance')
    # plt.show()
    plt.savefig(os.path.join('..', 'results', 'paper',  'paper_clusters_of_'+filename+'_'+method+'.png'))
    plt.show()
    plt.close()
