import extratos_extractor

def test_PDF_to_string():
    assert extratos_extractor.PDF_to_string("Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf")[0] == "G", "pdfminer not working properly"
