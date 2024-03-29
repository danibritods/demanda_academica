import academ.extratos_extractor as ee

STUDENT_REPORT_EXTRACT = 'MAT01105    Cálculo Diferencial e Integral III                                                              4  068 (068-000-000)  ---       TCNL\n\nMAT01106    Métodos Matemáticos                                                                             4  068 (068-000-000)  ---       TCNL\n\nCarga horária do período: 0 horas                                                                                 C.R. do         período:  0,0\n\nCarga horária acumulada: 867 horas\n\nEmitido em 18/12/2021 10:21  Av. Alberto Lamego, 2000 - Parque Califórnia - Campos dos Goytacazes/RJ - 28013-602                  Página 2/5\n\n                                     Tel.: (22) 27486039 - correio eletrônico: secretariaacademica@uenf.br\n\x0c\n                                          Governo do Estado do Rio de Janeiro\n\n                                          Secretaria de Estado de Ciência e Tecnologia\n\n                             Universidade Estadual do Norte Fluminense Darcy Ribeiro\n\n                                          SECRETARIA ACADÊMICA/REITORIA\n\n(Deliberação CEE/RJ nº 362/2017 - Homologação Portaria CEE/RJ 3576 - DOERJ de 26/04/2017)\n\n                                          EXTRATO    ESCOLAR - GRADUAÇÃO\n\n                                          Documento para simples conferência.\n\nNome:       Daniel Brito dos Santos\n\nMatrícula:  00119110393                                                                                           Situação: Ativo\n\nCentro:     CCT - Centro de Ciência e Tecnologia\n\nCurso:      Bacharelado em Ciência da Computação (Presencial)\n\nParticipações no ENADE\n\nAno      Data do exame       Tipo                              Critério                                           Regular?\n\n                                          Estudante não habilitado em razão do calendário do ciclo avaliativo,\n\n2019        24/11/2019       Ingressante  conforme disposto no Art. 58 § 2º, I, da Portaria Normativa MEC nº      Sim\n\n                                          840/2018.\n\nEmitido em 18/12/2021 10:21  Av. Alberto Lamego, 2000 - Parque Califórnia - Campos dos Goytacazes/RJ - 28013-602  Página 3/5\n\n                                   Tel.: (22) 27486039 - correio eletrônico: secretariaacademica@uenf.br\n\x0c\n                                          Governo do Estado do Rio de Janeiro\n\n                                       Secretaria de Estado de Ciência e Tecnologia\n\n                               Universidade Estadual do Norte Fluminense Darcy Ribeiro\n\n                                       SECRETARIA ACADÊMICA/REITORIA\n\n(Deliberação CEE/RJ nº 362/2017 - Homologação Portaria CEE/RJ 3576 - DOERJ de 26/04/2017)\n\n                                       EXTRATO         ESCOLAR - GRADUAÇÃO\n\n                                                 Documento para simples conferência.\n\nNome:       Daniel Brito dos Santos\n\nMatrícula:  00119110393                                                                                                         Situação: Ativo\n\nCentro:     CCT - Centro de Ciência e Tecnologia\n\nCurso:      Bacharelado em Ciência da Computação (Presencial)\n\nISENÇÃO DE   DISCIPLINAS *                                                            Período                      emergencial  devido  à  COVID-19\n\nSigla        Disciplina                                                                                                         Nota       Carga\n\nFIS01103     Física Geral II                                                                                                    9,0        68\n\nINF01112     Arquitetura de Computadores                                                                                        9,9        68\n\n'
def test_PDF_to_string():
    assert ee.PDF_to_string(
        "extratos_academicos/extrato_escolar_Daniel_Brito.pdf")[6140:9831] == STUDENT_REPORT_EXTRACT, "Incorrect text extration from pyxpdf or incorrect test document"

def test_Find_subjects_rows():
    assert ee.fetch_rows_with_subject_info(STUDENT_REPORT_EXTRACT) == ['MAT01105    Cálculo Diferencial e Integral III                                                              4  068 (068-000-000)  ---       TCNL',
 'MAT01106    Métodos Matemáticos                                                                             4  068 (068-000-000)  ---       TCNL',
 'FIS01103     Física Geral II                                                                                                    9,0        68',
 'INF01112     Arquitetura de Computadores                                                                                        9,9        68'], "Regular expression not listing subjects correctly"

def test_Subject_to_dict():
  assert ee.subject_to_dict('PRO01121     Introdução à Probabilidade e Estatística                                                                           9,3        68') ==  {'name': 'Introdução à Probabilidade e Estatística',
  'credit': '-',
  'workload': '68',
  'grade': '9,3',
  'situation': 'CVD'}, "Incorrect format of subject lectured during COVID special period"
  
  assert ee.subject_to_dict('INF01101      Introdução à Ciência da Computação                                                                2  034 (034-000-000)  9,5       APR') == {'name': 'Introdução à Ciência da Computação',
  'credit': '2',
  'workload': '034(034-000-000)',
  'grade': '9,5',
  'situation': 'APR'}, "Incorrect format of a normal period subject"

def test_Dict_taken_subjects():
    assert ee.build_taken_subjects_dict(['MAT01105    Cálculo Diferencial e Integral III                                                              4  068 (068-000-000)  ---       TCNL',
 'MAT01106    Métodos Matemáticos                                                                             4  068 (068-000-000)  ---       TCNL',
 'FIS01103     Física Geral II                                                                                                    9,0        68',
 'INF01112     Arquitetura de Computadores                                                                                        9,9        68']) == {'MAT01105': {'name': 'Cálculo Diferencial e Integral III',
  'credit': '4',
  'workload': '068(068-000-000)',
  'grade': '---',
  'situation': 'TCNL'},
 'MAT01106': {'name': 'Métodos Matemáticos',
  'credit': '4',
  'workload': '068(068-000-000)',
  'grade': '---',
  'situation': 'TCNL'},
 'FIS01103': {'name': 'Física Geral II',
  'credit': '-',
  'workload': '68',
  'grade': '9,0',
  'situation': 'CVD'},
 'INF01112': {'name': 'Arquitetura de Computadores',
  'credit': '-',
  'workload': '68',
  'grade': '9,9',
  'situation': 'CVD'}}, "Fault in the integration of the previous functions"

def test_List_approved_subjects():
    assert ee.list_approved_subjects(
      {'INF01112': {'name': 'Arquitetura de Computadores',
        'credit': '-',
        'workload': '68',
        'grade': '9,9',
        'situation': 'CVD'}, 
      'INF01101': {'name': 'Introdução à Ciência da Computação',
        'credit': '2',
        'workload': '034(034-000-000)',
        'grade': '9,5',
        'situation': 'APR'}}
    ) == {"INF01112","INF01101"}, "Approved subjects"

def test_List_demanded_disciplines():
    course_subjects = {"INF01201":{"name":"Análise e Projeto De Sistemas","prerequisites":["INF01101","INF01209"]},
                      "INF01204":{ "name":"Sistema Operacional"          ,"prerequisites":["INF01112"]},
                      "LEL04102":{ "name":"Inglês Instrumental I"        ,"prerequisites":[]},
                      "INF01207":{ "name":"Estruturas Discretas"         ,"prerequisites":["MAT01104"]}}
    approved_subjects = ["INF01112","INF01101"]
    expected_demand = ["INF01204","LEL04102"]
    #Here I could separate in cases (asserts), for incomplete prerequisites, no prerequisites, none prerequisite
    assert ee.list_demanded_subjects(approved_subjects,course_subjects) == expected_demand
  
def test_Student_info():
  #assert regex returns the right info (if the regex is compatible with doculement)
  #assert if the order of data is 'correct' (the expected order)
  pass


