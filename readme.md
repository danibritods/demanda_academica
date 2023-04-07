# AcaDem
A script to determine the **demand** for each **discipline** of a given course at UENF from the **academic transcripts** of its students.

# Installation 
1. O AcaDem requer Pyhon versão 3.9x. Para instalá-lo, siga as instruções oficiais da linguagem
1. Faça o download dese repositório e acomode a pasta onde desejar 
1. Execute o comando de instalação:
   - ``python setup.py``
# Usage 
To use AcaDem, provide the paths to the course syllabus and the student's transcripts in the `config` file. Then, run the script in your terminal. 

1. Coloque os extratos acadêmicos na pasta "extratos_acadêmicos"
2. Crie a tabela "disciplinas_do_curso.csv" conforme o [exemplo](exemplos/disciplinas_do_curso.csv)
3. Coloque o "arquivo disciplinas_do_curso.csv" na pasta "config" 
4. Execute o script com o comando:
   - ``python academ/academ.py`` 
5. Na pasta "results" estará o aquivo csv com a demanda das disciplinas e o banco de dados gerado.
The script will generate a CSV file with the code and number of students that demand each discipline, as well as a SQLite database file with all the data extracted and produced.

## config
The config file establishes the filepaths of all the files needed for the script. 
### subjects_dict
A dictionary containing each subject's name and prerequisites. 
If present, the script uses those definitions to compute each students demands. 
If absent, the scripts generates this file by extracting this information from the course curriculum pdf. 
 
### dicipline_equivalences
Each dicipline has an ID, in this file we can config equivalences and corrections. For example our curriculum stablish MAT01201 as our Introduction to Statistics, but we studied the same subject with the PRO01121 ID. 

# Folder Structure
```
├── LICENSE
├── README.md                        <- Apresentação do programa
├── config.ini                       <- configuration file
├── academ                           <- Pasta principal 
│   ├── __init__.py                      <- .
│   ├── academ.py                        <- Arquivo principal
│   ├── extratos_aggregate.py            <- Módulo de agregação da demanda
│   ├── extratos_extractor.py            <- Módulo de extração dos dados 
│   ├── files.py                         <- Módulo para manipulação de arquivos
│   └── presentation.py                  <- Módulo para transformação estética dos dados
├── data                            <- Pasta com os dados (opcional) 
│   ├── disciplinas_do_curso.csv         <- Grade curricular do curso
│   ├── disciplinas_equivalentes.csv     <- Tabela de equivalências entre disciplinas
│   └── extratos_academicos              <- Pasta com os extratos acadêmicos
├── results                         <- Pasta com os resultados
│   ├── academ.db                        <- SQLite database file
│   └── demanda_disciplinas_{date}.csv   <- Módulo para transformação estética dos dados
└── requirements.txt                <- Lista dos pacotes necessários 
```
# About
AcaDem was developed as a first step to generate information that assists coordinators and laboratory heads at Universidade Estadual do Norte Fluminense (UENF) in their decision-making process. As the university's academic system does not offer this possibility, I developed a script that extracts the necessary data from documents that coordinators and heads have access to. I tried to keep libraries at a minimum and used vanilla Python instead of Pandas, for example. It was also an interesting exploration of regular expressions and PDF data extraction.
