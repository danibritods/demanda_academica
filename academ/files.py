"""
Library to find, read and write files
"""
import json
import csv
import os
import logging
from datetime import datetime
from configparser import ConfigParser
CONFIG = ConfigParser()
CONFIG.read("config.ini")
PATHS = CONFIG["paths"]

def get_course_subjects():
    disciplinas_do_curso_csv_path = CONFIG.get("paths","DisciplinasCursoCSV")
    return format_read_course_subjects(
        read_csv(disciplinas_do_curso_csv_path))

def fetch_reports_filepaths():
    reports_folder_path = PATHS.get("PastaExtratosAcademicos")
    reports_filenames = os.listdir(reports_folder_path)
    reports_filepaths = [os.path.join(reports_folder_path,filename) for filename in reports_filenames]
    return reports_filepaths

def save_demand_csv(demand_table):
    results_path = PATHS.get("ResultsFolder")
    filename = f'{results_path}/demanda_disciplinas_{today()}.csv'
    save_CSV(demand_table, filename)


def format_read_course_subjects(course_subject_tuple):
    return {subject_id: {'name': name, 'prerequisites': _treat_prerequisite_read(prerequisites)}
            for subject_id, name, prerequisites in course_subject_tuple[1:]}

def read_csv(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        return tuple(csv_reader)

def _treat_prerequisite_read(prerequisite_str):
    return [] if prerequisite_str == '' else prerequisite_str.replace(' ', '').split(',')

def today():
    return datetime.today().strftime('%Y-%m-%d')


def Read_JSON_to_Dict(json_file):
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return -1


def Shape_old_course_subject(course_subjects):
    shaped = {subject: {'name': name, 'prerequisites': prerequisites}
              for (subject, name), prerequisites
              in zip(course_subjects['names'].items(), course_subjects['prerequisites'].values())}
    return shaped


def Read_old_course_subjects():
    course_subjects = Read_JSON_to_Dict('config/subjects_dict.json')
    course_subjects_shaped = Shape_old_course_subject(course_subjects)
    return course_subjects_shaped

def Get_current_working_directory():
    return os.getcwd

def save_CSV(table, csv_filename):
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    with open(csv_filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)
            
    logging.info("Arquivo "+"'"+csv_filename+"'" + " salvo com sucesso!")

def Write_csv_dict(filename,table,fieldnames):
    with open(filename, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames, delimiter=';', quotechar=' ')
        writer.writeheader()
        writer.writerows(table) 

def _treat_prerequisite_write(prerequisite_list):
    return str(prerequisite_list)[1:-1].replace("'","")


def Format_course_subjects_to_save(course_subjects):
    course_subjects_dictable = [{'Sigla':sub_id,'Nome':sub['name'],'Prerequisitos':_treat_prerequisite_write(sub['prerequisites'])} 
                                for sub_id,sub in course_subjects.items()]
    return course_subjects_dictable


def Save_course_subjects(course_subjects):
    course_subjects_dictable = Format_course_subjects_to_save(course_subjects)
    fieldnames = ('Sigla','Nome','Prerequisitos')
    Write_csv_dict('config/disciplinas_do_curso.csv',course_subjects_dictable,fieldnames)

def Get_subjects_equivalences():
    filename = 'config/disciplinas_equivalentes.csv'
    subjects_equivalences = read_csv(filename)
    # subjects_equivalences = 
    return subjects_equivalences



if __name__ == '__main__':
    pass
