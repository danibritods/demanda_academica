import files
import extratos_extractor as ee
import extratos_aggregate as ea
import presentation as present


def Find_subject_demand():
    course_subjects = files.Get_course_subjects()
    students_demanded_subjects = [ee.Student_subjects(ee.PDF_to_string(f'extratos_academicos/{filename}'), course_subjects)['demanded']
                                  for filename in files.Fetch_reports_filenames()]
    subject_demand_count = ea.Count_subjects_demand(students_demanded_subjects)

    demand_table = present.Subjects_demand_to_table(subject_demand_count,course_subjects)

    return demand_table


def main():
    demand_table = Find_subject_demand()
    present.Present_demand_table(demand_table)
    files.Save_demand_csv(demand_table)

if __name__ == '__main__':
    main()
