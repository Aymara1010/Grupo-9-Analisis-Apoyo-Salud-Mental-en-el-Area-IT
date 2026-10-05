import sqlite3
import pandas as pd
import os

def insertar_datos(db_path="mental_health.sqlite"):

    if not os.path.exists(db_path):
        print(f"No se encontró el archivo.")
        return

    print(f"Conectando a {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Insertando Datos...")
    script = """
-- Catalogos
INSERT OR IGNORE INTO Pais (Pais)
SELECT DISTINCT 
    TRIM(AnswerText) AS Pais
FROM Answer
WHERE QuestionID IN (3, 50)
  AND AnswerText NOT IN ('-1')
ORDER BY Pais;

INSERT OR IGNORE INTO Estados_USA (Estado)
SELECT DISTINCT 
    TRIM(AnswerText) AS Estado
FROM Answer
WHERE QuestionID IN (4, 51)
  AND AnswerText NOT IN ('-1')
ORDER BY Estado;

INSERT OR IGNORE INTO Trabajos (Puesto_Trabajo_Categoria)
SELECT DISTINCT 
    TRIM(AnswerText) AS Puesto_Trabajo_Categoria
FROM Answer
WHERE QuestionID = 117
  AND TRIM(AnswerText) NOT IN ('-1');

INSERT OR IGNORE INTO Condiciones (Condicion)
SELECT DISTINCT 
    TRIM(AnswerText) AS Condicion
FROM Answer
WHERE QuestionID IN (115, 116)
  AND AnswerText NOT IN ('-1')
ORDER BY Condicion;

-- Info encuesta y tabla centro
INSERT OR IGNORE INTO Encuesta (SurveyID, Description)
SELECT 
    SurveyID, 
    Description 
FROM Survey;

INSERT OR IGNORE INTO Respuesta (UsuarioID, SurveyID)
SELECT DISTINCT UserID, SurveyID
FROM Answer
ORDER BY SurveyID, UserID;

-- TABLA PREGUNTA SE HIZO CON UN CSV EXTRAIDO DEL EXCEL

INSERT OR IGNORE INTO Pregunta_Encuesta (QuestionID, SurveyID)
SELECT DISTINCT QuestionID, SurveyID
FROM Answer;
    """

    try:
        cursor.executescript(script)
        conn.commit()
        print("Inserción hecha correctamente.")
    except sqlite3.Error as e:
        print(f"Error {e}")
        conn.rollback()
    finally:
        conn.close()

def insertar_preguntas(db_path="mental_health.sqlite"):

    if not os.path.exists(db_path):
        print(f"No se encontró el archivo.")
        return

    df = pd.read_csv("PREGUNTA.csv", sep=";")
    conn = sqlite3.connect(db_path)
    df.to_sql("Pregunta", conn, if_exists="append", index=False)
    conn.close()
        
if __name__ == "__main__":
    insertar_datos(db_path="mental_health.sqlite")
    insertar_preguntas(db_path="mental_health.sqlite")
    
