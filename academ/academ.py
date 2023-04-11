import files as files
import extratos_extractor as ee
import extratos_aggregate as ea
import presentation as present
import database as db
import logging

def get_students_reports():
    students_reports = [ee.PDF_to_string(f'{filepath}')
        for filepath in files.fetch_reports_filepaths()]
    return students_reports 

def get_subjects_demand(course_subjects, students_subjects):
    students_demanded_subjects = [student_subject['demanded'] for student_subject in students_subjects]

    subject_demand_count = ea.Count_subjects_demand(students_demanded_subjects)

    demand_table = present.subjects_demand_to_table(subject_demand_count,course_subjects)

    return demand_table

def get_all_data():
    course_subjects = files.get_course_subjects()
    students_reports = get_students_reports()
    students_subjects = [ee.get_student_subjects(student_report, course_subjects)
                                  for student_report in students_reports]
    students_infos = [ee.student_personal_data(report) for report in students_reports]

    return (course_subjects, students_subjects, students_infos)

def build_database(course_subjects, students_subjects, students_infos):
    db.build(course_subjects, students_subjects, students_infos)

def get_only_subjects_demand():
    course_subjects = files.get_course_subjects()
    students_demanded_subjects = [ee.get_student_subjects(ee.PDF_to_string(filepath, course_subjects))['demanded']
                                  for filepath in files.fetch_reports_filepaths()]
    subject_demand_count = ea.Count_subjects_demand(students_demanded_subjects)

    demand_table = present.subjects_demand_to_table(subject_demand_count,course_subjects)

    return demand_table

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    logging.info("Lendo os dados... \n")
    course_subjects, students_subjects, students_infos = get_all_data()   
    logging.info("Construindo tabela de demandas... \n")
    demand_table = get_subjects_demand(course_subjects, students_subjects)

    logging.info("Resultados:\n")
    present.present_demand_table(demand_table)
    logging.info(f"Salvando os resultados...")
    files.save_demand_csv(demand_table)

    logging.info("Construindo o banco de dados...")
    build_database(course_subjects, students_subjects, students_infos)
    logging.info("Banco de dados construído com sucesso!")
    logging.info("Script finalizado.")

if __name__ == '__main__':
    main()
