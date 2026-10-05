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

INSERT OR REPLACE INTO Trabajo_Usuario (RespuestaID, Freelance, Num_Empleados, Empresa_Tec, Perfil_Tecnologico,
Experiencia_Laboral_Previa, Empresa_Tec_Anterior, Trabajo_Remoto_50, Trabajo_Remoto)
SELECT 
    r.RespuestaID,
    CASE WHEN ans5.AnswerText IN ('0', '1') THEN CAST(ans5.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans8.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans8.AnswerText) END,
    CASE WHEN ans9.AnswerText IN ('0', '1') THEN CAST(ans9.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans13.AnswerText IN ('0', '1') THEN CAST(ans13.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans22.AnswerText IN ('0', '1') THEN CAST(ans22.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans68.AnswerText IN ('0', '1') THEN CAST(ans68.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans93.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans93.AnswerText) END,
    CASE WHEN ans118.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans118.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans5   ON ans5.UserID = r.UsuarioID   AND ans5.SurveyID = r.SurveyID   AND ans5.QuestionID = 5
LEFT JOIN Answer ans8   ON ans8.UserID = r.UsuarioID   AND ans8.SurveyID = r.SurveyID   AND ans8.QuestionID = 8
LEFT JOIN Answer ans9   ON ans9.UserID = r.UsuarioID   AND ans9.SurveyID = r.SurveyID   AND ans9.QuestionID = 9
LEFT JOIN Answer ans13  ON ans13.UserID = r.UsuarioID  AND ans13.SurveyID = r.SurveyID  AND ans13.QuestionID = 13
LEFT JOIN Answer ans22  ON ans22.UserID = r.UsuarioID  AND ans22.SurveyID = r.SurveyID  AND ans22.QuestionID = 22
LEFT JOIN Answer ans68  ON ans68.UserID = r.UsuarioID  AND ans68.SurveyID = r.SurveyID  AND ans68.QuestionID = 68
LEFT JOIN Answer ans93  ON ans93.UserID = r.UsuarioID  AND ans93.SurveyID = r.SurveyID  AND ans93.QuestionID = 93
LEFT JOIN Answer ans118 ON ans118.UserID = r.UsuarioID AND ans118.SurveyID = r.SurveyID AND ans118.QuestionID = 118;

INSERT OR REPLACE INTO Impacto_SM_Trabajo (
    RespuestaID, Interferencia_Bajo_Tratamiento, Interferencia_Sin_Tratamiento,
    Productividad_Afectada_SM, Porcentaje_Tiempo_Afectado_SM, Identificacion_Publica_SM,
    Repercusion_Carrera_SM, Detalle_Impacto_Profesional, Interferencia_SM_Trabajo_General,
    Perjuicio_Carrera_SM
)
SELECT 
    r.RespuestaID,
    CASE WHEN ans48.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans48.AnswerText) END,
    CASE WHEN ans49.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans49.AnswerText) END,
    CASE WHEN ans54.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans54.AnswerText) END,
    CASE WHEN ans55.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans55.AnswerText) END,
    CASE WHEN ans78.AnswerText IN ('0', '1') THEN CAST(ans78.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans79.AnswerText IN ('0', '1') THEN CAST(ans79.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN CAST(ans80.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(ans80.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans92.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans92.AnswerText) END,
    CASE WHEN ans113.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans113.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans48  ON ans48.UserID = r.UsuarioID  AND ans48.SurveyID = r.SurveyID  AND ans48.QuestionID = 48
LEFT JOIN Answer ans49  ON ans49.UserID = r.UsuarioID  AND ans49.SurveyID = r.SurveyID  AND ans49.QuestionID = 49
LEFT JOIN Answer ans54  ON ans54.UserID = r.UsuarioID  AND ans54.SurveyID = r.SurveyID  AND ans54.QuestionID = 54
LEFT JOIN Answer ans55  ON ans55.UserID = r.UsuarioID  AND ans55.SurveyID = r.SurveyID  AND ans55.QuestionID = 55
LEFT JOIN Answer ans78  ON ans78.UserID = r.UsuarioID  AND ans78.SurveyID = r.SurveyID  AND ans78.QuestionID = 78
LEFT JOIN Answer ans79  ON ans79.UserID = r.UsuarioID  AND ans79.SurveyID = r.SurveyID  AND ans79.QuestionID = 79
LEFT JOIN Answer ans80  ON ans80.UserID = r.UsuarioID  AND ans80.SurveyID = r.SurveyID  AND ans80.QuestionID = 80
LEFT JOIN Answer ans92  ON ans92.UserID = r.UsuarioID  AND ans92.SurveyID = r.SurveyID  AND ans92.QuestionID = 92
LEFT JOIN Answer ans113 ON ans113.UserID = r.UsuarioID AND ans113.SurveyID = r.SurveyID AND ans113.QuestionID = 113;

INSERT OR REPLACE INTO Impacto_Social_Trabajo_Anterior (
    RespuestaID, Confianza_Liderazgo_Anterior, Comodidad_SF_VS_SM_Anterior,
    Consecuencias_SM_Empleador_Anterior, Consecuencias_SF_Empleador_Anterior,
    Disposicion_SM_Companeros_Anteriores, Consecuencias_SM_Companeros_Anteriores
)
SELECT 
    r.RespuestaID,
    CASE WHEN ans28.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans28.AnswerText) END,
    CASE WHEN ans69.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans69.AnswerText) END,
    CASE WHEN ans108.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans108.AnswerText) END,
    CASE WHEN ans109.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans109.AnswerText) END,
    CASE WHEN ans110.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans110.AnswerText) END,
    CASE WHEN ans112.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans112.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans28  ON ans28.UserID = r.UsuarioID  AND ans28.SurveyID = r.SurveyID  AND ans28.QuestionID = 28
LEFT JOIN Answer ans69  ON ans69.UserID = r.UsuarioID  AND ans69.SurveyID = r.SurveyID  AND ans69.QuestionID = 69
LEFT JOIN Answer ans108 ON ans108.UserID = r.UsuarioID AND ans108.SurveyID = r.SurveyID AND ans108.QuestionID = 108
LEFT JOIN Answer ans109 ON ans109.UserID = r.UsuarioID AND ans109.SurveyID = r.SurveyID AND ans109.QuestionID = 109
LEFT JOIN Answer ans110 ON ans110.UserID = r.UsuarioID AND ans110.SurveyID = r.SurveyID AND ans110.QuestionID = 110
LEFT JOIN Answer ans112 ON ans112.UserID = r.UsuarioID AND ans112.SurveyID = r.SurveyID AND ans112.QuestionID = 112
WHERE (ans28.AnswerText IS NOT NULL AND ans28.AnswerText NOT IN ('-1'))
   OR (ans69.AnswerText IS NOT NULL AND ans69.AnswerText NOT IN ('-1'))
   OR (ans108.AnswerText IS NOT NULL AND ans108.AnswerText NOT IN ('-1'))
   OR (ans109.AnswerText IS NOT NULL AND ans109.AnswerText NOT IN ('-1'))
   OR (ans110.AnswerText IS NOT NULL AND ans110.AnswerText NOT IN ('-1'))
   OR (ans112.AnswerText IS NOT NULL AND ans112.AnswerText NOT IN ('-1'));
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