# AcaDem
Script para determinar a demanda por cada disciplina de determinado curso da UENF a partir dos extratos acadêmicos de seus alunos.

O AcaDem processa os extratos acadêmicos dos alunos para gerar uma tabela no formato CSV com a sigla e o número de alunos que demandam cada disciplina, além de um arquivo banco de dados SQLite com todos os dados extraídos nesse proceso. 

O AcaDem foi desenvolvido como um primeiro passo para gerar informações que auxiliem coordenadores e chefes de laboratório da Universidade Estatual no Norte Flumense (UENF) em seu processo decisório. Como o sistema da acadêmico da universidade não oferece essa possbilidade, desenvolvi um script que extrai os dados necessários dos documentos que coordenadores e chefes tem acesso

 extratos acadêmicos dos estudantes 

ao fornecer a informação crucial de quantos estudantes demandam cada disciplina. Além disso, o script cria um banco de dados com todos os dados extraidos dos extrados acadêmicos de modo que futuros desenvolvimentos possam mais informações úteis para informar o processo decisório. 

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


# About
This project exist because our academic system currently does not offer a clear visualization of the student's aggregate demand for subjects.
In that regard, my friend @João and I thought about a feaseble way to help our coordinator. As the intent is for him to run this script, I tried to keep libraries at minimum and used vanilla python intead of Pandas for example. It was also an interesting exploration of regular expressions and pdf reading. 

The idea is to automatically extract information from pdfs about attendance and prerequisites to map the exact necessity of each subject by the number of student currently needing them. 

The project is specially relevant in the context of our exception period during the pandemics which brings a layer of complexity to the academic system consider demand. 

Finally this is hopefully a small first step towards a data driven culture that is more precise and confortable to the faculty and staff. 
