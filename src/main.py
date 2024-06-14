#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Main script for launching the evaluation of annotations and boundaries

The tasks of this script are:
1 Run the algorithms and save the output
2 Join algorithm boundaries and human annotations with the same timestamps
3 Plot a heatmap of the annotations and boundaries
4 Smooth the annotations with a Gaussian kernel
5 Compute a distance matrix within each annotations and boundaries
6 Perform a hierachical clustering based on that metric
7 Find the peaks in the non-smoothered annotations
8 Evaluate the difference between expert annotations, non-expert annotations,
  and algorithm boundaries
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os
import random

from algorithms import run_algorithms
from join import join_algorithms_annotations
from heatmap import plot_heatmap
from smoother import smooth_annotations
from distances import compute_distances
from clustering import clustering
from peakplotter import plot_peaks
from peakfinder import find_peaks
from evaluation import evaluate
from evaluation_homophonic import evaluate_homophonic_paper
from smoother_paper import gaussian_curves_paper
from clustering_paper import clustering_paper

"""
Define the files to use from data/audio
If you want to run your own corpus, the name convention for the annotations
is w[n].csv and for the audio files w[n].wav where n is the position of the
work in the dataset. The w is to prevent the Foote  algorithm from crashing
on the file name.
The file /data/raw/Ren8_works.csv provides the titles of the works and is
used for the plot titles
"""

random.seed(131)

files = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8']

# Define the tiles of the works
works_file= os.path.join('..', 'data','raw', 'metadata','Ren8_works.csv')
works= pd.read_csv(works_file).fillna(0).set_index('ren8_id').file_name_sheet_music.to_dict()
# Define the algorithms to evaluate
algorithms = ['cnmf', 'foote', 'olda', 'scluster', 'sf', 'vmo']
# Define the name of the experts and non-experts in the annotation files
experts_list = ['e1','e2','e3','e4','e5','e6','e7','e8']
nonexperts_list = ['n1','n2','n3','n4','n5','n6','n7','n8','n9','n10','n11','n12','n13']
# Define the table that will contain the performance on all files
total_results = [['Comparison', 'P', 'R', 'F']]
for experience in ['reference', 'Non-expert']:
    total_results.append([experience, 0.0, 0.0, 0.0])
for experience in algorithms:
    total_results.append([experience, 0.0, 0.0, 0.0])
all_annotations = pd.DataFrame()
distance_matrix = pd.DataFrame()
peakwindow = 4 #window for the peakfinder
evalwindow = 8 #window for the individual evaluation

for f in files:
    title = works[int(f[1])]
    # Load the extended annotation file. The extension is to prevent the peakfinder missing the last peak
    annotations_file = os.path.join('..', 'data', 'raw', 'annotations', f+'.csv')
    # annotations_file = os.path.join('..', 'data', 'raw', 'annotations_extended', f+'.csv')
    annotations = pd.read_csv(annotations_file).fillna(0)
    # Verify which of the participants actually annotated this specific file
    experts = list(set(experts_list).intersection(annotations.columns))
    nonexperts = list(set(nonexperts_list).intersection(annotations.columns))
    # Remove of a temporary file to avoids crash due to a bug in OLDA algorithm
    if os.path.exists(os.path.join('..', 'data', 'raw', 'estimations', f+'.jams')):
        os.remove(os.path.join('..', 'data', 'raw', 'estimations', f+'.jams'))
    # # Execute the different steps of the framework    
    run_algorithms(f, algorithms)
    result = join_algorithms_annotations(f, experts, nonexperts)
    result['work'] = f
    # join single files to one big file for all works
    all_annotations = pd.concat([all_annotations,result])
    plot_heatmap(f, title)
    smooth_annotations(f,title, algorithms, experts, nonexperts)
    distances = compute_distances(f)
    # add distance matrix of the work to the total distance matrix
    distance_matrix = pd.concat([distance_matrix, distances])
    # plot the peaks to provide an opportunity to do a visual inspection of the peaks
    plot_peaks(f, title, peakwindow)
    # Evaluate the obtained boundaries and annotations for each single work
    results = evaluate(f, algorithms, evalwindow)
    print('Performance on '+f+' for evaluation window '+str(evalwindow))
    print(pd.DataFrame(results))

# Compute the average pairwise distance over all works (the input is normalised to quarter notes)
distance_matrix = (distance_matrix
                    .groupby(distance_matrix.index)
                   .mean()
                   .sort_index()
                   .sort_index(axis=1)
                   )
distance_matrix.to_csv(os.path.join('..', 'data', 'processed', 'distances','distance_matrix.csv'))
clustering('distance_matrix', 'ward')

# provide each quarter note in the corpus with a unique identifier global_unit
all_annotations['global_unit'] = range(len(all_annotations))
all_annotations.to_csv(os.path.join('..', 'data', 'processed', 'join','all_annotations.csv'))

# peakfinder on this all_annotations
find_peaks(files, peakwindow)

"""
Below is the code that reproduces the paper content
"""
# table 3
evalwindows = [8,4,2]
total_eval = None
for evalwindow in evalwindows:
    window_results = evaluate('all_annotations', algorithms, evalwindow= evalwindow)
    print('Average performance for windowsize '+str(evalwindow))
    # Display the average performance
    window_results = (pd.DataFrame(window_results[1:], columns=  window_results[0])
                     .sort_values(by=['P'+str(evalwindow)], ascending=False))
    print(window_results)
    window_results.to_csv(os.path.join('..', 'results', 'output','evaluation_window_'+ str(evalwindow)+ '.csv'))
    if total_eval is None:
        total_eval = window_results.copy()
    else:
        total_eval = pd.merge(total_eval, window_results, on='Comparison')
        
total_eval.to_csv(os.path.join('..', 'results', 'paper','evaluation.csv'))    

# table 5
evaluate_homophonic_paper(files=['2. Isaac, Innsbruck, ich muss dich lassen', '3. Byrd, Ave verum corpus'],algorithms=algorithms)

# figure 4
gaussian_curves_paper('w3', algorithms)
# figure 5
clustering_paper('distance_matrix', 'ward')


print('ready!')