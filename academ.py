import files
import extratos_extractor as ee
import extratos_aggregate as ea


def Find_subject_demand():
    course_subjects = files.Read_course_subjects()

    students_demanded_subjects = [ee.Student_subjects(ee.PDF_to_string(f'Extratos_Academicos/{filename}'), course_subjects)['demanded']
                         for filename in files.Fetch_reports_filenames()]
    subject_demand_count = ea.Count_subjects_demand(students_demanded_subjects)

    return subject_demand_count


def main():
    print(Find_subject_demand())

if __name__ == '__main__':
    main()
