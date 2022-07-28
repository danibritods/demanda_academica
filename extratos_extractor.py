"""
Library to extract data from a student's extract. 
"""
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def PDF_to_string(student_extract_pdf_path):
    #Ideal layout parameters:
    laparams = LAParams(line_overlap=0.5,
        char_margin=95.0, line_margin=2, word_margin=0.5,
        boxes_flow=0.5, detect_vertical=False, all_texts=False)
    return extract_text(student_extract_pdf_path,laparams=laparams)   

if __name__ == '__main__':
    # with open("temp",'w') as writer:
    #     writer.writelines(PDF_to_string("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf"))
    print(PDF_to_string("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf")[0])