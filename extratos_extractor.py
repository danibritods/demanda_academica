"""
Library to extract data from a student's extract. 
"""
import re
from pyxpdf import Document
from pyxpdf.xpdf import TextOutput, TextControl, page_iterator

def PDF_to_string(doc_path): #should I name more specifically? Extrato_text(extrato_path)
    doc = Document(doc_path)
    control = TextControl(mode = "table")
    text_out = TextOutput(doc, control)
    return "\n".join(page_iterator(text_out))

def List_subjects(report):
    exp = r"[A-Z]{3}\d{5}.*"
    subjects = re.findall(exp,report,re.M)
    return subjects
    
def Subjects_to_dict(subjects_raw):
    name = subjects_raw[8:100].strip()
    data = subjects_raw[100:].strip().split()
    if len(data) == 2:
        return {"name":name,"credit":"-","workload":data[1],"grade":data[0],"situation":"CVD"}
    else:
        return {"name":name,"credit":data[0],"workload":data[1]+data[2],"grade":data[3],"situation":data[4]}

def Taken_subjects(subjects):
    taken_subjects = {subject[:8]:Subjects_to_dict(subject) for subject in subjects}
    return taken_subjects

def Approved_subjects(taken_subjects):
    return [subject for subject in taken_subjects.keys() if 
        (taken_subjects[subject]["situation"] in ["APR","CVD"])]

def Demanded_subjects(approved_subjects,course_subjects):
    return [subject for subject in course_subjects if 
            (subject not in approved_subjects 
            and set(course_subjects[subject]['prerequisites']).issubset(set(approved_subjects)))]

if __name__ == '__main__':
    # with open("temp",'w') as writer:
    #     writer.writelines(PDF_to_string("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf"))
    print(
            Taken_subjects(
                    (List_subjects(
                            PDF_to_string("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf")))))