#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to compute the distance between all the annotations and boundaries

The tasks of this script are:
1 Read the smoothed annotations and boundaries file
2 Create a distance matrix
3 Compute the similarity under the curves of two annotations/boundaries
4 Save the matrix to a log file
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os
import numpy as np
import itertools
import similaritymeasures


def compute_distances(filename):
    print('Running the distances computation for '+filename+ '... This step may take some time.')
    df = pd.read_csv(os.path.join('..', 'data', 'processed', 'smoothed_annotations', 'individual_'+filename+'.csv'))
    # truncate to exclude smoothing artifacts
    df=df.iloc[4: -25,  :]
    index = df.columns.to_list()[1:]
    # Create a matrix of the size of the number of individual annotations + algorithm boundaries
    distance_matrix = np.full((len(index), len(index)), np.nan)
    counter = np.arange(len(df.index))
    # Create a vector with 2 columns and the number of points for the smoothed annotations
    # First column corresponds the x axis and second column to the y axis
    ind1_data = np.zeros((len(counter), 2))
    ind1_data[:, 0] = counter
    # Same as the first vector
    ind2_data = np.zeros((len(counter), 2))
    ind2_data[:, 0] = counter
    # For each possible combination of annotations/boundaries
    for ind1, ind2 in itertools.combinations_with_replacement(index,2):
        ind1_data[:, 1] = df[ind1]#pak even niet de laatste 8
        ind2_data[:, 1] = df[ind2]
        # Compute the area under the curve
        area = similaritymeasures.area_between_two_curves(ind1_data, ind2_data)
        # Add the normalised value to the matrix. The normalisation unit is the quarter note
        distance_matrix[index.index(ind1)][index.index(ind2)] = area/len(counter)
        distance_matrix[index.index(ind2)][index.index(ind1)] = area/len(counter)
    # Set to zero very low values
    distance_matrix[distance_matrix < 0.0001] = 0.0
    # Save it to log file
    distance_matrix = pd.DataFrame(distance_matrix, columns=index, index=index)
    return(distance_matrix)
    distance_matrix.to_csv(os.path.join('..', 'data', 'processed', 'distances', 'individual_'+filename+'.csv'))