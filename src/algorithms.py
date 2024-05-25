#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on June 2023
Function to run the selected algorithms on the selected audio file

The tasks of this script are:
1 Read the audio files
2 Process the audio files with the given algorithm
3 Write the found boundaries into a DataFrame
@author: MirjamVisscher libgoncalv
"""

import msaf
import os
import numpy as np
import pandas as pd
import random

def run_algorithms(filename, algorithms):
    random.seed(131)
    np.random.seed(131)
    print('Running msaf algorithms for '+ filename + '... This step may take some time.')
    # Set the float precision to 0.01
    np.set_printoptions(precision=2) 
    # Create a DataFrame with all the algorithm boundaries
    algo_result = pd.DataFrame()
    audio_file = os.path.join('..', 'data', 'raw', 'audio', filename+'.wav')
    # For each algorithm
    for algo in algorithms:
        # Execute the i algorithm on the audio_file
        boundaries, _ = msaf.process(audio_file, boundaries_id=algo)
        # Create a DataFrame ordered by the timestamp
        df = pd.DataFrame(np.array(boundaries), columns=['timestamp'])
        df['algorithm'] = algo
        df['weight'] = 1.0
        # Add the obtained boundaries to the result DataFrame
        algo_result = pd.concat([algo_result, df], ignore_index=True)  
    # Save result to the log file
    algo_result.to_csv(os.path.join('..', 'data', 'processed', 'boundaries', filename+'.csv'))
    return(algo_result)