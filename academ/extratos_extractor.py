"""
Library to extract data from a student's extract. 
"""
import re
from pyxpdf import Document
from pyxpdf.xpdf import TextOutput, TextControl, page_iterator

def get_student_subjects(report,course_subjects,subjects_equivalences={}):
    taken_subjects = get_taken_subjects(report)
    approved_subjects = list_approved_subjects(taken_subjects,subjects_equivalences)
    demanded_subjects = list_demanded_subjects(approved_subjects,course_subjects)
    return {"taken":taken_subjects,"approved":approved_subjects,"demanded":demanded_subjects}

def student_personal_data(report):
    #todo: break, atomise 
    exp = r":\s*((?:[A-Za-z0-9\/ÃÂÁâáãÊÉéêíÍóÓôÔúÚûÛçÇ,.;()-]+[\s]{0,1}[A-Za-z0-9\/ÃÂÁâáãÊÉéêíÍóÓôÔúÚûÛçÇ,.()-]*[\s]{0,1}(?:;\\n\\n){0,1})*)"
    data = re.findall(exp, report)

    indices_of_interest = [0,1,2,3,4,5,6,7,9] + [-6,-5,-4] + [11,12,13]
    clean_data = [data[i].split('\n')[0].strip() for i in indices_of_interest]
    enem_data = re.findall(r"\d{3},\d{2}",data[8])

    columns = ['name','id','situation', 'center', 'course', 
                'entry_form','quota','year_semester','enrollment_date',
                'credits', 'workload', 'CR']
    student_data = dict(zip(columns,clean_data[:12]))

    enem_subjects = ['essay','lang','math','natural_sci','human_sci','course']
    student_data['enem_grade'] = dict(zip(enem_subjects,enem_data))

    high_school_col = ['name','city','conclusion_year']
    student_data['high_school'] = dict(zip(high_school_col,clean_data[12:]))

    return student_data

def get_taken_subjects(report):
    taken_subjects = build_taken_subjects_dict(fetch_rows_with_subject_info(report))
    return taken_subjects

def build_taken_subjects_dict(subject_rows):
    taken_subjects_dict = {subject[:8] : subject_to_dict(subject) for subject in subject_rows}
    return taken_subjects_dict

def fetch_rows_with_subject_info(report):
    exp = r"[A-Z]{3}\d{5}.*"
    subject_rows = re.findall(exp,report,re.M)
    return subject_rows

def list_approved_subjects(taken_subjects,subjects_equivalences={}):
    approved_subjects = {subject for subject in taken_subjects.keys() if 
        (taken_subjects[subject]["situation"] in ["APR","CVD"])}
    subjects_with_equivalences = set.intersection(set(approved_subjects),set(subjects_equivalences.keys()))
    equivalent_subjects = {subjects_equivalences['subject'] for subject in subjects_with_equivalences}

    return set.union(approved_subjects,equivalent_subjects)

def list_demanded_subjects(approved_subjects,course_subjects):
    demanded_subjects = [subject for subject in course_subjects if 
            (subject not in approved_subjects 
            and set(course_subjects[subject]['prerequisites']).issubset(set(approved_subjects)))]
    return demanded_subjects 

def subject_to_dict(subject_row):
    name = subject_row[8:100].strip()
    data = subject_row[100:].strip().split()
    if len(data) == 2:
        """Subjects taken within Covid special period"""
        subject_dict = {"name":name,"credit":"-","workload":data[1],"grade":data[0],"situation":"CVD"}
    else:
        subject_dict = {"name":name,"credit":data[0],"workload":data[1]+data[2],"grade":data[3],"situation":data[4]}
    return subject_dict 

def PDF_to_string(doc_path): #should I name more specifically? Extrato_text(extrato_path)
    doc = Document(doc_path)
    control = TextControl(mode = "table")
    text_out = TextOutput(doc, control)
    return "\n".join(page_iterator(text_out))

