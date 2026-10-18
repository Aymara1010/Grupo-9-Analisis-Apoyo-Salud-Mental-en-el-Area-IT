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
    
def migrar_demografia_y_trabajo(db_path="modelo_relacional.sqlite"):
    sql = """
    PRAGMA foreign_keys = OFF;

    INSERT OR REPLACE INTO Info_Encuestado (RespuestaID, Edad, Genero, Pais_Vivienda, Pais_Empleo, Raza_Etnia)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 1 AND CAST(a.AnswerText AS INTEGER) BETWEEN 18 AND 85 THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 2 THEN a.AnswerText END),
        pv.PaisID, pe.PaisID,
        MAX(CASE WHEN a.QuestionID = 89 THEN a.AnswerText END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (1, 2, 3, 50, 89)
    LEFT JOIN Pais pv ON pv.Pais = (SELECT AnswerText FROM Answer WHERE UserID = r.EncuestadoID AND SurveyID = r.EncuestaID AND QuestionID = 3)
    LEFT JOIN Pais pe ON pe.Pais = (SELECT AnswerText FROM Answer WHERE UserID = r.EncuestadoID AND SurveyID = r.EncuestaID AND QuestionID = 50)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Encuestados_Vive_USA (RespuestaID, Estado_USA_Vivienda)
    SELECT r.RespuestaID, e.EstadoID FROM Respuesta r
    JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID = 4
    JOIN Estados_USA e ON e.Estado = a.AnswerText;

    INSERT OR REPLACE INTO Encuestados_Trabaja_USA (RespuestaID, Estado_USA_Empleo)
    SELECT r.RespuestaID, e.EstadoID FROM Respuesta r
    JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID = 51
    JOIN Estados_USA e ON e.Estado = a.AnswerText;

    INSERT OR REPLACE INTO Trabajo_Encuestado (RespuestaID, Freelance, Num_Empleados, Empresa_Tec, Perfil_Tecnologico, Experiencia_Laboral_Previa, Empresa_Tec_Anterior)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 5 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 8 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 9 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 13 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 22 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 68 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (5, 8, 9, 13, 22, 68)
    GROUP BY r.RespuestaID;

    PRAGMA foreign_keys = ON;
    """
    ejecutar_script(sql, db_path)
    print("Demografia y trabajo cargados.")