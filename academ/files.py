"""
Library to find, read and write files
"""
import json
import csv
from os import listdir, getcwd
import logging
from datetime import datetime


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


def Read_course_subjects():
    course_subjects = Read_JSON_to_Dict('config/subjects_dict.json')
    course_subjects_shaped = Shape_old_course_subject(course_subjects)
    return course_subjects_shaped


def Fetch_filenames(dir):
    return listdir(dir)


def Get_current_working_directory():
    return getcwd


def Fetch_reports_filenames():
    reports_names = Fetch_filenames('extratos_academicos')
    return reports_names


def Save_CSV(table, csv_file_name):
    with open(csv_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)
    logging.info("'"+csv_file_name+"'", "sucessfuly written!")


def Today():
    return datetime.today().strftime('%Y-%m-%d')


def Save_demand_csv(demand_table):
    filename = f'results/demanda_disciplinas_{Today()}.csv'
    Save_CSV(demand_table, filename)


if __name__ == '__main__':
    pass
