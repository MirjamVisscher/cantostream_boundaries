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
import matplotlib.pyplot as plt
from scipy import signal


def plot_peaks(filename,title, window=4):
    print('Running peakfinder for '+filename+ '...')
    df = pd.read_csv(os.path.join('..', 'data', 'processed','join', filename+'.csv'))
    # Select the groups non-smoothed annotations only for the first quarter note
    ticks = df.loc[df['quarter note']==1]
    # Find peaks in both signals
    peaks_x = signal.find_peaks_cwt(df['non-expert'], widths=[window])
    peaks_y = signal.find_peaks_cwt(df['expert'], widths=[window])

    # Plot the peaks along the original annotations of the two groups
    plt.figure(figsize=(40,5))
    plt.plot(df['non-expert'], label='non-experts',color='blue', alpha = 0.5)
    plt.plot(df['expert'], label='experts', color='red', alpha = 0.5)
    plt.plot(peaks_x, df['non-expert'][peaks_x], "ob", label='non-experts')
    plt.plot(peaks_y, df['expert'][peaks_y], "or", label='experts')
    plt.plot(df.loc[df['reference']!=0]['reference'], 'Dg', label='reference')
    plt.xticks(ticks.index, ticks.measure, fontsize=8, rotation = 45)
    plt.grid(axis = "x")
    plt.legend()
    plt.title('Work '+ title)
    plt.xlabel('measure', fontsize=16)
    plt.ylabel('mean weight', fontsize=16)
    plt.savefig(os.path.join('..', 'results', 'figures', 'peaks_'+filename+'.png'))
    plt.close()

    # Save the peaks to a log file
    d = {'non-expert': peaks_x, 'expert': peaks_y, 'reference': df.loc[df['reference']!=0].index}
    evaluation_input = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
    evaluation_input.to_csv(os.path.join('..', 'data', 'processed', 'peaks', filename+'.csv'))
                        