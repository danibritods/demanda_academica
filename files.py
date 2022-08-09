"""
Library to find, read and write files
"""
import json

def Read_JSON_to_Dict(json_file):
    try:
        with open(json_file,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return -1  

def Read_course_subjects():
    course_subjects = Read_JSON_to_Dict('Config/subjects_dict.json')
    course_subjects_new_format = {k:{'prerequisites':v} for k,v in course_subjects['prerequisites'].items()}
    return course_subjects_new_format

