import extratos_extractor

STUDENT_REPORT_EXTRACT = 'MAT01105    Cálculo Diferencial e Integral III                                                              4  068 (068-000-000)  ---       TCNL\n\nMAT01106    Métodos Matemáticos                                                                             4  068 (068-000-000)  ---       TCNL\n\nCarga horária do período: 0 horas                                                                                 C.R. do         período:  0,0\n\nCarga horária acumulada: 867 horas\n\nEmitido em 18/12/2021 10:21  Av. Alberto Lamego, 2000 - Parque Califórnia - Campos dos Goytacazes/RJ - 28013-602                  Página 2/5\n\n                                     Tel.: (22) 27486039 - correio eletrônico: secretariaacademica@uenf.br\n\x0c\n                                          Governo do Estado do Rio de Janeiro\n\n                                          Secretaria de Estado de Ciência e Tecnologia\n\n                             Universidade Estadual do Norte Fluminense Darcy Ribeiro\n\n                                          SECRETARIA ACADÊMICA/REITORIA\n\n(Deliberação CEE/RJ nº 362/2017 - Homologação Portaria CEE/RJ 3576 - DOERJ de 26/04/2017)\n\n                                          EXTRATO    ESCOLAR - GRADUAÇÃO\n\n                                          Documento para simples conferência.\n\nNome:       Daniel Brito dos Santos\n\nMatrícula:  00119110393                                                                                           Situação: Ativo\n\nCentro:     CCT - Centro de Ciência e Tecnologia\n\nCurso:      Bacharelado em Ciência da Computação (Presencial)\n\nParticipações no ENADE\n\nAno      Data do exame       Tipo                              Critério                                           Regular?\n\n                                          Estudante não habilitado em razão do calendário do ciclo avaliativo,\n\n2019        24/11/2019       Ingressante  conforme disposto no Art. 58 § 2º, I, da Portaria Normativa MEC nº      Sim\n\n                                          840/2018.\n\nEmitido em 18/12/2021 10:21  Av. Alberto Lamego, 2000 - Parque Califórnia - Campos dos Goytacazes/RJ - 28013-602  Página 3/5\n\n                                   Tel.: (22) 27486039 - correio eletrônico: secretariaacademica@uenf.br\n\x0c\n                                          Governo do Estado do Rio de Janeiro\n\n                                       Secretaria de Estado de Ciência e Tecnologia\n\n                               Universidade Estadual do Norte Fluminense Darcy Ribeiro\n\n                                       SECRETARIA ACADÊMICA/REITORIA\n\n(Deliberação CEE/RJ nº 362/2017 - Homologação Portaria CEE/RJ 3576 - DOERJ de 26/04/2017)\n\n                                       EXTRATO         ESCOLAR - GRADUAÇÃO\n\n                                                 Documento para simples conferência.\n\nNome:       Daniel Brito dos Santos\n\nMatrícula:  00119110393                                                                                                         Situação: Ativo\n\nCentro:     CCT - Centro de Ciência e Tecnologia\n\nCurso:      Bacharelado em Ciência da Computação (Presencial)\n\nISENÇÃO DE   DISCIPLINAS *                                                            Período                      emergencial  devido  à  COVID-19\n\nSigla        Disciplina                                                                                                         Nota       Carga\n\nFIS01103     Física Geral II                                                                                                    9,0        68\n\nINF01112     Arquitetura de Computadores                                                                                        9,9        68\n\n'
def test_PDF_to_string():
    assert extratos_extractor.PDF_to_string(
        "Extratos_Academicos/extrato_escolar_Daniel_Brito.pdf")[6140:9831] == STUDENT_REPORT_EXTRACT, "Incorrect text extration from pyxpdf or incorrect test document"

def test_List_subjects():
    assert extratos_extractor.List_subjects(STUDENT_REPORT_EXTRACT) == ['MAT01105    Cálculo Diferencial e Integral III                                                              4  068 (068-000-000)  ---       TCNL',
 'MAT01106    Métodos Matemáticos                                                                             4  068 (068-000-000)  ---       TCNL',
 'FIS01103     Física Geral II                                                                                                    9,0        68',
 'INF01112     Arquitetura de Computadores                                                                                        9,9        68'], "Regular expression not listing subjects correctly"

def test_Subjects_to_dict():
  assert extratos_extractor.Subjects_to_dict('PRO01121     Introdução à Probabilidade e Estatística                                                                           9,3        68') ==  {'name': 'Introdução à Probabilidade e Estatística',
  'credit': '-',
  'workload': '68',
  'grade': '9,3',
  'situation': 'CVD'}, "Incorrect format of subject lectured during COVID special period"
  
  assert extratos_extractor.Subjects_to_dict('INF01101      Introdução à Ciência da Computação                                                                2  034 (034-000-000)  9,5       APR') == {'name': 'Introdução à Ciência da Computação',
  'credit': '2',
  'workload': '034(034-000-000)',
  'grade': '9,5',
  'situation': 'APR'}, "Incorrect format of a normal period subject"

def test_Taken_subjects():
    assert extratos_extractor.Taken_subjects(['MAT01105    Cálculo Diferencial e Integral III                                                              4  068 (068-000-000)  ---       TCNL',
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