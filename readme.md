# AcaDem
A script to determine the **demand** for each **subject** of a given course at UENF from the **academic transcripts** of its students.

# Installation 
1. Install Python 3.9
2. Clone this repo
3. Run the setup script:  
   - ```python setup.py```

# Usage 
To use AcaDem, provide the paths to the course syllabus and the student's transcripts in the `config` file. Then, run the script in your terminal. 
The script will generate a CSV file with the code and number of students that demand each subject, as well as a SQLite database file with all the data extracted and produced. Both located at the `results` folder. 

1. Prepare a folder with students academic transcripts 
2. Prepare the `disciplinas_do_curso.csv`. A file with the subjects code and their prerequisites following our [example]
3. Optionally prepare the `disciplinas_equivalentes.csv`. A file establishing the equivalence between subjects. 
4. Provide the filepaths for prepared files in the `config.ini` file. 
5. Run the script in your terminal: ```python academ/academ.py```


## config
The config file establishes the filepaths of all the files needed for the script. 

### `disciplinas_do_curso.csv`
Table containing course's each subject, its code, name and pre requisites. This file should follow the this structure. Alternatively the user can provide the course syllabus, 

This file has to be built and the user. Alternatively by providing the course's syllabus the script generates the file. 

### subjects_dict
A dictionary containing each subject's name and prerequisites. 
If present, the script uses those definitions to compute each students demands. 
If absent, the scripts generates this file by extracting this information from the course curriculum pdf. 
 
### dicipline_equivalences
Each dicipline has an ID, in this file we can config equivalences and corrections. For example our curriculum stablish MAT01201 as our Introduction to Statistics, but we studied the same subject with the PRO01121 ID. 

# Folder Structure
```
├── README.md                        <- Program overview 
├── config.ini                       <- Configuration file
├── academ                           <- Main folder
│   ├── __init__.py                      <- Python file 
│   ├── academ.py                        <- Main code
│   ├── extratos_aggregate.py            <- Data aggregation module
│   ├── extratos_extractor.py            <- Data extraction module
│   ├── files.py                         <- File manipulation module
│   └── presentation.py                  <- Format and styling module
├── data                             <- Data folder 
│   ├── disciplinas_do_curso.csv         <- subjects from the course curriculum
│   ├── disciplinas_equivalentes.csv     <- Table of equivalences between subjects
│   └── extratos_academicos              <- Folder with the academic transcripts
├── results                          <- Results folder 
│   ├── academ.db                        <- SQLite database file
│   └── demanda_disciplinas_{date}.csv   <- Table with subjects demand
└── requirements.txt                 <- List of the required packages  
```
# About
AcaDem was developed as a first step to generate information that assists coordinators and laboratory heads at Universidade Estadual do Norte Fluminense (UENF) in their decision-making process. As the university's academic system does not offer this possibility, I developed a script that extracts the necessary data from documents that coordinators and heads have access to. I tried to keep libraries at a minimum and used vanilla Python instead of Pandas, for example. It was also an interesting exploration of regular expressions and PDF data extraction.
