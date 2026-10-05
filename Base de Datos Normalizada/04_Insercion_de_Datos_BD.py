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


INSERT OR REPLACE INTO Beneficios_Trabajo_Anterior (
    RespuestaID, Beneficios_Anteriores, Conocimiento_Cobertura_Anterior,
    Comunicacion_Anterior, Recursos_Anteriores, Privacidad_Anterior,
    Prioridad_Fisica_Anterior, Prioridad_Mental_Anterior, Empresa_Anterior_Seriedad_SM_VS_SF
)
SELECT 
    r.RespuestaID,
    CASE WHEN ans23.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans23.AnswerText) END,
    CASE WHEN ans24.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans24.AnswerText) END,
    CASE WHEN ans25.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans25.AnswerText) END,
    CASE WHEN ans26.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans26.AnswerText) END,
    CASE WHEN ans27.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans27.AnswerText) END,
    CASE WHEN CAST(ans76.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(ans76.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN CAST(ans77.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(ans77.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans111.AnswerText IN ('-1') THEN NULL ELSE TRIM(ans111.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans23  ON ans23.UserID = r.UsuarioID  AND ans23.SurveyID = r.SurveyID  AND ans23.QuestionID = 23
LEFT JOIN Answer ans24  ON ans24.UserID = r.UsuarioID  AND ans24.SurveyID = r.SurveyID  AND ans24.QuestionID = 24
LEFT JOIN Answer ans25  ON ans25.UserID = r.UsuarioID  AND ans25.SurveyID = r.SurveyID  AND ans25.QuestionID = 25
LEFT JOIN Answer ans26  ON ans26.UserID = r.UsuarioID  AND ans26.SurveyID = r.SurveyID  AND ans26.QuestionID = 26
LEFT JOIN Answer ans27  ON ans27.UserID = r.UsuarioID  AND ans27.SurveyID = r.SurveyID  AND ans27.QuestionID = 27
LEFT JOIN Answer ans76  ON ans76.UserID = r.UsuarioID  AND ans76.SurveyID = r.SurveyID  AND ans76.QuestionID = 76
LEFT JOIN Answer ans77  ON ans77.UserID = r.UsuarioID  AND ans77.SurveyID = r.SurveyID  AND ans77.QuestionID = 77
LEFT JOIN Answer ans111 ON ans111.UserID = r.UsuarioID AND ans111.SurveyID = r.SurveyID AND ans111.QuestionID = 111
WHERE (ans23.AnswerText IS NOT NULL AND ans23.AnswerText NOT IN ('-1'))
   OR (ans24.AnswerText IS NOT NULL AND ans24.AnswerText NOT IN ('-1'))
   OR (ans25.AnswerText IS NOT NULL AND ans25.AnswerText NOT IN ('-1'))
   OR (ans26.AnswerText IS NOT NULL AND ans26.AnswerText NOT IN ('-1'))
   OR (ans27.AnswerText IS NOT NULL AND ans27.AnswerText NOT IN ('-1'))
   OR (ans76.AnswerText IS NOT NULL AND ans76.AnswerText NOT IN ('-1'))
   OR (ans77.AnswerText IS NOT NULL AND ans77.AnswerText NOT IN ('-1'))
   OR (ans111.AnswerText IS NOT NULL AND ans111.AnswerText NOT IN ('-1'));

INSERT OR REPLACE INTO Beneficios_Trabajo_Actual (
    RespuestaID, Beneficio, Privacidad_Tratamiento, Conocimiento_Cobertura,
    Conversacion_Empresarial, Disponibilidad_Recursos, Gestion_Licencia,
    Acceso_Servicios, Conocimiento_Recursos_Externos, Prioridad_Salud_Fisica,
    Prioridad_Salud_Mental, Empresa_Seriedad_SM_VS_SF, Conocimiento_Opciones_SM_Empleador,
    Empresa_Programa_Bienestar_SM, Empresa_Recursos_Ayuda_SM, Facilidad_Licencia_Medica_SM
)
SELECT 
    r.RespuestaID,
    CASE WHEN ans10.AnswerText = '-1' THEN NULL ELSE TRIM(ans10.AnswerText) END,
    CASE WHEN ans11.AnswerText = '-1' THEN NULL ELSE TRIM(ans11.AnswerText) END,
    CASE WHEN ans14.AnswerText = '-1' THEN NULL ELSE TRIM(ans14.AnswerText) END,
    CASE WHEN ans15.AnswerText = '-1' THEN NULL ELSE TRIM(ans15.AnswerText) END,
    CASE WHEN ans16.AnswerText = '-1' THEN NULL ELSE TRIM(ans16.AnswerText) END,
    CASE WHEN ans17.AnswerText = '-1' THEN NULL ELSE TRIM(ans17.AnswerText) END,
    CASE WHEN ans20.AnswerText IN ('0', '1') THEN CAST(ans20.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans21.AnswerText = '-1' THEN NULL ELSE TRIM(ans21.AnswerText) END,
    CASE WHEN CAST(ans64.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(ans64.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN CAST(ans65.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(ans65.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans91.AnswerText = '-1' THEN NULL ELSE TRIM(ans91.AnswerText) END,
    CASE WHEN ans94.AnswerText = '-1' THEN NULL ELSE TRIM(ans94.AnswerText) END,
    CASE WHEN ans95.AnswerText = '-1' THEN NULL ELSE TRIM(ans95.AnswerText) END,
    CASE WHEN ans96.AnswerText = '-1' THEN NULL ELSE TRIM(ans96.AnswerText) END,
    CASE WHEN ans97.AnswerText = '-1' THEN NULL ELSE TRIM(ans97.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans10 ON ans10.UserID = r.UsuarioID AND ans10.SurveyID = r.SurveyID AND ans10.QuestionID = 10
LEFT JOIN Answer ans11 ON ans11.UserID = r.UsuarioID AND ans11.SurveyID = r.SurveyID AND ans11.QuestionID = 11
LEFT JOIN Answer ans14 ON ans14.UserID = r.UsuarioID AND ans14.SurveyID = r.SurveyID AND ans14.QuestionID = 14
LEFT JOIN Answer ans15 ON ans15.UserID = r.UsuarioID AND ans15.SurveyID = r.SurveyID AND ans15.QuestionID = 15
LEFT JOIN Answer ans16 ON ans16.UserID = r.UsuarioID AND ans16.SurveyID = r.SurveyID AND ans16.QuestionID = 16
LEFT JOIN Answer ans17 ON ans17.UserID = r.UsuarioID AND ans17.SurveyID = r.SurveyID AND ans17.QuestionID = 17
LEFT JOIN Answer ans20 ON ans20.UserID = r.UsuarioID AND ans20.SurveyID = r.SurveyID AND ans20.QuestionID = 20
LEFT JOIN Answer ans21 ON ans21.UserID = r.UsuarioID AND ans21.SurveyID = r.SurveyID AND ans21.QuestionID = 21
LEFT JOIN Answer ans64 ON ans64.UserID = r.UsuarioID AND ans64.SurveyID = r.SurveyID AND ans64.QuestionID = 64
LEFT JOIN Answer ans65 ON ans65.UserID = r.UsuarioID AND ans65.SurveyID = r.SurveyID AND ans65.QuestionID = 65
LEFT JOIN Answer ans91 ON ans91.UserID = r.UsuarioID AND ans91.SurveyID = r.SurveyID AND ans91.QuestionID = 91
LEFT JOIN Answer ans94 ON ans94.UserID = r.UsuarioID AND ans94.SurveyID = r.SurveyID AND ans94.QuestionID = 94
LEFT JOIN Answer ans95 ON ans95.UserID = r.UsuarioID AND ans95.SurveyID = r.SurveyID AND ans95.QuestionID = 95
LEFT JOIN Answer ans96 ON ans96.UserID = r.UsuarioID AND ans96.SurveyID = r.SurveyID AND ans96.QuestionID = 96
LEFT JOIN Answer ans97 ON ans97.UserID = r.UsuarioID AND ans97.SurveyID = r.SurveyID AND ans97.QuestionID = 97;

INSERT OR REPLACE INTO Experiencia_Trabajo_Actual (
    RespuestaID, Experiencia_Respuesta_Negativa_SM, Discutido_SM_Empleador,
    Descripcion_Conversacion_Empleador_SM, Discutido_SM_Companeros,
    Descripcion_Conversacion_Companeros_SM, Companero_Discutio_SM_Conmigo,
    Descripcion_Conversacion_Companero_SM, Contexto_Respuesta_Negativa, Percepcion_Apoyo_SM
)
SELECT 
    r.RespuestaID,
    CASE WHEN ans56.AnswerText = '-1' THEN NULL ELSE TRIM(ans56.AnswerText) END,
    CASE WHEN ans58.AnswerText IN ('0', '1') THEN CAST(ans58.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans59.AnswerText IN ('-1', '.') THEN NULL ELSE TRIM(ans59.AnswerText) END,
    CASE WHEN ans60.AnswerText IN ('0', '1') THEN CAST(ans60.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans61.AnswerText IN ('-1', '.') THEN NULL ELSE TRIM(ans61.AnswerText) END,
    CASE WHEN ans62.AnswerText IN ('0', '1') THEN CAST(ans62.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans63.AnswerText IN ('-1', '.') THEN NULL ELSE TRIM(ans63.AnswerText) END,
    CASE WHEN ans82.AnswerText IN ('-1', '.') THEN NULL ELSE TRIM(ans82.AnswerText) END,
    CASE WHEN ans83.AnswerText = '-1' THEN NULL ELSE TRIM(ans83.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans56 ON ans56.UserID = r.UsuarioID AND ans56.SurveyID = r.SurveyID AND ans56.QuestionID = 56
LEFT JOIN Answer ans58 ON ans58.UserID = r.UsuarioID AND ans58.SurveyID = r.SurveyID AND ans58.QuestionID = 58
LEFT JOIN Answer ans59 ON ans59.UserID = r.UsuarioID AND ans59.SurveyID = r.SurveyID AND ans59.QuestionID = 59
LEFT JOIN Answer ans60 ON ans60.UserID = r.UsuarioID AND ans60.SurveyID = r.SurveyID AND ans60.QuestionID = 60
LEFT JOIN Answer ans61 ON ans61.UserID = r.UsuarioID AND ans61.SurveyID = r.SurveyID AND ans61.QuestionID = 61
LEFT JOIN Answer ans62 ON ans62.UserID = r.UsuarioID AND ans62.SurveyID = r.SurveyID AND ans62.QuestionID = 62
LEFT JOIN Answer ans63 ON ans63.UserID = r.UsuarioID AND ans63.SurveyID = r.SurveyID AND ans63.QuestionID = 63
LEFT JOIN Answer ans82 ON ans82.UserID = r.UsuarioID AND ans82.SurveyID = r.SurveyID AND ans82.QuestionID = 82
LEFT JOIN Answer ans83 ON ans83.UserID = r.UsuarioID AND ans83.SurveyID = r.SurveyID AND ans83.QuestionID = 83
WHERE (ans56.AnswerText IS NOT NULL AND ans56.AnswerText NOT IN ('-1'))
   OR (ans58.AnswerText IS NOT NULL AND ans58.AnswerText IN ('0', '1'))
   OR (ans59.AnswerText IS NOT NULL AND ans59.AnswerText NOT IN ('-1'))
   OR (ans60.AnswerText IS NOT NULL AND ans60.AnswerText IN ('0', '1'))
   OR (ans61.AnswerText IS NOT NULL AND ans61.AnswerText NOT IN ('-1'))
   OR (ans62.AnswerText IS NOT NULL AND ans62.AnswerText IN ('0', '1'))
   OR (ans63.AnswerText IS NOT NULL AND ans63.AnswerText NOT IN ('-1'))
   OR (ans82.AnswerText IS NOT NULL AND ans82.AnswerText NOT IN ('-1'))
   OR (ans83.AnswerText IS NOT NULL AND ans83.AnswerText NOT IN ('-1'));

INSERT OR REPLACE INTO Impacto_Social_Trabajo_Actual (
    RespuestaID, Salud_Mental_Entrevista, Confianza_Colegas, Confianza_Liderazgo,
    Salud_Fisica_Entrevista, Apertura_Circulo_Social, Efecto_Revelar_Observado,
    Apertura_Clientes, Apertura_Companeros, Comodidad_SF_VS_SM_Companeros,
    Efecto_Revelar_SM_Cliente, Efecto_Revelar_SM_Companero, Expectativa_Reaccion_Equipo,
    Disposicion_Entrevista_SM, Consecuencias_Discutir_SF, Consecuencias_Discutir_SM,
    Disposicion_SM_Companeros, Disposicion_SM_Supervisor, Mencionar_SF_Entrevista,
    Consecuencias_SM_Companeros, Consecuencias_SM_Empleador_Actual,
    Consecuencias_SM_Companeros_Actual, Impacto_Negativo_SM_Cliente,
    Impacto_Negativo_SM_Companero, Percepcion_Negativa_Equipo_SM
)
SELECT 
    r.RespuestaID,
    CASE WHEN ans12.AnswerText = '-1' THEN NULL ELSE TRIM(ans12.AnswerText) END,
    CASE WHEN ans18.AnswerText = '-1' THEN NULL ELSE TRIM(ans18.AnswerText) END,
    CASE WHEN ans19.AnswerText = '-1' THEN NULL ELSE TRIM(ans19.AnswerText) END,
    CASE WHEN ans29.AnswerText = '-1' THEN NULL ELSE TRIM(ans29.AnswerText) END,
    CASE WHEN ans30.AnswerText = '-1' THEN NULL ELSE TRIM(ans30.AnswerText) END,
    CASE WHEN ans31.AnswerText = '-1' THEN NULL ELSE TRIM(ans31.AnswerText) END,
    CASE WHEN ans52.AnswerText = '-1' THEN NULL ELSE TRIM(ans52.AnswerText) END,
    CASE WHEN ans53.AnswerText = '-1' THEN NULL ELSE TRIM(ans53.AnswerText) END,
    CASE WHEN ans57.AnswerText = '-1' THEN NULL ELSE TRIM(ans57.AnswerText) END,
    CASE WHEN ans66.AnswerText = '-1' THEN NULL ELSE TRIM(ans66.AnswerText) END,
    CASE WHEN ans67.AnswerText = '-1' THEN NULL ELSE TRIM(ans67.AnswerText) END,
    CASE WHEN CAST(ans81.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(ans81.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans88.AnswerText IN ('0', '1') THEN CAST(ans88.AnswerText AS INTEGER) ELSE NULL END,
    CASE WHEN ans90.AnswerText = '-1' THEN NULL ELSE TRIM(ans90.AnswerText) END,
    CASE WHEN ans98.AnswerText = '-1' THEN NULL ELSE TRIM(ans98.AnswerText) END,
    CASE WHEN ans99.AnswerText = '-1' THEN NULL ELSE TRIM(ans99.AnswerText) END,
    CASE WHEN ans100.AnswerText = '-1' THEN NULL ELSE TRIM(ans100.AnswerText) END,
    CASE WHEN ans101.AnswerText = '-1' THEN NULL ELSE TRIM(ans101.AnswerText) END,
    CASE WHEN ans102.AnswerText = '-1' THEN NULL ELSE TRIM(ans102.AnswerText) END,
    CASE WHEN ans104.AnswerText = '-1' THEN NULL ELSE TRIM(ans104.AnswerText) END,
    CASE WHEN ans105.AnswerText = '-1' THEN NULL ELSE TRIM(ans105.AnswerText) END,
    CASE WHEN ans106.AnswerText = '-1' THEN NULL ELSE TRIM(ans106.AnswerText) END,
    CASE WHEN ans107.AnswerText = '-1' THEN NULL ELSE TRIM(ans107.AnswerText) END,
    CASE WHEN ans114.AnswerText = '-1' THEN NULL ELSE TRIM(ans114.AnswerText) END
FROM Respuesta r
LEFT JOIN Answer ans12  ON ans12.UserID = r.UsuarioID  AND ans12.SurveyID = r.SurveyID  AND ans12.QuestionID = 12
LEFT JOIN Answer ans18  ON ans18.UserID = r.UsuarioID  AND ans18.SurveyID = r.SurveyID  AND ans18.QuestionID = 18
LEFT JOIN Answer ans19  ON ans19.UserID = r.UsuarioID  AND ans19.SurveyID = r.SurveyID  AND ans19.QuestionID = 19
LEFT JOIN Answer ans29  ON ans29.UserID = r.UsuarioID  AND ans29.SurveyID = r.SurveyID  AND ans29.QuestionID = 29
LEFT JOIN Answer ans30  ON ans30.UserID = r.UsuarioID  AND ans30.SurveyID = r.SurveyID  AND ans30.QuestionID = 30
LEFT JOIN Answer ans31  ON ans31.UserID = r.UsuarioID  AND ans31.SurveyID = r.SurveyID  AND ans31.QuestionID = 31
LEFT JOIN Answer ans52  ON ans52.UserID = r.UsuarioID  AND ans52.SurveyID = r.SurveyID  AND ans52.QuestionID = 52
LEFT JOIN Answer ans53  ON ans53.UserID = r.UsuarioID  AND ans53.SurveyID = r.SurveyID  AND ans53.QuestionID = 53
LEFT JOIN Answer ans57  ON ans57.UserID = r.UsuarioID  AND ans57.SurveyID = r.SurveyID  AND ans57.QuestionID = 57
LEFT JOIN Answer ans66  ON ans66.UserID = r.UsuarioID  AND ans66.SurveyID = r.SurveyID  AND ans66.QuestionID = 66
LEFT JOIN Answer ans67  ON ans67.UserID = r.UsuarioID  AND ans67.SurveyID = r.SurveyID  AND ans67.QuestionID = 67
LEFT JOIN Answer ans81  ON ans81.UserID = r.UsuarioID  AND ans81.SurveyID = r.SurveyID  AND ans81.QuestionID = 81
LEFT JOIN Answer ans88  ON ans88.UserID = r.UsuarioID  AND ans88.SurveyID = r.SurveyID  AND ans88.QuestionID = 88
LEFT JOIN Answer ans90  ON ans90.UserID = r.UsuarioID  AND ans90.SurveyID = r.SurveyID  AND ans90.QuestionID = 90
LEFT JOIN Answer ans98  ON ans98.UserID = r.UsuarioID  AND ans98.SurveyID = r.SurveyID  AND ans98.QuestionID = 98
LEFT JOIN Answer ans99  ON ans99.UserID = r.UsuarioID  AND ans99.SurveyID = r.SurveyID  AND ans99.QuestionID = 99
LEFT JOIN Answer ans100 ON ans100.UserID = r.UsuarioID AND ans100.SurveyID = r.SurveyID AND ans100.QuestionID = 100
LEFT JOIN Answer ans101 ON ans101.UserID = r.UsuarioID AND ans101.SurveyID = r.SurveyID AND ans101.QuestionID = 101
LEFT JOIN Answer ans102 ON ans102.UserID = r.UsuarioID AND ans102.SurveyID = r.SurveyID AND ans102.QuestionID = 102
LEFT JOIN Answer ans104 ON ans104.UserID = r.UsuarioID AND ans104.SurveyID = r.SurveyID AND ans104.QuestionID = 104
LEFT JOIN Answer ans105 ON ans105.UserID = r.UsuarioID AND ans105.SurveyID = r.SurveyID AND ans105.QuestionID = 105
LEFT JOIN Answer ans106 ON ans106.UserID = r.UsuarioID AND ans106.SurveyID = r.SurveyID AND ans106.QuestionID = 106
LEFT JOIN Answer ans107 ON ans107.UserID = r.UsuarioID AND ans107.SurveyID = r.SurveyID AND ans107.QuestionID = 107
LEFT JOIN Answer ans114 ON ans114.UserID = r.UsuarioID AND ans114.SurveyID = r.SurveyID AND ans114.QuestionID = 114;
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

