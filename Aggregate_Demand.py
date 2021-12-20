from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import json
import csv
import re
import os
log = []
path = "."

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
#-------------------------------------------------

#dicipline_equivalence = {"PRO01121":"MAT01201"}
dicipline_equivalence = Read_JSON_to_Dict(path+"/Config/dicipline_equivalences.json")

#------------------------------------------------
def Correction(target,correction_rules):
    '''Replaces the target substrings in the text according to the correction_rules'''
    fixed_target = target
    for phrase,fixed_phrase in correction_rules.items():
        fixed_target = fixed_target.replace(phrase,fixed_phrase)
    return fixed_target 
    
def Subject_Dict_prerequisites_names(files):
    '''Return a subjects_dict with the subject keys, names and prerequisites'''
    def _Build_prerequisites_names_Dict(matriz_pdf):
        '''Build the subject database, with the subject key, name and prerequitites'''
        laparams = LAParams(line_overlap=0.5,
        char_margin=500, line_margin=2, word_margin=0.5,
        boxes_flow=0.5, detect_vertical=False, all_texts=False)
        matriz_raw = extract_text(matriz_pdf,laparams=laparams)

        #TODO: should we make a global "correction_rules"?
        matriz_correction_rules = {"INF01106 BancodeDadosI":"INF01116 BancodeDadosI",
                "BancodeDadosII INF01106":"BancodeDadosII INF01116",
                "INF01203 4 68\nINF01210 ParadigmaOOparaDesenvolvimentodeSoft-":
                "INF01210 ParadigmaOOparaDesenvolvimentodeSoftware INF01203 4 68"}
        matriz = Correction(matriz_raw,matriz_correction_rules)
        log.append(matriz)

        #This first expression fixes the side effect of the pdf reader putting prerequisites in new lines
        #substitute the newline for a comma just between prerequisites
        exp = r",\n[A-Z]{3}\d{5}"
        def repl(m):
            #print(m.group(0)[2:])
            return(","+m.group(0)[2:])

        fixed_prerequisites=re.sub(exp,repl,matriz)
        log.append(fixed_prerequisites)

        #Regex to filter the lines starting with a subject key
        exp2 = r"[A-Z]{3}\d{5}.*"
        subjects_info = re.findall(exp2,fixed_prerequisites,re.M)

        subjects_info_cleaned = [re.sub(r" \d "," , ",s).split()[:3] for s in subjects_info]
        
        log.append(subjects_info_cleaned) 

        prerequisites = {x[0]:[] if x[2] == "," else x[2].split(",") for x in subjects_info_cleaned}
        subject_names = {x[0]:x[1] for x in subjects_info_cleaned}
        subject_dict = {"names":subject_names,"prerequisites":prerequisites}

        Save_Dict_to_JSON(subject_dict,path+"/Config/subjects_dict.json")
        print("'subjects_dict.json' sucssesfully built and loaded.")
        return subject_dict 

    dict = Read_JSON_to_Dict(path+"/Config/subjects_dict.json")
    if dict == -1:
        #TODO: improve the safety with a try catch 
        matriz_pdf = os.listdir(path+"/Matriz_Curricular")[-1]
        if matriz_pdf == []:
            #return "Error! Neither 'subjects_dict.json' nor MatrizCurricular were not found."
            return -1
        else:
            print("'subjects_dict.json' not found. Lets build it!")
            return _Build_prerequisites_names_Dict(path+"/Matriz_Curricular/"+matriz_pdf)
    else:
        print("'subjects_dict.json' sucssesfully loaded.")
        return dict 

def Extratos():
    '''Return the filenames of students extract inside the folder "Extratos_Academicos"'''
    # TODO: Should I make a function to deal with full paths? 
    return [path+"/Extratos_Academicos/"+extrato for extrato in os.listdir(path+"/Extratos_Academicos") if extrato[-3:]=="pdf"]

def Aggregate_Demand(extratos,prerequisites):
    '''Reads each students extract to find the completed subjects and their subsequent demands'''
    #TODO improove this commet
    def _Approved_Subjects(student_extract_pdf):
        '''Return approved subject keys from the student's academic extract'''
        #Ideal layout parameters:
        laparams = LAParams(line_overlap=0.5,
            char_margin=95.0, line_margin=2, word_margin=0.5,
            boxes_flow=0.5, detect_vertical=False, all_texts=False)
        #Reading pdf to string
        extract_raw = extract_text(student_extract_pdf,laparams=laparams)
        extract = Correction(extract_raw,dicipline_equivalence)


        #Filter from "extrato" all the lines begining with a subject key
        attended_subjects = re.findall(r"[A-Z]{3}\d{5}.*",extract) #print(attended_subjects)
        #Filter the approved subjects and the subjects exempt through the special pandemic period (AAREs) 
        approved_subjects = [att_sub.split(" ",1)[0] for att_sub in attended_subjects if ("APR" in att_sub or len(att_sub) == 12)]
        return approved_subjects 

    def _Subjects_Demand(prerequisites,approved_subjects):
        '''Finds subjects the student have the possibility to attend.
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
    '''Consolidates the aggregate_demand into a structured result.'''
    final_demand = [["Sigla","Diciplina","Demanda"]]
    print(final_demand[-1])
    for subject,name in subject_dict["names"].items():
        try:
            final_demand.append([subject,name,aggregate_demand[subject]])
            print(final_demand[-1])
        except KeyError:
            log.append(subject)
        
    Save_CSV(final_demand,path+"/Results/RESULTS_aggregate_demand.csv")

def main():
    files = Read_Files_in_Folder()
    subject_dict = Subject_Dict_prerequisites_names(files)
    if subject_dict == -1:
        return "Error! Neither 'subjects_dict.json' nor MatrizCurricular were found in the current folder:\n"+os.getcwd()
    else:
        extratos = Extratos()
        aggregate_demand = Aggregate_Demand(extratos,subject_dict["prerequisites"])
        Final_Demand(aggregate_demand,subject_dict)
main()