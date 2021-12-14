from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import json
import csv
import re
import os


def Read_Files_in_Folder():
    files = os.listdir()
    return files

def Read_JSON_to_Dict(json_file):
    try:
        with open(json_file,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return -1  

def Save_Dict_to_JSON(dict,json_file):
    with open(json_file,'w') as f:
        json.dump(dict,f)

def Save_CSV(table,csv_file_name):
    with open(csv_file_name,'w') as csvfile:
        writer = csv.writer(csvfile) 
        for row in table:
            writer.writerow(row)
    print("'"+csv_file_name+"'","sucessfuly written!")

def Subject_Dict_prerequisites_names(files):
    '''Return a subjects_dict with the subject keys, names and prerequisites'''
    def _Build_prerequisites_names_Dict(matriz_pdf):
        '''Build the subject database, with the subject key, name and prerequitites'''
        laparams = LAParams(line_overlap=0.5,
        char_margin=500, line_margin=2, word_margin=0.5,
        boxes_flow=0.5, detect_vertical=False, all_texts=False)
        text = extract_text(matriz_pdf,laparams=laparams)

        #This first expression fixes the side effect of the pdf reader putting prerequisites in new lines
        #substitute the newline for a comma just between prerequisites
        exp = r",\n[A-Z]{3}\d{5}"
        def repl(m):
            #print(m.group(0)[2:])
            return(","+m.group(0)[2:])

        fixed_prerequisites=re.sub(exp,repl,text)
        
        exp2 = r"[A-Z]{3}\d{5}.*[A-Z]{3}\d{5}"
        subjects_prerequisites = re.findall(exp2,fixed_prerequisites,re.M) 
        subjects_prerequisites

        #~improove this repetition of .split()~
        #prerequisites = {x.split()[0]:x.split()[-1] for x in subjects_prerequisites}
        prerequisites = {x[0]:x[-1].split(",") for x in [y.split() for y in subjects_prerequisites]}
        subject_names = {x[0]:x[-2] for x in [y.split() for y in subjects_prerequisites]}
        subject_dict = {"names":subject_names,"prerequisites":prerequisites}

        Save_Dict_to_JSON(subject_dict,"subjects_dict.json")
        print("'subjects_dict.json' sucssesfully built and loaded.")
        return subject_dict 

    dict = Read_JSON_to_Dict("subjects_dict.json")
    if dict == -1:
        matriz_pdf = [pdf for pdf in files if "Matriz" in pdf][0]
        if matriz_pdf == []:
            #return "Error! Neither 'subjects_dict.json' nor MatrizCurricular were not found."
            return -1
        else:
            print("'subjects_dict.json' not found. Lets build it!")
            return _Build_prerequisites_names_Dict(matriz_pdf)
    else:
        print("'subjects_dict.json' sucssesfully loaded.")
        return dict 

def Extratos(files):     
    files = os.listdir()
    pdfs = [file for file in files if file[-3:] == "pdf"]
    #extratos = ["extrato_escolar.pdf","Ext_-_JVFD.pdf","extrato_ze.pdf"]
    extratos = [pdf for pdf in pdfs if "Matriz" not in pdf]
    return extratos 

def Aggregate_Demand(extratos,prerequisites):
    def _Approved_Subjects(student_extract_pdf):
        '''Return approved subject keys from the academic extract'''
        #Ideal layout parameters:
        laparams = LAParams(line_overlap=0.5,
            char_margin=95.0, line_margin=2, word_margin=0.5,
            boxes_flow=0.5, detect_vertical=False, all_texts=False)
        #Reading pdf to string
        extract = extract_text(student_extract_pdf,laparams=laparams)

        #Filter from "extrato" all the lines begining with a subject key
        attended_subjects = re.findall(r"[A-Z]{3}\d{5}.*",extract) #print(attended_subjects)
        #Filter the approved subjects and the subjects exempt through the special pandemic period (AAREs) 
        approved_subjects = [att_sub.split(" ",1)[0] for att_sub in attended_subjects if ("APR" in att_sub or len(att_sub) == 12)]
        return approved_subjects 

    def _Subjects_Demand(prerequisites,approved_subjects):
        '''Finds the subjects the student have the possibility to attend.
        That is, unnatended subjects that the student already has the prerequisites'''
        def Is_sublist(sublist,list):
            return set(sublist) <= set(list)

        subjects_demand = [subject for subject in prerequisites.keys() if 
        (subject not in approved_subjects and Is_sublist(prerequisites[subject],approved_subjects))] 
        return subjects_demand

    aggregate_demand = {}
    i = 0 
    for extrato in extratos:
        approved_subjects = _Approved_Subjects(extrato)
        subjects_demand = _Subjects_Demand(prerequisites,approved_subjects)
        for subject in subjects_demand:
            if subject not in aggregate_demand:
                aggregate_demand[subject] = 1 
            else:
                aggregate_demand[subject] += 1
        print(i+1,"Extracts processed.")
        i+=1
    print("Aggregate Demand sucssesfully calculated.\nResults preview:")
    return aggregate_demand

def Final_Demand(aggregate_demand,subject_dict):
    final_demand = [["Sigla","Diciplina","Demanda"]]
    print(final_demand[-1])
    for subject,demand in aggregate_demand.items():
        final_demand.append([subject,subject_dict["names"][subject],demand])
        print(final_demand[-1])
    
        
    Save_CSV(final_demand,"RESULTS_aggregate_demand.csv")

def main():
    files = Read_Files_in_Folder()
    subject_dict = Subject_Dict_prerequisites_names(files)
    if subject_dict == -1:
        return "Error! Neither 'subjects_dict.json' nor MatrizCurricular were found in the current folder:\n"+os.getcwd()
    else:
        extratos = Extratos(files)
        aggregate_demand = Aggregate_Demand(extratos,subject_dict["prerequisites"])
        Final_Demand(aggregate_demand,subject_dict)

main()

    

