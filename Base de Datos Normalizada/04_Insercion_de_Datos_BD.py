import sqlite3
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

INSERT OR REPLACE INTO Usuarios_Trabaja_USA (RespuestaID, Estado_USA_Empleo)
SELECT r.RespuestaID,
       e.EstadoID AS Estado_USA_Empleo
FROM Answer a
JOIN Respuesta r ON r.UsuarioID = a.UserID AND r.SurveyID = a.SurveyID
JOIN Estados_USA e ON e.Estado = TRIM(a.AnswerText)
WHERE a.QuestionID = 51
  AND TRIM(a.AnswerText) NOT IN ('-1');

INSERT OR REPLACE INTO Usuarios_Vive_USA (RespuestaID, Estado_USA_Vivienda)
SELECT r.RespuestaID,
       e.EstadoID AS Estado_USA_Vivienda
FROM Answer a
JOIN Respuesta r ON r.UsuarioID = a.UserID AND r.SurveyID = a.SurveyID
JOIN Estados_USA e ON e.Estado = TRIM(a.AnswerText)
WHERE a.QuestionID = 4
  AND TRIM(a.AnswerText) NOT IN ('-1');

INSERT OR REPLACE INTO Trabajo_Respuesta (RespuestaID, PuestoID)
SELECT DISTINCT r.RespuestaID,t.PuestoID
FROM Answer a
JOIN Respuesta r ON r.UsuarioID = a.UserID AND r.SurveyID = a.SurveyID
JOIN Trabajos t ON t.Puesto_Trabajo_Categoria = TRIM(a.AnswerText)
WHERE a.QuestionID = 117 AND a.AnswerText IS NOT NULL AND TRIM(a.AnswerText) NOT IN ('-1');

INSERT OR IGNORE INTO Condicion_Diagnosticada (RespuestaID, CondicionID)
SELECT DISTINCT r.RespuestaID, c.CondicionID
FROM Answer a
JOIN Respuesta r ON r.UsuarioID = a.UserID AND r.SurveyID = a.SurveyID
JOIN Condiciones c ON c.Condicion = TRIM(a.AnswerText)
WHERE a.QuestionID = 116 
  AND TRIM(a.AnswerText) NOT IN ('-1');

INSERT OR IGNORE INTO Condicion_Sospechada (RespuestaID, CondicionID)
SELECT DISTINCT r.RespuestaID, c.CondicionID
FROM Answer a
JOIN Respuesta r ON r.UsuarioID = a.UserID AND r.SurveyID = a.SurveyID
JOIN Condiciones c  ON c.Condicion = TRIM(a.AnswerText)
WHERE a.QuestionID = 116 AND TRIM(a.AnswerText) NOT IN ('-1');

INSERT OR REPLACE INTO Info_Usuario (RespuestaID, Edad, Genero, Pais_Vivienda, Pais_Empleo, Raza_Etnia)
SELECT r.RespuestaID,
    CASE WHEN CAST(ans1.AnswerText AS INTEGER) BETWEEN 18 AND 85 THEN CAST(ans1.AnswerText AS INTEGER) ELSE NULL END AS Edad,
    CASE WHEN ans2.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans2.AnswerText) END AS Genero,
    CASE WHEN pv.PaisID IN ('-1') THEN NULL ELSE TRIM(pv.PaisID) END AS Pais_Vivienda,
    CASE WHEN pe.PaisID IN ('-1') THEN NULL ELSE TRIM(pe.PaisID) END AS Pais_Empleo,
    CASE WHEN ans89.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans89.AnswerText) END AS Raza_Etnia
FROM Respuesta r
LEFT JOIN Answer ans1 ON ans1.UserID = r.UsuarioID AND ans1.SurveyID = r.SurveyID AND ans1.QuestionID = 1
LEFT JOIN Answer ans2 ON ans2.UserID = r.UsuarioID AND ans2.SurveyID = r.SurveyID AND ans2.QuestionID = 2
LEFT JOIN Answer ans3 ON ans3.UserID = r.UsuarioID AND ans3.SurveyID = r.SurveyID AND ans3.QuestionID = 3
LEFT JOIN Answer ans50 ON ans50.UserID = r.UsuarioID AND ans50.SurveyID = r.SurveyID AND ans50.QuestionID = 50
LEFT JOIN Answer ans89 ON ans89.UserID = r.UsuarioID AND ans89.SurveyID = r.SurveyID AND ans89.QuestionID = 89
LEFT JOIN Pais pv ON pv.Pais = TRIM(ans3.AnswerText)
LEFT JOIN Pais pe ON pe.Pais = TRIM(ans50.AnswerText);

INSERT OR REPLACE INTO Estado_Mental (RespuestaID, Historial, Tratamiento, Historial_Previo,
Condicion_Actual, Diagnostico_Oficial)
SELECT 
r.RespuestaID, CASE WHEN ans6.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans6.AnswerText) END AS Historial,
CASE WHEN ans7.AnswerText IN ('0', '1') THEN CAST(ans7.AnswerText AS INTEGER) ELSE NULL END AS Tratamiento,
CASE WHEN ans32.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans32.AnswerText) END AS Historial_Previo,
CASE WHEN ans33.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans33.AnswerText) END AS Condicion_Actual,
CASE WHEN ans34.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans34.AnswerText) END AS Diagnostico_Oficial 
FROM Respuesta r 
LEFT JOIN Answer ans6 ON ans6.UserID = r.UsuarioID AND ans6.SurveyID = r.SurveyID AND ans6.QuestionID = 6 
LEFT JOIN Answer ans7 ON ans7.UserID = r.UsuarioID AND ans7.SurveyID = r.SurveyID AND ans7.QuestionID = 7 
LEFT JOIN Answer ans32 ON ans32.UserID = r.UsuarioID AND ans32.SurveyID = r.SurveyID AND ans32.QuestionID = 32 
LEFT JOIN Answer ans33 ON ans33.UserID = r.UsuarioID AND ans33.SurveyID = r.SurveyID AND ans33.QuestionID = 33 
LEFT JOIN Answer ans34 ON ans34.UserID = r.UsuarioID AND ans34.SurveyID = r.SurveyID AND ans34.QuestionID = 34;
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

if __name__ == "__main__":
    insertar_datos(db_path="mental_health.sqlite")