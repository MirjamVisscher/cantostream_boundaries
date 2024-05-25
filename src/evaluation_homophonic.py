#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 21:44:56 2023
Function to run the 3 homophonic works and compare them to the boundary annotations 
by one human reference

@author: MirjamVisscher
"""


import os
import random
import pandas as pd
import numpy as np
import mir_eval
from algorithms import run_algorithms


# random.seed(8)
# epsilon = 0.00001
# evalwindow=8
# files = ['1. Arcadelt, Ave Maria', '2. Isaac, Innsbruck, ich muss dich lassen']
# algorithms = ['cnmf', 'foote', 'olda', 'scluster', 'sf', 'vmo']
# pd.set_option('display.float_format', '{:.2f}'.format)
# f=files[0]

# reference = pd.DataFrame()
# algo = pd.DataFrame()

# for f in files:
#     run_algorithms(f, algorithms)
#     reference_work = pd.read_csv(os.path.join('..', 'data', 'raw', 'annotations', f+'.csv'))
#     algo_work = pd.read_csv(os.path.join('..', 'data', 'processed', 'boundaries', f+'.csv'))
#     reference = pd.concat([reference, reference_work])
#     algo = pd.concat([algo, algo_work])

# results = [['Comparison', 'P', 'R', 'F']]
# for i in algorithms:
#     reference_intervals = reference.timestamp.dropna()
#     reference_intervals= np.array([reference_intervals, reference_intervals+epsilon]).T
#     estimated_intervals = algo.loc[algo.algorithm==i, 'timestamp']
#     estimated_intervals = np.array([estimated_intervals, estimated_intervals+epsilon]).T
#     P, R, F = mir_eval.segment.detection(reference_intervals, estimated_intervals, window=evalwindow, beta=1.0, trim=True)
#     results.append([i, P, R, F])
# results = (pd.DataFrame(results[1:], columns=results[0])
#                  .sort_values(by=['P'], ascending=False))
# results.to_csv(os.path.join('..', 'results', 'paper','evaluation_homophonic_compositions_window8.csv'))

# print('results of '+f)
# print(results)

def evaluate_homophonic_paper(files, algorithms, epsilon=0.00001, evalwindow=8):
    """
    Evaluate boundaries based on given files and algorithms.

    Parameters:
    - files (list): List of file names (without extension).
    - algorithms (list): List of algorithm names.
    - epsilon (float): Small value added to timestamps to avoid exact matches.
    - evalwindow (int): Window size for evaluation in seconds.
    """

    # Setting seed
    random.seed(8)

    # Placeholder for results
    results = [['Comparison', 'P', 'R', 'F']]
    reference = pd.DataFrame()
    algo = pd.DataFrame()
    
    # Iterate over files
    for f in files:
        run_algorithms(f, algorithms)
        reference_work = pd.read_csv(os.path.join('..', 'data', 'raw', 'annotations', f + '.csv'))
        algo_work = pd.read_csv(os.path.join('..', 'data', 'processed', 'boundaries', f + '.csv'))
        
        reference = pd.concat([reference, reference_work])
        algo = pd.concat([algo, algo_work])

    # Evaluate results for each algorithm
    for i in algorithms:
        reference_intervals = reference.timestamp.dropna()
        reference_intervals = np.array([reference_intervals, reference_intervals + epsilon]).T
        estimated_intervals = algo.loc[algo.algorithm == i, 'timestamp']
        estimated_intervals = np.array([estimated_intervals, estimated_intervals + epsilon]).T
        P, R, F = mir_eval.segment.detection(reference_intervals, estimated_intervals, window=evalwindow,
                                              beta=1.0, trim=True)
        results.append([i, P, R, F])

    # Save results to a CSV file
    results_df = pd.DataFrame(results[1:], columns=results[0]).sort_values(by=['P'], ascending=False)
    results_df.to_csv(os.path.join('..', 'results', 'paper', 'evaluation_homophonic_compositions_window8.csv'))

    print('Evaluation results:')
    print(results_df)
