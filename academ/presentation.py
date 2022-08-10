'''Module to format info into presentation'''


def Subjects_demand_to_table(subjects_demand, course_subjects):
    header = [('Sigla', 'Nome', 'Demanda (aluno)')]
    demand_table = [(subject_id, course_subjects[subject_id]['name'], subject_demand)
                    for subject_id, subject_demand in subjects_demand]

    return header + demand_table

def Present_demand_table(demand_table):
    for row in demand_table:
        print(*row)