import sqlite3

def ejecutar_script(sql: str, db_path: str):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.cursor().executescript(sql)
        print("Script SQL ejecutado exitosamente.")
    except sqlite3.Error as e:
        print(f"Error durante la ejecución del script SQL: {e}")
        if conn:
            try:
                conn.rollback()
            except sqlite3.Error:
                pass
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
    
def migrar_estado_y_trabajo_actual(db_path="modelo_relacional.sqlite"):
    sql = """
    PRAGMA foreign_keys = OFF;

    INSERT OR REPLACE INTO Estado_Mental (RespuestaID, Historial, Tratamiento, Historial_Previo, Condicion_Actual, Diagnostico_Oficial)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 6 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 7 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 32 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 33 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 34 THEN a.AnswerText END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (6, 7, 32, 33, 34)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Opinion_Industria (RespuestaID, Percepcion_Apoyo_SM_Industria, Sugerencias_Mejora_SM_Industria, Comentarios_Adicionales_Encuesta)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 85 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 5 THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 86 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 87 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (85, 86, 87)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Beneficios_Trabajo_Actual (RespuestaID, Beneficio, Privacidad_Tratamiento, Conocimiento_Cobertura, Conversacion_Empresarial, Disponibilidad_Recursos, Gestion_Licencia, Acceso_Servicios, Conocimiento_Recursos_Externos, Prioridad_Salud_Fisica, Prioridad_Salud_Mental)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 10 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 11 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 14 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 15 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 16 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 17 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 20 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 21 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 64 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 65 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(a.AnswerText AS INTEGER) END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (10, 11, 14, 15, 16, 17, 20, 21, 64, 65)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Impacto_SM_Trabajo (RespuestaID, Interferencia_Bajo_Tratamiento, Interferencia_Sin_Tratamiento, Productividad_Afectada_SM, Porcentaje_Tiempo_Afectado_SM, Identificacion_Publica_SM, Repercusion_Carrera_SM, Detalle_Impacto_Profesional)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 48 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 49 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 54 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 55 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 78 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 79 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 80 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(a.AnswerText AS INTEGER) END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (48, 49, 54, 55, 78, 79, 80)
    GROUP BY r.RespuestaID;

    PRAGMA foreign_keys = ON;
    """
    ejecutar_script(sql, db_path)
    print("Estado mental y trabajo actual migrados.")
   
def migrar_social_y_trabajo_anterior(db_path="modelo_relacional.sqlite"):
    sql = """
    PRAGMA foreign_keys = OFF;

    INSERT OR REPLACE INTO Impacto_Social_Trabajo_Actual (RespuestaID, Salud_Mental_Entrevista, Confianza_Colegas, Confianza_Liderazgo, Salud_Fisica_Entrevista, Apertura_Circulo_Social, Efecto_Revelar_Observado, Apertura_Clientes, Apertura_Companeros, Comodidad_SF_VS_SM_Companeros, Efecto_Revelar_SM_Cliente, Efecto_Revelar_SM_Companero, Expectativa_Reaccion_Equipo, Disposicion_Entrevista_SM)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 12 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 18 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 19 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 29 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 30 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 31 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 52 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 53 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 57 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 66 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 67 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 81 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 88 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (12, 18, 19, 29, 30, 31, 52, 53, 57, 66, 67, 81, 88)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Experiencia_Trabajo_Actual (RespuestaID, Experiencia_Respuesta_Negativa_SM, Discutido_SM_Empleador, Descripcion_Conversacion_Empleador_SM, Discutido_SM_Companeros, Descripcion_Conversacion_Companeros_SM, Companero_Discutio_SM_Conmigo, Descripcion_Conversacion_Companero_SM, Contexto_Respuesta_Negativa, Percepcion_Apoyo_SM)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 56 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 58 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END), MAX(CASE WHEN a.QuestionID = 59 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 60 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END), MAX(CASE WHEN a.QuestionID = 61 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 62 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END), MAX(CASE WHEN a.QuestionID = 63 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 82 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 83 THEN a.AnswerText END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (56, 58, 59, 60, 61, 62, 63, 82, 83)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Beneficios_Trabajo_Anterior (RespuestaID, Beneficios_Anteriores, Conocimiento_Cobertura_Anterior, Comunicacion_Anterior, Recursos_Anteriores, Privacidad_Anterior, Prioridad_Fisica_Anterior, Prioridad_Mental_Anterior)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 23 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 24 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 25 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 26 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 27 THEN a.AnswerText END),
        MAX(CASE WHEN a.QuestionID = 76 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(a.AnswerText AS INTEGER) END),
        MAX(CASE WHEN a.QuestionID = 77 AND CAST(a.AnswerText AS INTEGER) BETWEEN 0 AND 10 THEN CAST(a.AnswerText AS INTEGER) END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (23, 24, 25, 26, 27, 76, 77)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Experiencias_Trabajo_Anterior (RespuestaID, Discutido_SM_Empleador_Anterior, Descripcion_Conversacion_Liderazgo_Anterior, Discutido_SM_Colegas_Anteriores, Descripcion_Conversacion_Colegas_Anterior, Dialogo_Colega_Anterior_SM, Relato_Conversacion_Colega_Anterior)
    SELECT r.RespuestaID,
        MAX(CASE WHEN a.QuestionID = 70 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END), MAX(CASE WHEN a.QuestionID = 71 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 72 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END), MAX(CASE WHEN a.QuestionID = 73 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 74 AND a.AnswerText IN ('0', '1') THEN CAST(a.AnswerText AS INTEGER) END), MAX(CASE WHEN a.QuestionID = 75 AND a.AnswerText NOT IN ('.') THEN a.AnswerText END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (70, 71, 72, 73, 74, 75)
    GROUP BY r.RespuestaID;

    INSERT OR REPLACE INTO Impacto_Social_Trabajo_Anterior (RespuestaID, Confianza_Liderazgo_Anterior, Comodidad_SF_VS_SM_Anterior)
    SELECT r.RespuestaID, MAX(CASE WHEN a.QuestionID = 28 THEN a.AnswerText END), MAX(CASE WHEN a.QuestionID = 69 THEN a.AnswerText END)
    FROM Respuesta r
    LEFT JOIN Answer a ON a.UserID = r.EncuestadoID AND a.SurveyID = r.EncuestaID AND a.QuestionID IN (28, 69)
    GROUP BY r.RespuestaID;

    PRAGMA foreign_keys = ON;
    """
    ejecutar_script(sql, db_path)
    print("Social y trabajo anterior migrados.")
    
def limpieza(db_path="modelo_relacional.sqlite"):
    sql = """
-- Info General
DELETE FROM Info_Encuestado
WHERE Edad IS NULL
  AND Genero IS NULL
  AND Pais_Vivienda IS NULL
  AND Pais_Empleo IS NULL
  AND Raza_Etnia IS NULL;

DELETE FROM Trabajo_Encuestado
WHERE Freelance IS NULL
  AND Num_Empleados IS NULL
  AND Empresa_Tec IS NULL
  AND Perfil_Tecnologico IS NULL
  AND Experiencia_Laboral_Previa IS NULL
  AND Empresa_Tec_Anterior IS NULL;

DELETE FROM Opinion_Industria
WHERE Percepcion_Apoyo_SM_Industria IS NULL
  AND Sugerencias_Mejora_SM_Industria IS NULL
  AND Comentarios_Adicionales_Encuesta IS NULL;

-- Trabajo Actual
DELETE FROM Experiencia_Trabajo_Actual
WHERE Experiencia_Respuesta_Negativa_SM IS NULL
  AND Discutido_SM_Empleador IS NULL
  AND Descripcion_Conversacion_Empleador_SM IS NULL
  AND Discutido_SM_Companeros IS NULL
  AND Descripcion_Conversacion_Companeros_SM IS NULL
  AND Companero_Discutio_SM_Conmigo IS NULL
  AND Descripcion_Conversacion_Companero_SM IS NULL
  AND Contexto_Respuesta_Negativa IS NULL
  AND Percepcion_Apoyo_SM IS NULL;

-- Trabajo Anterior
DELETE FROM Beneficios_Trabajo_Anterior
WHERE Beneficios_Anteriores IS NULL
  AND Conocimiento_Cobertura_Anterior IS NULL
  AND Comunicacion_Anterior IS NULL
  AND Recursos_Anteriores IS NULL
  AND Privacidad_Anterior IS NULL
  AND Prioridad_Fisica_Anterior IS NULL
  AND Prioridad_Mental_Anterior IS NULL;

DELETE FROM Experiencias_Trabajo_Anterior
WHERE Discutido_SM_Empleador_Anterior IS NULL
  AND Descripcion_Conversacion_Liderazgo_Anterior IS NULL
  AND Discutido_SM_Colegas_Anteriores IS NULL
  AND Descripcion_Conversacion_Colegas_Anterior IS NULL
  AND Dialogo_Colega_Anterior_SM IS NULL
  AND Relato_Conversacion_Colega_Anterior IS NULL;

DELETE FROM Impacto_Social_Trabajo_Anterior
WHERE Confianza_Liderazgo_Anterior IS NULL
  AND Comodidad_SF_VS_SM_Anterior IS NULL;
  
-- Validación Cruzada:

-- Info_Encuestado
UPDATE Info_Encuestado
SET Pais_Empleo = Pais_Vivienda 
WHERE Pais_Empleo  IS NULL;

UPDATE Info_Encuestado
SET Pais_Vivienda = Pais_Empleo 
WHERE Pais_Vivienda  IS NULL;

UPDATE Info_Encuestado
SET Raza_Etnia = 'No Declarado' 
WHERE Raza_Etnia   IS NULL;

UPDATE Info_Encuestado
SET Genero = 'No Declarado' 
WHERE Genero   IS NULL;

UPDATE Info_Encuestado
SET Edad = ROUND((SELECT AVG(b.Edad)
                  FROM Info_Encuestado b
                  WHERE b.Genero = Info_Encuestado.Genero 
                  AND Info_Encuestado.Pais_Vivienda = b.Pais_Vivienda 
                  AND b.Edad IS NOT NULL), 2)
WHERE Edad IS NULL;

-- Trabajo Encuestado

UPDATE Trabajo_Encuestado
SET 
    Empresa_Tec = 0,
    Perfil_Tecnologico = 1
WHERE Freelance = 1 
  AND (Empresa_Tec IS NULL OR Perfil_Tecnologico IS NULL);

--Beneficios
UPDATE Beneficios_Trabajo_Actual
SET Conocimiento_Cobertura = CASE 
    WHEN Beneficio LIKE 'Not eligible%' OR Beneficio = 'No' THEN 'No'
    WHEN Beneficio = 'I don''t know' THEN 'I don''t know'
    WHEN Beneficio = 'Yes' THEN 'Yes'
    ELSE 'No' END
WHERE Conocimiento_Cobertura IS NULL;

UPDATE Beneficios_Trabajo_Actual
SET Conocimiento_Cobertura = CASE 
    WHEN Acceso_Servicios = 0 
      OR Conocimiento_Recursos_Externos LIKE 'No%' THEN 'No'
    WHEN Acceso_Servicios = 1 
      AND Conocimiento_Recursos_Externos LIKE 'Yes%' THEN 'Yes'
    WHEN Acceso_Servicios = 1 
      AND Conocimiento_Recursos_Externos LIKE '%some%' THEN 'I don''t know'
    WHEN Acceso_Servicios = 1 THEN 'Yes'
    ELSE 'No'
END
WHERE Acceso_Servicios IS NOT NULL;

UPDATE Beneficios_Trabajo_Actual
SET 
    Beneficio = 'Not Applicable',
    Privacidad_Tratamiento = 'Not Applicable',
    Conversacion_Empresarial = 'Not Applicable'
WHERE Acceso_Servicios IS NOT NULL 
  AND Beneficio IS NULL;

-- Texto Complejo
UPDATE Experiencia_Trabajo_Actual
SET Descripcion_Conversacion_Companeros_SM = CASE 
    WHEN Discutido_SM_Companeros = 1 THEN 'No description provided'
    ELSE 'Not applicable' END
WHERE Descripcion_Conversacion_Companeros_SM IS NULL;

UPDATE Experiencia_Trabajo_Actual
SET Descripcion_Conversacion_Companero_SM = CASE 
    WHEN Companero_Discutio_SM_Conmigo = 1 THEN 'No description provided'
    ELSE 'Not applicable' END
WHERE Descripcion_Conversacion_Companero_SM IS NULL;

UPDATE Opinion_Industria
SET Sugerencias_Mejora_SM_Industria = 'No description provided'
WHERE Sugerencias_Mejora_SM_Industria IS NULL;
    """
    ejecutar_script(sql, db_path)
    print("base de datos limpiada.")    