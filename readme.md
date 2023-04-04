# demanda_academica
Pipeline to automatically extract students data and demand for disciplines from their transcripts. 

# Use
1. Put all the students extracts in the folder "Extratos_Academicos". (We provide mine and João's as example)
2. Run the "Aggregate_Demand.py" script.
3. A csv file with the results will be created in the "Results" folder.

## Config
In the "Config" folder we have two json files:
### subjects_dict
A dictionary containing each subject's name and prerequisites. 
If present, the script uses those definitions to compute each students demands. 
If absent, the scripts generates this file by extracting this information from the course curriculum pdf. 
 
### dicipline_equivalences
Each dicipline has an ID, in this file we can config equivalences and corrections. For example our curriculum stablish MAT01201 as our Introduction to Statistics, but we studied the same subject with the PRO01121 ID. 

# About
This project exist because our academic system currently does not offer a clear visualization of the student's aggregate demand for subjects.
In that regard, my friend @João and I thought about a feaseble way to help our coordinator. As the intent is for him to run this script, I tried to keep libraries at minimum and used vanilla python intead of Pandas for example. It was also an interesting exploration of regular expressions and pdf reading. 

The idea is to automatically extract information from pdfs about attendance and prerequisites to map the exact necessity of each subject by the number of student currently needing them. 

The project is specially relevant in the context of our exception period during the pandemics which brings a layer of complexity to the academic system consider demand. 

Finally this is hopefully a small first step towards a data driven culture that is more precise and confortable to the faculty and staff. 
