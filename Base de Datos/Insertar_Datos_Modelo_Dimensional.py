import sqlite3

def ejecutar_script(sql, db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.cursor().executescript(sql)
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def migrar_catalogos_y_centro(db_path="modelo_relacional.sqlite"):
    sql = """
    PRAGMA foreign_keys = OFF;

    INSERT OR REPLACE INTO Pais (Pais)
    SELECT DISTINCT AnswerText FROM Answer
    WHERE QuestionID IN (3, 50) AND AnswerText IS NOT NULL ORDER BY AnswerText;

    INSERT OR REPLACE INTO Estados_USA (Estado)
    SELECT DISTINCT AnswerText FROM Answer
    WHERE QuestionID IN (4, 51) AND AnswerText IS NOT NULL ORDER BY AnswerText;

    INSERT OR REPLACE INTO Encuesta (EncuestaID, Descripcion)
    SELECT SurveyID, Description FROM Survey;

    INSERT OR REPLACE INTO Respuesta (EncuestadoID, EncuestaID)
    SELECT DISTINCT UserID, SurveyID FROM Answer ORDER BY SurveyID, UserID;

    INSERT OR REPLACE INTO Pregunta_Encuesta (PreguntaID, EncuestaID)
    SELECT DISTINCT QuestionID, SurveyID FROM Answer;

    PRAGMA foreign_keys = ON;
    """
    ejecutar_script(sql, db_path)
    print("Catalogos y nucleo migrados.")