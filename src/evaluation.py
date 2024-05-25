#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to evaluate the difference between experts, non-experts and algorithms

The tasks of this script are:
1 Read the peaks and join files
2 Compare the performance of non-experts and algorithms against experts notations
3 Resulting the resulting values
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import numpy as np
import os
import mir_eval


def evaluate(filename, algorithms, evalwindow=8):
    print('Running evaluation for '+filename+ '...')
    pd.set_option('display.float_format', '{:.2f}'.format)
    humanpeaks = pd.read_csv(os.path.join('..', 'data', 'processed', 'peaks', filename+'.csv'))
    algopeaks = pd.read_csv(os.path.join('..', 'data', 'processed', 'join', filename+'.csv'))

    epsilon = 0.00001
    reference_intervals = humanpeaks['expert'].dropna()
    # Set the experts notations with a +-epsilon error tolerance
    reference_intervals= np.array([reference_intervals, reference_intervals+epsilon]).T
    results = [['Comparison', 'P'+str(evalwindow), 'R'+str(evalwindow), 'F'+str(evalwindow)]]

    # Evaluate the performance of non-experts and reference
    for experience in ['reference', 'non-expert']:
        estimated_intervals = humanpeaks[experience].dropna()
        estimated_intervals = np.array([estimated_intervals, estimated_intervals+epsilon]).T
        P, R, F = mir_eval.segment.detection(reference_intervals, estimated_intervals, window=evalwindow, beta=1.0, trim=True)
        results.append([experience, P, R, F])
    # Evaluate the performance of algorithms
    for experience in algorithms:
        estimated_intervals = algopeaks.loc[algopeaks[experience]!=0].index
        estimated_intervals = np.array([estimated_intervals, estimated_intervals+epsilon]).T
        P, R, F = mir_eval.segment.detection(reference_intervals, estimated_intervals, window=evalwindow, beta=1.0, trim=True)
        results.append([experience, P, R, F])
    
    return results
