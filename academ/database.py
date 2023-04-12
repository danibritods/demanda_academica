import sqlite3
import os
from files import PATHS

def build(course_subjects, students_subjects, students_infos):
  database_filename = "academ.db"
  database_filepath = os.path.join(PATHS.get("ResultsFolder"),database_filename)
  con = sqlite3.connect(database_filepath)
  cur = con.cursor()

  tables_creation_script = """
  CREATE TABLE IF NOT EXISTS Disciplinas (
    Sigla         varchar(10) NOT NULL, 
    Nome          varchar(10) NOT NULL, 
    Creditos      integer(10), 
    CargaHoraria  integer(10),  
    PRIMARY KEY (Sigla)
    );

  CREATE TABLE IF NOT EXISTS Pre_requisitos (
    Pre_requisitante INTEGER,
    Pre_requisito    INTEGER,
    FOREIGN KEY (Pre_requisitante) 
        REFERENCES disciplinas(Sigla),
    FOREIGN KEY (Pre_requisito) 
        REFERENCES disciplinas(Sigla)
  );

  CREATE TABLE IF NOT EXISTS DisciplinasCursadas (
    EstudanteMatricula integer(10) NOT NULL, 
    DisciplinasSigla   varchar(10) NOT NULL, 
    Nota               varchar(4) NOT NULL, 
    Situacao           varchar(3) NOT NULL, 
    PRIMARY KEY (
      EstudanteMatricula, 
      DisciplinasSigla), 
    FOREIGN KEY(EstudanteMatricula) 
      REFERENCES Estudante(Matricula), 
    FOREIGN KEY(DisciplinasSigla) 
      REFERENCES Disciplinas(Sigla));

  CREATE TABLE IF NOT EXISTS EnsinoMedio (
    EstudanteMatricula integer(10) NOT NULL, 
    Instituicao        varchar(255), 
    Cidade             varchar(255), 
    AnoConclusao       char(4), 
    FOREIGN KEY(EstudanteMatricula) 
      REFERENCES Estudante(Matricula));

  CREATE TABLE IF NOT EXISTS Estudante (
    Matricula     integer(10) NOT NULL, 
    Nome          varchar(255) NOT NULL, 
    Situacao      varchar(255) NOT NULL, 
    Centro        varchar(255) NOT NULL, 
    Curso         varchar(255) NOT NULL, 
    DataMatricula char(10) NOT NULL, 
    CreditosAcum  integer(10) NOT NULL, 
    CargaHoraria  varchar(255) NOT NULL, 
    CRE           varchar(5) NOT NULL, 
    PRIMARY KEY (Matricula));

  CREATE TABLE IF NOT EXISTS Ingresso (
    EstudanteMatricula integer(10) NOT NULL, 
    FormaIngresso      varchar(255) NOT NULL, 
    Cota               varchar(255) NOT NULL, 
    AnoSemestre        char(6) NOT NULL, 
    FOREIGN KEY(EstudanteMatricula) 
      REFERENCES Estudante(Matricula));

  CREATE TABLE IF NOT EXISTS NotasEnem (
    EstudanteMatricula integer(10) NOT NULL, 
    Redacao            char(7) NOT NULL, 
    Linguagens         char(7) NOT NULL, 
    Matematica         char(7) NOT NULL, 
    CienNat            char(7) NOT NULL, 
    CienHum            char(7) NOT NULL, 
    Curso              char(7) NOT NULL, 
    FOREIGN KEY(EstudanteMatricula) 
      REFERENCES Estudante(Matricula));
  """

  insertion_script = {"DisciplinasCursadas":"""
                      INSERT OR IGNORE INTO DisciplinasCursadas
                      (EstudanteMatricula, 
                      DisciplinasSigla, 
                      Nota, 
                      Situacao) 
                      VALUES 
                      (?, ?, ?, ?);
                      """,
                "Estudante":"""
                    INSERT OR IGNORE INTO Estudante
                      (Matricula, 
                      Nome, 
                      Situacao, 
                      Centro, 
                      Curso, 
                      DataMatricula, 
                      CreditosAcum, 
                      CargaHoraria, 
                      CRE)
                    VALUES 
                      (?, ?, ?, ?, ?, ?, ?, ?, ?);
                      """,
                "EnsinoMedio":"""
                    INSERT OR IGNORE INTO EnsinoMedio
                      (EstudanteMatricula,
                      Instituicao, 
                      Cidade, 
                      AnoConclusao) 
                    VALUES 
                      (?, ?, ?, ?);
                    """,
                "Ingresso":"""
                    INSERT OR IGNORE INTO Ingresso
                      (EstudanteMatricula,
                      FormaIngresso, 
                      Cota, 
                      AnoSemestre) 
                    VALUES 
                      (?, ?, ?, ?);
                    """,
                "NotasEnem":"""
                    INSERT OR IGNORE INTO NotasEnem
                      (EstudanteMatricula, 
                      Redacao, 
                      Linguagens, 
                      Matematica, 
                      CienNat, 
                      CienHum, 
                      Curso) 
                    VALUES 
                      (?, ?, ?, ?, ?, ?, ?);
                    """             
                      }

  create_tables(con, cur, tables_creation_script)
  insert_student_data(con, cur, students_subjects, students_infos, insertion_script)
  insert_subjects_data(con,cur, course_subjects)
  
def create_tables(con, cur, tables_creation_script):
  cur.executescript(tables_creation_script)
  con.commit()

def insert_student_data(con, cur, students_subjects, students_infos, insertion_script):
  [student_data_to_db(con, cur, student_subject['taken'], student_info, insertion_script) 
  for student_subject, student_info in zip(students_subjects, students_infos)]    

def student_data_to_db(con, cur, taken_subjects, student_info, insertion_script):
    insert_db(con, cur, insertion_script["DisciplinasCursadas"],
        format_disciplinas_cursadas(student_info['id'],
            taken_subjects_dict_to_rows(taken_subjects)))
    
    insert_db(con, cur, insertion_script["Estudante"],
      format_estudante(student_info))

    insert_db(con, cur, insertion_script["Ingresso"],
      format_ingresso(student_info))

    insert_db(con, cur, insertion_script["EnsinoMedio"],
      format_ingresso(student_info))

    insert_db(con, cur, insertion_script["NotasEnem"],
      format_notas_enem(student_info))

def insert_subjects_data(con, cur, course_subjects):
  for sigla, v in course_subjects.items():
    name = v["name"]
    prerequisites = v["prerequisites"]
    subject_tuple = (sigla,name)
    insert_subject_tuple(con,cur, subject_tuple)
    insert_subject_prerequisites(con,cur, sigla,prerequisites,)

def insert_subject_tuple(con: sqlite3.Connection, cur: sqlite3.Cursor, subject_tuple: tuple[str,str]) -> None:
    insert_subjects_script = """
    INSERT OR IGNORE INTO Disciplinas
    (Sigla, Nome)
    VALUES (?,?);
    """
    insert_db(con,cur, insert_subjects_script, [subject_tuple])

def insert_subject_prerequisites(con: sqlite3.Connection, cur: sqlite3.Cursor, subject_id: int, subject_prerequisites: list[int]) -> None:
   insert_prerequisites_script = """
   INSERT OR IGNORE INTO Pre_requisitos 
   (Pre_requisitante, Pre_requisito)
   VALUES (?,?);
   """
   data = [(subject_id,subject_prerequisite) for subject_prerequisite in subject_prerequisites]
   insert_db(con,cur, insert_prerequisites_script, data)

def insert_db(con, cur,  insertion_script, data):
  cur.executemany(insertion_script,data)
  con.commit()
  
def format_disciplinas_cursadas(student_id, taken_subjects_rows):
    """(student_id, subject_id, grade, situation)"""
    data = [(student_id, sb[0], sb[-2], sb[-1]) for sb in taken_subjects_rows ]
    #get_prerequisites(sb[0], course_subjects)
    return data

def taken_subjects_dict_to_rows(taken_subjects):
    """(id,{name,... }) -> [(id,name,credit,workload,grade,situation),]"""
    return [(id, *data.values()) for id, data in taken_subjects.items()]
    
def format_estudante(student_info):
  s = student_info
  return [(s['id'], s['name'], s['situation'], s['center'], s['course'], 
          s['enrollment_date'], s['credits'], s['workload'], s['CR']),]

def format_notas_enem(student_info):  
  """
  EstudanteMatricula, 
  Redacao, 
  Linguagens, 
  Matematica, 
  CienNat, 
  CienHum, 
  Curso
  """
  g = student_info['enem_grade']
  return ((student_info['id'], g['essay'], g['lang'], g['math'], g['natural_sci'], g['human_sci'], g['course']),)

def format_ingresso(student_info):
  """
  EstudanteMatricula,
  FormaIngresso, 
  Cota, 
  AnoSemestre 
  """
  s = student_info
  return ((s['id'], s['entry_form'], s['quota'], s['year_semester']),)
  
def format_ensino_medio(student_info):
  """
  EstudanteMatricula,
  Instituicao, 
  Cidade, 
  AnoConclusao
  """
  d = student_info['high_school']
  return ((student_info['id'], d['name'], d['city'], d['conclusion_year']),)




