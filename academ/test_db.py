#This script builds a test database 
#to help implement this project into UENF's Academic System(yey!!!).
import sqlite3
import files
import logging

def create_table(tables_creation_script: str, con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    with con:
        cur.executescript(tables_creation_script)

def insert_db(insertion_script: str, data: list[tuple], con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    with con:
        cur.executemany(insertion_script, data)

def insert_subject_tuple(subject_tuple: tuple[str,str], con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    insert_subjects_script = """
    INSERT OR IGNORE INTO disciplinas
    (sigla, nome)
    VALUES (?,?);
    """
    insert_db(insert_subjects_script,[subject_tuple],con,cur)

def insert_subject_prerequisites(subject_id: int, subject_prerequisites: list[int], con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
   insert_prerequisites_script = """
   INSERT OR IGNORE INTO prerequisitos 
   (prerequisitante, prerequisito)
   VALUES (?,?);
   """
   data = [(subject_id,subject_prerequisite) for subject_prerequisite in subject_prerequisites]
   insert_db(insert_prerequisites_script,data,con,cur)
   
def insert_subjects(course_subjects: dict[str,dict[str,list[int]]], con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    for sigla, v in course_subjects.items():
        name = v["name"]
        prerequisites = v["prerequisites"]
        subject_tuple = (sigla,name)
        insert_subject_tuple(subject_tuple,con,cur)
        insert_subject_prerequisites(sigla,prerequisites,con,cur)

if __name__ == "__main__":
    CON = sqlite3.connect("test.db")
    CUR = CON.cursor()
    
    course_subjects = files.get_course_subjects()
    
    create_tables_script = """
    CREATE TABLE IF NOT EXISTS disciplinas(
        sigla TEXT PRIMARY KEY,
        nome TEXT
    );

    CREATE TABLE IF NOT EXISTS prerequisitos(
        prerequisitante INTEGER,
        prerequisito INTEGER,
        FOREIGN KEY (prerequisitante) 
            REFERENCES disciplinas(sigla),
        FOREIGN KEY (prerequisito) 
            REFERENCES disciplinas(sigla)
    );

    CREATE TABLE IF NOT EXISTS discipinas_cursadas(
        matricula TEXT PRIMARY KEY,
        sigla TEXT,
        FOREIGN KEY (sigla)
            REFERENCES disciplinas(sigla)
    );
    """
    
    create_table(create_tables_script,CON,CUR)
    insert_subjects(course_subjects,CON,CUR)