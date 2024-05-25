#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to smooth the annotations with a Gaussian kernel

The tasks of this script are:
1 Read the join file
2 Smooth the data with a Gaussian kernel
3 Plot the groups smoothed annotations
4 Plot the algorithm smoothed annotations
5 Plot the groups smoothed annotations only for the first quarter note
6 Save the smoothed annotations and boundaries to log file
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from tsmoothie.smoother import GaussianSmoother

def smooth_annotations(filename, title, algorithms, experts, nonexperts, sigma=0.002):
    print('Running smoothing for '+filename+ '...')
    df = pd.read_csv(os.path.join('..', 'data', 'processed', 'join', filename+'.csv'))
    # Select only the groups annotations and algorithm boundaries
    data = df[['total human', 'expert', 'non-expert', 'reference']+algorithms]
    # Transpose the DataFrame to have a row for each colums
    data =  data.transpose()
    ticks = df.loc[df['quarter note']==1]
    # Smooth all the annotations and boundaries
    smoother = GaussianSmoother(n_knots=len(data.columns), sigma=sigma)
    smoother.smooth(data)
    plotpoints = smoother.data.astype('float')
    # Set all points equal to 0 a NaN value in order to not plot them
    plotpoints[plotpoints == 0] = 'nan'
    
    # Plot the groups smoothed annotations
    plt.style.use('Solarize_Light2')
    plt.figure(figsize=(20,5))
    plt.title(title+': human annotations and algorithm boundaries\n')
    ax1 = plt.subplot(211)
    # ax1.set(ylim=(-0.1,0.3))
    # ax1.set(xlim=(300, 500), ylim=(-0.1,0.3))
    for i, h in enumerate(['expert', 'non-expert', 'reference']):
        plt.plot(smoother.smooth_data[1+i], label=h, alpha=0.7)
        plt.plot(plotpoints[1+i], '.', label=h, alpha=0.6)
    plt.legend()
    plt.title(title)
    plt.ylabel('smoothed weight', fontsize=16)
    # Plot the algorithm smoothed annotations
    ax2 = plt.subplot(212, sharex=ax1)
    # ax2.set(ylim=(-0.2,0.5))
    for i, a in enumerate(algorithms):
            plt.plot(smoother.smooth_data[4+i], label=a, alpha=0.7)
            plt.xticks(ticks.index, ticks.measure, fontsize=8)
            plt.plot(plotpoints[4+i], '.', label=a, alpha = 0.6)
    plt.legend()
    plt.xlabel('quarter note', fontsize=16)
    plt.ylabel('smoothed weight', fontsize=16)
    # Save it to output file
    plt.savefig(os.path.join('..', 'results', 'figures', 'humans and algorithms '+filename+'.png'))
    plt.close()

    # Plot the smoothed annotations per group
    ticks = df.loc[df['quarter note']==1]
    plt.figure(figsize=(40,5))
    for i, g in enumerate(['total human', 'expert', 'non-expert', 'reference']):
        plt.plot(smoother.smooth_data[i], label=g, alpha=0.7)
        plt.xticks(ticks.index, ticks.measure, fontsize=8)
        plt.plot(plotpoints[i], '.', label=g, alpha=0.6)
    plt.title(title+': grouped human annotations and reference')
    plt.xlabel('measure', fontsize=16)
    plt.ylabel('weight', fontsize=16)
    plt.legend()
    plt.xticks(ticks.index, ticks.measure, fontsize=8)
    # Save it to output file
    plt.savefig(os.path.join('..', 'results', 'figures', 'gauss_humans_'+filename+'.png'))
    plt.close()

    # Save only the groups annotations and algorithm boundaries
    smoothed_annotations = pd.DataFrame(smoother.smooth_data.T, columns=['total human', 'expert', 'non-expert', 'reference']+algorithms)
    smoothed_annotations.to_csv(os.path.join('..', 'data', 'processed', 'smoothed_annotations', 'group_'+filename+'.csv'))
    # Select the individual annotations and algorithms boundaries
    data = df[['reference']+experts+nonexperts+algorithms]
    data =  data.transpose()
    smoother = GaussianSmoother(n_knots=len(data.columns), sigma=sigma)
    smoother.smooth(data)
    # Save the individual annotations and algorithm boundaries
    smoothed_annotations = pd.DataFrame(smoother.smooth_data.T, columns=['reference']+experts+nonexperts+algorithms)
    smoothed_annotations.to_csv(os.path.join('..', 'data', 'processed', 'smoothed_annotations', 'individual_'+filename+'.csv'))