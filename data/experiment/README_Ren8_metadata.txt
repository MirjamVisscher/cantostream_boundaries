=== Metadata Ren8 dataset ===

--- Files ---
Ren8_acquaintance_difficulty.csv: acquaintance and perceived difficulty to annotate the works
Ren8_annotations.csv: annotations of the works. This is the core of the dataset
Ren8_boundary_survey.txt: survey questions to measure the musical experience of the participants
Ren8_instructions.txt: instructions as given to the participants during the experiment
Ren8_sheet_music: folder containing the sheet music of the eight works in the experiment
Ren8_survey_answers.csv: participants’ answers to the survey about their musical experience
Ren8_works.csv: description of the works and the recordings used

--- Audio files ---

The recordings used are proprietary material and will not be shared in this dataset, the playlist of the experiment is on spotify: https://open.spotify.com/playlist/5vJzuTQ345fW8iwbWx6UIn?si=ac1cd856ef17484a

--- More about Ren8_annotations.csv ---

The file Ren8_annotations.csv contains all human annotations and the algorithms' boundaries aggregated to quarter notes.
The human annotations are collected by hand, using sheet music. We refer to Visscher & Wiering (2023) for a full description of the method and limitation of this data.

global_unit	nth quarter note in the total dataset, starting with 0
work		work number, values 1-8
work_unit	nth quarter note in the work, starting with 0
Measure	measure in the sheet music in this dataset
quarter note	nth quarter note in the work, starting with 1
timestamp	timestamp in seconds in the recordings used for this experiment
n1 - n13	non-expert participant 1 to 13, numbers are the assigned weights of the boundaries, with values 1-4
e1 - e8	expert participant 1 to 8
s1 - s4	student participant 1 to 4	
reference	music theoretical reference
Expert		average weight of expert boundaries
Non-expert	average weight of non-expert boundaries
total		average weight of expert and non-expert boundaries
cnmf		total number of boundaries assigned to this quarter note by the CNMF algorithm in the MSAF library
example	total number of boundaries assigned to this quarter note by the example algorithm in the MSAF library
foote		total number of boundaries assigned to this quarter note by the Foote algorithm in the MSAF library
olda		total number of boundaries assigned to this quarter note by the OLDA algorithm in the MSAF library
scluster	total number of boundaries assigned to this quarter note by the SCluster algorithm in the MSAF library
sf		total number of boundaries assigned to this quarter note by the SF algorithm in the MSAF library
vmo		total number of boundaries assigned to this quarter note by the VMO algorithm in the MSAF library




