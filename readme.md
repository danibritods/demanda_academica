# demanda_academica
Automatically assess and agregate the demand for each subject in UENF's Computer Science course curriculum. 

# Use
1. Put all the students extracts in the folder "Extratos_Academicos". (We provide mine and João's as example)
2. Run the "Aggregate_Demand.py" script.
3. A csv file with the results will be created in the "Results" folder.

## Config
In the "Config" folder we can manually change the criterea automatically generated from the "2014-MatrizCurricularComputacao.pdf" file. 

# About
This project exist because our academic system currently does not offer a clear visualization of the student's aggregate demand for subjects.
In that regard, my friend @João and I thought about a feaseble way to help our coordinator.
The idea is to automatically extract information from pdfs about attendance and prerequisites to map the exact necessity of each subject by the number of student currently needing them. 

The project is specially relevant in the context of our exception period during the pandemics which brings a layer of complexity to the academic system consider demand. 

Finally this is hopefully a small first step towards a data driven culture that is more precise and confortable to the faculty and staff. 
