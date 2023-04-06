# AcaDem
A script to determine the **demand** for each **discipline** of a given course at UENF from the **academic transcripts** of its students.

# Installation 

# Usage

To use AcaDem, you only need to provide the paths to the course syllabus and the transcripts and run the script in your terminal. 

The script will generate a CSV file with the code and number of students that demand each discipline, as well as a SQLite database file with all the data extracted and produced.

# About

AcaDem was developed as a first step to generate information that assists coordinators and laboratory heads at Universidade Estadual do Norte Fluminense (UENF) in their decision-making process. As the university's academic system does not offer this possibility, I developed a script that extracts the necessary data from documents that coordinators and heads have access to. I tried to keep libraries at a minimum and used vanilla Python instead of Pandas, for example. It was also an interesting exploration of regular expressions and PDF data extraction.



Script to automatically extract students data and their demand for subjects from their college transcripts. It builds a sqlite database with all the data and a csv with the number of students demanding each course subjects. 

# About

AcaDem is a script that processes **academic transcripts** of students to generate a **CSV table** with the abbreviation and number of students that demand each discipline. Additionally, it creates an **SQLite database** file with all the data extracted in this process. The script was developed as a first step to generate information that assists coordinators and laboratory heads at the State University of Northern Fluminense (UENF) in their decision-making process. As the academic system of the university does not offer this possibility, I developed a script that extracts the necessary data from documents that coordinators and heads have access to.



Script para determinar a demanda por cada disciplina de determinado curso da UENF a partir dos extratos acadêmicos de seus alunos.
O AcaDem processa os extratos acadêmicos dos alunos para gerar uma tabela no formato CSV com a sigla e o número de alunos que demandam cada disciplina, além de um arquivo banco de dados SQLite com todos os dados extraídos nesse proceso de modo que futuros desenvolvimentos possam mais informações úteis para informar o processo decisório. 
O AcaDem foi desenvolvido como um primeiro passo para gerar informações que auxiliem coordenadores e chefes de laboratório da Universidade Estatual no Norte Flumense (UENF) em seu processo decisório. Como o sistema da acadêmico da universidade não oferece essa possbilidade, desenvolvi um script que extrai os dados necessários dos documentos que coordenadores e chefes tem acesso
This project exist because our academic system currently does not offer a clear visualization of the student's aggregate demand for subjects.
 I tried to keep libraries at minimum and used vanilla python intead of Pandas for example. It was also an interesting exploration of regular expressions and pdf reading. 
The idea is to automatically extract information from pdfs about attendance and prerequisites to map the exact necessity of each subject by the number of student currently needing them. 
Finally this is hopefully a small first step towards a data driven culture that is more precise and confortable to the faculty and staff. 
## Instalação
1. O AcaDem requer Pyhon versão 3.9x. Para instalá-lo, siga as intruções oficiais da linguagem
1. Faça o download dese repositório e acomode a pasta onde desejar 
1. Execute o comando de instalação:
   - ``python setup.py``

## Uso
1. Coloque os extratos acadêmicos na pasta "extratos_acadêmicos"
2. Crie a tabela "disciplinas_do_curso.csv" conforme o [exemplo](exemplos/disciplinas_do_curso.csv)
3. Coloque o "arquivo disciplinas_do_curso.csv" na pasta "config" 
4. Execute o script com o comando:
   - ``python academ/academ.py`` (linux/mac)
   - ``py academ\academ.py`` (windows)
5. Na pasta "results" estará o aquivo csv com a demanda das disciplinas e o banco de dados gerado.



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
# Folder Structure

```
├── LICENSE
├── README.md                        <- Apresentação do programa
├── academ                         <- Pasta principal 
│   ├── __init__.py                      <- .
│   ├── academ.py                        <- Arquivo principal
│   ├── extratos_aggregate.py            <- Módulo de agregação da demanda
│   ├── extratos_extractor.py            <- Módulo de extração dos dados 
│   ├── files.py                         <- Módulo para manipulação de arquivos
│   └── presentation.py                  <- Módulo para transformação estética dos dados
├── config                        <- Pasta de configuração
│   └── disciplinas_do_curso.csv    <- Grade curricular do curso
├── extratos_academicos           <- Pasta com os extratos acadêmicos
├── results                       <- Pasta com os resultados
└── requirements.txt                <- Lista dos pacotes necessários 
```
