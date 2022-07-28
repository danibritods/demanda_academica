"""
Library to extract data from a student's extract. 
"""
from pyxpdf import Document
from pyxpdf.xpdf import TextOutput, TextControl, page_iterator

def PDF_to_string(doc_path):
    doc = Document(doc_path)
    control = TextControl(mode = "table")
    text_out = TextOutput(doc, control)
    return "\n".join(page_iterator(text_out))

if __name__ == '__main__':
    # with open("temp",'w') as writer:
    #     writer.writelines(PDF_to_string("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf"))
    print(PDFx("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf"))