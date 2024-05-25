# CANTOSTREAM Boundaries
Version 1.0.0

In CANTOSTREAM Boundaries we analyse how humans perceive boundaries in music. Is there a distinction between boundaries indicated by experts versus non-experts? And how do these human boundaries relate to those indicated by a selection of boundary detectors?

## Manual
### Prerequisites
- python 3.10
- [msaf](https://github.com/urinieto/msaf)
- tsmoothie
- similaritymeasures
- mir_eval

### Installation
There are two options to get this package:
1. Download the zip file, using the green button "<> Code" and unzip it in a folder of your preference
2. Or alternatively, install using git 
```git clone https://github.com/MirjamVisscher/cantostream_boundaries.git```

### Operating instructions
1. Install all prerequisites
2. Put the audio files in .wav format in the [audio folder](/data/raw/audio/). The audio files are not provided due to prorietary reasons. The recording details are to be found in the [metadata](/data/raw/metadata/)
3. Execute main.py
4. Find the results in the [results folder](/results/)
 
### Use the code to analyse own annotations
1. Modify in main.py the names of the audio files and annotations you want to use
2. Put the audio files in .wav format in the [audio folder](/data/raw/audio/)
3. Put your .csv containing the human annotations in the [annotation folder](/data/annotations/)
    
## Project organization
```
.
├── CITATION.md                      
├── LICENSE.md                       	<- the licence of this project
├── README.md                        	<- your guide through this project
├── data
│   ├── experiment                   	<- survey data, experiment instructions
│   │   └── Ren8_sheet_music		<- sheet music used in this experiment
│   ├── processed                    	<- processed data, output of the functions
│   │   ├── boundaries               	<- msaf boundaries with default settings
│   │   ├── distances                	<- pairwise distances between annotators
│   │   ├── join                     	<- separate files joined into one file
│   │   ├── peaks                    	<- peaks of the participants' annotations
│   │   └── smoothed_annotations     	<- peaks in the time series of the participants' annotations
│   ├── raw                          	<- input data
│   │   ├── annotations              	<- annotations by the participants of the experiment 
│   │   ├── audio                   	<- (not inlcuded)
│   │   ├── estimations              	<- a work folder, needed by the msaf library
│   │   └── metadata                   	<- description of the compositions in the analysis
│   └── temp
├── results				<- results of the experiment
│   ├── figures                      	<- figures for a visual inspection of the data and the results
│   └── output                       	<- evaluation of the algorithms and the non-experts
│   └── paper				<- figures and numbers as published in the [paper](/CITATION.md)
└── src					<- source code, start with main.py

```
### File description of data in Experiment folder
| File name       			| Description                                                                	|
|---------------------------------------|-------------------------------------------------------------------------------|
| Ren8_acquaintance_difficulty.csv	| participant acquaintance and perceived difficulty to annotate the works	|
| Ren8_annotations.csv			| boundary annotations of the works. This is the core of the dataset		|
| Ren8_boundary_survey.txt		| survey questions to measure the musical experience of the participants	|
| Ren8_instructions.txt			| instructions as given to the participants during the experiment		|
| Ren8_sheet_music			| folder containing the sheet music of the eight works in the experiment	|
| Ren8_survey_answers.csv		| participants’ answers to the survey about their musical experience		|
| Ren8_works.csv   			| description of the works and the recordings used				|


### Audio files 
The recordings used are proprietary material and will not be shared in this dataset, the playlist of the experiment is on [Spotify](https://open.spotify.com/playlist/5vJzuTQ345fW8iwbWx6UIn?si=ac1cd856ef17484a), the metadata of the works and the recordings used is described in [Ren8_works.csv](/data/raw/Ren8_works.csv). In case you want to use the audio files originally used for the paper, please send an email to m.e.visscher @ uu.nl.


### Metadata of annotations in Ren8_annotations.csv
The file Ren8_annotations.csv contains all human annotations and the algorithms' boundaries aggregated to quarter notes.
The human annotations are collected by hand, using sheet music. We refer to Visscher & Wiering (2024) for a full description of the method and limitations of this data.


| Column       | Description                                                                                                    | Value domain |
|--------------|----------------------------------------------------------------------------------------------------------------|--------------|
| global_unit  | Nth quarter note in the total dataset                                                                          | [0,∞)        |
| work         | Work number, according to the list in the article                                                              | 1-8          |
| work_unit    | Nth quarter note in the work, starting with 0                                                                  | [0,∞)        |
| Measure      | Nth measure in the sheet music in this dataset                                                                 | [0,∞)        |
| quarter note | Nth quarter note in the work, starting with 1                                                                  | [1,∞)        |
| timestamp    | Timestamp in seconds in the recordings used for this experiment                                                | [1,∞)        |
| n1 – n13     | Assigned weights of the boundaries by non-expert participant 1 to 13                                           | [1,4]        |
| e1 – e8      | Assigned weights of the boundaries by expert participant 1 to 8                                                | [1,4]        |
| s1 – s4      | Assigned weights of the boundaries by student participant 1 to 4                                               | [1,4]        |
| reference    | Assigned weights of the boundaries, using a structure analysis, by the music theoretical reference participant | [1,2]        |
| expert       | Average weight of expert boundaries                                                                            | [0,4]        |
| non-expert   | Average weight of non-expert boundaries                                                                        | [0,4]        |
| total        | Average weight of expert and non-expert boundaries                                                             | [0,4]        |
| cnmf         | Total number of boundaries assigned to this quarter note by the CNMF algorithm in the MSAF library             | [0,∞)        |
| example      | Total number of boundaries assigned to this quarter note by the example algorithm in the MSAF library          | [0,∞)        |
| foote        | Total number of boundaries assigned to this quarter note by the Foote algorithm in the MSAF library            | [0,∞)        |
| olda         | Total number of boundaries assigned to this quarter note by the OLDA algorithm in the MSAF library             | [0,∞)        |
| scluster     | Total number of boundaries assigned to this quarter note by the SCluster algorithm in the MSAF library         | [0,∞)        |
| sf           | Total number of boundaries assigned to this quarter note by the SF algorithm in the MSAF library               | [0,∞)        |
| vmo          | Total number of boundaries assigned to this quarter note by the VMO algorithm in the MSAF library              | [0,∞)        |

## License

This project is licensed under the terms of te [MIT License](/LICENSE)
This license allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator.

## Citation

Please [cite this project as described here](/CITATION.md).
