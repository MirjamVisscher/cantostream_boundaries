#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to join the algorithm boundaries with the human annotations

The tasks of this script are:
1 Read the boundaries file
2 Process the boundaries to put it in the same format as the annotations
3 Read the annotations file
4 Process the annotations file to create expert and non-expert metrics
5 Merge the boundaries and annotations files based on the timestamp
@author: MirjamVisscher libgoncalv
"""

import pandas as pd
import os

def join_algorithms_annotations(filename, experts, nonexperts):
        print('Running join for '+filename+ '...')
        # Open boundaries file
        boundaries_file = os.path.join('..', 'data', 'processed', 'boundaries', filename+'.csv')
        boundaries = pd.read_csv(boundaries_file).fillna(0)
        boundaries = boundaries.sort_values(by=['timestamp'])
        # Open annotations files
        annotations_file = os.path.join('..', 'data', 'raw', 'annotations', filename+'.csv')
        annotations = pd.read_csv(annotations_file).fillna(0)
        annotations = annotations.sort_values(by=['timestamp'])
        # annotations = annotations.drop(['stamp', 'step', 'stepfull'], axis=1)

        # Creation of temporary column to merging the files
        annotations['merge_unit'] = list(range(len(annotations['timestamp'])))
        # When merged, the temporary column allow to match several boundaries to the same annotations
        temp_merge = pd.merge_asof(boundaries, annotations, on=['timestamp'], direction='nearest')
        # Only keep 3 culumns
        temp_merge = temp_merge[["merge_unit", 'algorithm', 'weight']]
        # Sum the weights of the boundaries happening at the same merged_unit 
        # This synchronize the boundaries timestamps on the annotations timestamps 
        temp_merge = temp_merge.groupby(['merge_unit', 'algorithm']).count()
        # Pivot the DataFrame in order to have a column per algorithm
        boundaries = temp_merge.pivot_table(index='merge_unit', columns='algorithm', values='weight').fillna(0)
        
        # Compute the mean value of annotations within each group
        annotations['expert'] = annotations[experts].mean(axis=1)
        annotations['non-expert'] = annotations[nonexperts].mean(axis=1)
        annotations['total human'] = annotations[experts+nonexperts].mean(axis=1)
        # Join the boundaries with the annotations
        result = annotations.merge(boundaries, how='left', on=['merge_unit']).fillna(0)
        result = result.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.2', 'index', 'weight', 'merge_unit'], axis=1, errors='ignore')
        # Save result to the log file
        result.to_csv(os.path.join('..', 'data','processed', 'join', filename+'.csv'))
        return(result)