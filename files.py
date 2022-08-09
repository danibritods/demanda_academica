"""
Library to find, read and write files
"""
import json
from os import listdir, getcwd

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
