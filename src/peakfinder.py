#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to find the peaks in non-smoothed group annotations

The tasks of this script are:
1 Read the join file
2 Find the peaks in expert and non-expert groups
3 Plot the resulting values
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os
from scipy import signal

# files = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8']
# window = 4


def find_peaks(files, window=4):
# all_annotations = pd.DataFrame()
# for filename in files:
#     df = pd.read_csv(os.path.join('..', 'data', 'processed','join', filename+'.csv'))
#     # append files to frame
#     all_annotations = pd.concat([all_annotations, df]).reset_index(drop=True)
    
    
# # Find peaks in both signals
# peaks_x = signal.find_peaks_cwt(all_annotations['non-expert'], widths=[window])
# peaks_y = signal.find_peaks_cwt(all_annotations['expert'], widths=[window])

#     # Save the peaks to a log file
# d = {'non-expert': peaks_x, 'expert': peaks_y, 'reference': df.loc[df['reference']!=0].index}
# evaluation_input = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
# evaluation_input.to_csv(os.path.join('..', 'data', 'processed', 'peaks.csv'))



    cumulation = 0
    all_peaks =  pd.DataFrame()
    
    for f in files:
        df = pd.read_csv(os.path.join('..', 'data', 'processed','join', f+'.csv'))
        peaks_nonexpert = signal.find_peaks_cwt(df['non-expert'], widths=[window])
        peaks_expert = signal.find_peaks_cwt(df['expert'], widths=[window])
        
        d = {'non-expert': peaks_nonexpert, 'expert': peaks_expert, 'reference': df.loc[df['reference']!=0].index}
        work_peaks = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))+cumulation
        all_peaks = pd.concat([all_peaks,work_peaks])
        
        cumulation = cumulation + len(df)
    all_peaks.to_csv(os.path.join('..', 'data', 'processed', 'peaks', 'all_annotations.csv'))
    return all_peaks