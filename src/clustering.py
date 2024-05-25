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

def clustering(filename, method):
    print('Running clustering for '+filename+ ' '+method+'...')
    df = pd.read_csv(os.path.join('..', 'data', 'processed', 'distances', filename+'.csv'), index_col=0)
    # Compute Ward hierachical clustering
    hier = linkage(squareform(df), method=method, optimal_ordering=True)
    # # Plot the clustering map
    hierarchy.dendrogram(hier, labels = df.index, color_threshold = 0.12, orientation='right', )
    # Save it to log file
    plt.savefig(os.path.join('..', 'results', 'figures', 'clusters_of_'+filename+'_'+method+'.png'))
    plt.close()
