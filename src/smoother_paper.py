#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 20:55:00 2024
The task of this script is to draw a plot for the boundaries paper.
@author: mirjam
"""
# import os
# import pandas as pd
# from tsmoothie.smoother import GaussianSmoother
# import matplotlib.pyplot as plt

# sigma = 0.002 # Gaussian smoothing: higher is more smoothed, 0.002 is default for this project

# lower = 39*8 #first measure to show
# upper = 59*8 #last measure to show

# filename = 'w3' #choose between w1-w8
# algorithms = ['cnmf', 'foote', 'olda', 'scluster', 'sf', 'vmo']

# #read, select and transpose the data
# annotations = pd.read_csv(os.path.join('..', 'data', 'processed', 'join', filename+'.csv'))
# ticks = (annotations.loc[annotations['quarter note'] == 1][['Unnamed: 0', 'measure']]
#          .rename(columns={'Unnamed: 0': 'given_index'})
#          )
# annotations = annotations[['expert', 'non-expert']+algorithms].transpose()

# #smooth the data
# smoother = GaussianSmoother(n_knots=len(annotations.columns), sigma=sigma)
# smoother.smooth(annotations)
# plotpoints = smoother.smooth_data

# #define the plot characteristics
# linestyles = ['-', '--','-.', ':',':']#define linestyles to cycle through
# plt.style.use('grayscale')
# plt.figure(figsize=(6.5, 6), facecolor='white')

# # plot the first pane with the experts and non-experts
# ax1 = plt.subplot(211)
# for i, h in enumerate(['expert', 'non-expert']):
#     plt.plot(plotpoints[i], label=h, alpha=0.7)
# plt.xticks(ticks.given_index, ticks.measure, fontsize=8)
# ax1.set_xlim(lower, upper) #cut to the measures I want to show
# ax1.set(ylim=(-0.1, 0.3))
# plt.legend(loc=1)

# # plot the second pane with the algorithms
# ax2 = plt.subplot(212, sharex=ax1)
# for i, a in enumerate(algorithms):
#     linestyle = linestyles[i % len(linestyles)]
#     plt.plot(plotpoints[2 + i], label=a, alpha=0.7, linestyle=linestyle)
# ax2.set(ylim=(-0.5, 1.5))
# ax2.set_xlim(lower, upper) #cut to the measures I want to show
# plt.legend(loc='best')
# plt.xlabel('measure')

# plt.savefig(os.path.join('..', 'results', 'figures', 'paper', 'humans and algorithms ' + filename + '.png'))
# plt.show()
# plt.close()

import os
import pandas as pd
from tsmoothie.smoother import GaussianSmoother
import matplotlib.pyplot as plt

def gaussian_curves_paper(filename, algorithms, sigma=0.002, lower=None, upper=None):
    """
    Draw a plot showing boundaries based on given filename and algorithms.

    Parameters:
    - filename (str): The name of the file (without extension) containing the data.
    - algorithms (list): List of algorithm names.
    - sigma (float): Standard deviation for Gaussian smoothing.
    - lower (int): Index of the lower bound for measures to show.
    - upper (int): Index of the upper bound for measures to show.
    """

    # Default lower and upper bounds if not provided
    if lower is None:
        lower = 39 * 8
    if upper is None:
        upper = 59 * 8

    # Read, select, and transpose the data
    annotations = pd.read_csv(os.path.join('..', 'data', 'processed', 'join', filename + '.csv'))
    ticks = (annotations.loc[annotations['quarter note'] == 1][['Unnamed: 0', 'measure']]
             .rename(columns={'Unnamed: 0': 'given_index'})
             )
    annotations = annotations[['expert', 'non-expert'] + algorithms].transpose()

    # Smooth the data
    smoother = GaussianSmoother(n_knots=len(annotations.columns), sigma=sigma)
    smoother.smooth(annotations)
    plotpoints = smoother.smooth_data

    # Define plot characteristics
    linestyles = ['-', '--', '-.', ':', ':']  # Define linestyles to cycle through
    plt.style.use('grayscale')
    plt.figure(figsize=(6.5, 6), facecolor='white')

    # Plot the first pane with the experts and non-experts
    ax1 = plt.subplot(211)
    for i, h in enumerate(['expert', 'non-expert']):
        plt.plot(plotpoints[i], label=h, alpha=0.7)
    plt.xticks(ticks.given_index, ticks.measure, fontsize=8)
    ax1.set_xlim(lower, upper)  # Cut to the measures I want to show
    ax1.set(ylim=(-0.1, 0.3))
    plt.legend(loc=1)

    # Plot the second pane with the algorithms
    ax2 = plt.subplot(212, sharex=ax1)
    for i, a in enumerate(algorithms):
        linestyle = linestyles[i % len(linestyles)]
        plt.plot(plotpoints[2 + i], label=a, alpha=0.7, linestyle=linestyle)
    ax2.set(ylim=(-0.5, 1.5))
    ax2.set_xlim(lower, upper)  # Cut to the measures I want to show
    plt.legend(loc='best')
    plt.xlabel('measure')

    plt.savefig(os.path.join('..', 'results', 'paper', 'humans and algorithms ' + filename + '.png'))
    plt.show()
    plt.close()


