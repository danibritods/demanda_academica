"""
Library to find, read and write files
"""
import json, csv
from os import listdir, getcwd
import logging
from datetime import datetime

def Read_JSON_to_Dict(json_file):
    try:
        with open(json_file,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return -1  

def Read_course_subjects():
    course_subjects = Read_JSON_to_Dict('Config/subjects_dict.json')
    course_subjects_new_format = {k:{'prerequisites':v,'name':course_subjects['names'][k]} for k,v in course_subjects['prerequisites'].items()}
    return course_subjects_new_format

def Fetch_filenames(dir):
    return listdir(dir)

def Get_current_working_directory():
    return getcwd

def Fetch_reports_filenames():
    reports_names = Fetch_filenames('Extratos_Academicos')
    return reports_names

def Save_CSV(table,csv_file_name):
    with open(csv_file_name,'w') as csvfile:
        writer = csv.writer(csvfile) 
        for row in table:
            writer.writerow(row)
    logging.info("'"+csv_file_name+"'","sucessfuly written!")

def Today():
    return datetime.today().strftime('%Y-%m-%d')
    
def Save_demand_csv(demand_table):
    filename = f'demanda_disciplinas_{Today()}.csv'
    Save_CSV(demand_table,filename)

if __name__ == '__main__':
    pass

