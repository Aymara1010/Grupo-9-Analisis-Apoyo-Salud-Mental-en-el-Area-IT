import sqlite3
import os

def clonar_datos_filtrados(ruta_origen, ruta_destino):
    if not os.path.exists(ruta_origen):
        print(f"No se encontró el archivo.")
        return

    conn = sqlite3.connect(ruta_destino)
    cursor = conn.cursor()

    try:
        cursor.execute("ATTACH DATABASE ? AS origen;", (ruta_origen,))

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS Survey AS 
            SELECT * FROM origen.Survey 
            WHERE SurveyID IN (2017, 2018, 2019);

            CREATE TABLE IF NOT EXISTS Answer AS 
            SELECT * FROM origen.Answer 
            WHERE SurveyID IN (2017, 2018, 2019);
        """)

        cursor.execute("DETACH DATABASE origen;")
        conn.commit()
        return conn

    except sqlite3.Error as e:
        print(f"Error de SQLite en extraccion: {e}")
        conn.rollback()
        conn.close()
        return None

def limpiar_respuestas(conn, ruta_destino):
    cursor = conn.cursor()
    try:
        cursor.executescript(
            """
            UPDATE Answer
            SET AnswerText = CASE 
                WHEN TRIM(AnswerText) = '-1' THEN NULL 
                ELSE TRIM(AnswerText) END;

            UPDATE Answer
            SET AnswerText = CASE 
                WHEN AnswerText = 'United States of America' THEN 'United States' 
                ELSE AnswerText END
            WHERE QuestionID IN (3, 50);

            UPDATE Answer
            SET AnswerText = CASE 
                WHEN AnswerText IN (
                    'Male', 'male', 'MALE', 'Male-ish', 'something kinda male?',
                    'Guy (-ish) ^_^', 'male leaning androgynous', 
                    'ostensibly male, unsure what that really means',
                    'Ostensibly Male', 'Cishet male', 'Masculine', 
                    'masculino', 'SWM', 'Demiguy', 'I have a penis'
                ) THEN 'Masculino'
                WHEN AnswerText IN (
                    'Female', 'female', 'Woman-identified', 'Female-identified',
                    'Female assigned at birth', 'fm', 'femmina', 'Female-ish'
                ) THEN 'Femenino'
                ELSE 'Otro' END
            WHERE QuestionID = 2;
            
            UPDATE Answer
            SET AnswerText = 'I don''t know'
            WHERE QuestionID IN (11, 10, 91)
            AND (TRIM(AnswerText) IN ('Don''t know', 'I don''t know'));  
        """)

        conn.commit()
        print(f"Proceso completado exitosamente en '{ruta_destino}'.")

    except sqlite3.Error as e:
        print(f"Error de SQLite en limpieza: {e}")
        conn.rollback()
    finally:
        conn.close()

def normalizar_base_de_datos(db_path):
    if not os.path.exists(db_path):
        print(f"No se encontró el archivo en: {db_path}")
        return

    print(f"Conectando a {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Creando tablas normalizadas...")
    script = """
-- Tablas Catalogo

CREATE TABLE IF NOT EXISTS Pais (
    PaisID INTEGER PRIMARY KEY AUTOINCREMENT,
    Pais VARCHAR NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Estados_USA (
    EstadoID INTEGER PRIMARY KEY AUTOINCREMENT,
    Estado VARCHAR NOT NULL UNIQUE
);

-- Encuesta y Preguntas

CREATE TABLE IF NOT EXISTS Encuesta (
    EncuestaID INTEGER PRIMARY KEY,
    Descripcion VARCHAR NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Pregunta (
    PreguntaID INTEGER PRIMARY KEY,
    Pregunta VARCHAR NOT NULL,
    Tabla_Destino VARCHAR,
    Columna_Destino VARCHAR
);

CREATE TABLE IF NOT EXISTS Pregunta_Encuesta (
    PreguntaID INTEGER NOT NULL,
    EncuestaID INTEGER NOT NULL,
    PRIMARY KEY (PreguntaID, EncuestaID),
    FOREIGN KEY (PreguntaID) REFERENCES Pregunta(PreguntaID) ON DELETE CASCADE,
    FOREIGN KEY (EncuestaID) REFERENCES Encuesta(EncuestaID) ON DELETE CASCADE
);

-- Respuestas (Núcleo de la bd)
CREATE TABLE IF NOT EXISTS Respuesta (
    RespuestaID INTEGER PRIMARY KEY AUTOINCREMENT,
    EncuestadoID INTEGER NOT NULL,
    EncuestaID INTEGER NOT NULL,
    FOREIGN KEY (EncuestaID) REFERENCES Encuesta(EncuestaID) ON DELETE CASCADE,
    UNIQUE(EncuestadoID, EncuestaID)
);

-- Información General del Encuestado
CREATE TABLE IF NOT EXISTS Info_Encuestado (
    RespuestaID INTEGER PRIMARY KEY,
    Edad INTEGER,
    Genero VARCHAR,
    Pais_Vivienda INTEGER,
    Pais_Empleo INTEGER,
    Raza_Etnia VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (Pais_Vivienda) REFERENCES Pais(PaisID),
    FOREIGN KEY (Pais_Empleo) REFERENCES Pais(PaisID)
);

CREATE TABLE IF NOT EXISTS Encuestados_Vive_USA (
    RespuestaID INTEGER PRIMARY KEY,
    Estado_USA_Vivienda INTEGER,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (Estado_USA_Vivienda) REFERENCES Estados_USA(EstadoID)
);

CREATE TABLE IF NOT EXISTS Encuestados_Trabaja_USA (
    RespuestaID INTEGER PRIMARY KEY,
    Estado_USA_Empleo INTEGER,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (Estado_USA_Empleo) REFERENCES Estados_USA(EstadoID));

CREATE TABLE IF NOT EXISTS Trabajo_Encuestado (
    RespuestaID INTEGER PRIMARY KEY,
    Freelance INTEGER CHECK (Freelance IN (0, 1, NULL)),
    Num_Empleados VARCHAR,
    Empresa_Tec INTEGER CHECK (Empresa_Tec IN (0, 1, NULL)),
    Perfil_Tecnologico INTEGER CHECK (Perfil_Tecnologico IN (0, 1, NULL)),
    Experiencia_Laboral_Previa INTEGER CHECK (Experiencia_Laboral_Previa IN (0, 1, NULL)),
    Empresa_Tec_Anterior INTEGER CHECK (Empresa_Tec_Anterior IN (0, 1, NULL)),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Estado_Mental (
    RespuestaID INTEGER PRIMARY KEY,
    Historial VARCHAR,
    Tratamiento INTEGER CHECK (Tratamiento IN (0, 1, NULL)),
    Historial_Previo VARCHAR,
    Condicion_Actual VARCHAR,
    Diagnostico_Oficial VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Opinion_Industria (
    RespuestaID INTEGER PRIMARY KEY,
    Percepcion_Apoyo_SM_Industria INTEGER CHECK (Percepcion_Apoyo_SM_Industria BETWEEN 0 AND 5 OR Percepcion_Apoyo_SM_Industria IS NULL),
    Sugerencias_Mejora_SM_Industria VARCHAR,
    Comentarios_Adicionales_Encuesta VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

-- Trabajo Actual
CREATE TABLE IF NOT EXISTS Beneficios_Trabajo_Actual (
    RespuestaID INTEGER PRIMARY KEY,
    Beneficio VARCHAR,
    Privacidad_Tratamiento VARCHAR,
    Conocimiento_Cobertura VARCHAR,
    Conversacion_Empresarial VARCHAR,
    Disponibilidad_Recursos VARCHAR,
    Gestion_Licencia VARCHAR,
    Acceso_Servicios INTEGER CHECK (Acceso_Servicios IN (0, 1, NULL)),
    Conocimiento_Recursos_Externos VARCHAR,
    Prioridad_Salud_Fisica INTEGER CHECK (Prioridad_Salud_Fisica BETWEEN 0 AND 10 OR Prioridad_Salud_Fisica IS NULL),
    Prioridad_Salud_Mental INTEGER CHECK (Prioridad_Salud_Mental BETWEEN 0 AND 10 OR Prioridad_Salud_Mental IS NULL),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Impacto_SM_Trabajo (
    RespuestaID INTEGER PRIMARY KEY,
    Interferencia_Bajo_Tratamiento VARCHAR,
    Interferencia_Sin_Tratamiento VARCHAR,
    Productividad_Afectada_SM VARCHAR,
    Porcentaje_Tiempo_Afectado_SM VARCHAR,
    Identificacion_Publica_SM INTEGER CHECK (Identificacion_Publica_SM IN (0, 1, NULL)),
    Repercusion_Carrera_SM INTEGER CHECK (Repercusion_Carrera_SM IN (0, 1, NULL)),
    Detalle_Impacto_Profesional INTEGER CHECK (Detalle_Impacto_Profesional BETWEEN 0 AND 10 OR Detalle_Impacto_Profesional IS NULL),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Impacto_Social_Trabajo_Actual (
    RespuestaID INTEGER PRIMARY KEY,
    Salud_Mental_Entrevista VARCHAR,
    Confianza_Colegas VARCHAR,
    Confianza_Liderazgo VARCHAR,
    Salud_Fisica_Entrevista VARCHAR,
    Apertura_Circulo_Social VARCHAR,
    Efecto_Revelar_Observado VARCHAR,
    Apertura_Clientes VARCHAR,
    Apertura_Companeros VARCHAR,
    Comodidad_SF_VS_SM_Companeros VARCHAR,
    Efecto_Revelar_SM_Cliente VARCHAR,
    Efecto_Revelar_SM_Companero VARCHAR,
    Expectativa_Reaccion_Equipo INTEGER CHECK (Expectativa_Reaccion_Equipo BETWEEN 0 AND 10 OR Expectativa_Reaccion_Equipo IS NULL),
    Disposicion_Entrevista_SM INTEGER CHECK (Disposicion_Entrevista_SM IN (0, 1, NULL)),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Experiencia_Trabajo_Actual (
    RespuestaID INTEGER PRIMARY KEY,
    Experiencia_Respuesta_Negativa_SM VARCHAR,
    Discutido_SM_Empleador INTEGER CHECK (Discutido_SM_Empleador IN (0, 1, NULL)),
    Descripcion_Conversacion_Empleador_SM VARCHAR,
    Discutido_SM_Companeros INTEGER CHECK (Discutido_SM_Companeros IN (0, 1, NULL)),
    Descripcion_Conversacion_Companeros_SM VARCHAR,
    Companero_Discutio_SM_Conmigo INTEGER CHECK (Companero_Discutio_SM_Conmigo IN (0, 1, NULL)),
    Descripcion_Conversacion_Companero_SM VARCHAR,
    Contexto_Respuesta_Negativa VARCHAR,
    Percepcion_Apoyo_SM VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

-- Trabajo Anterior
CREATE TABLE IF NOT EXISTS Beneficios_Trabajo_Anterior (
    RespuestaID INTEGER PRIMARY KEY,
    Beneficios_Anteriores VARCHAR,
    Conocimiento_Cobertura_Anterior VARCHAR,
    Comunicacion_Anterior VARCHAR,
    Recursos_Anteriores VARCHAR,
    Privacidad_Anterior VARCHAR,
    Prioridad_Fisica_Anterior INTEGER CHECK (Prioridad_Fisica_Anterior BETWEEN 0 AND 10 OR Prioridad_Fisica_Anterior IS NULL),
    Prioridad_Mental_Anterior INTEGER CHECK (Prioridad_Mental_Anterior BETWEEN 0 AND 10 OR Prioridad_Mental_Anterior IS NULL),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Experiencias_Trabajo_Anterior (
    RespuestaID INTEGER PRIMARY KEY,
    Discutido_SM_Empleador_Anterior INTEGER CHECK (Discutido_SM_Empleador_Anterior IN (0, 1, NULL)),
    Descripcion_Conversacion_Liderazgo_Anterior VARCHAR,
    Discutido_SM_Colegas_Anteriores INTEGER CHECK (Discutido_SM_Colegas_Anteriores IN (0, 1, NULL)),
    Descripcion_Conversacion_Colegas_Anterior VARCHAR,
    Dialogo_Colega_Anterior_SM INTEGER CHECK (Dialogo_Colega_Anterior_SM IN (0, 1, NULL)),
    Relato_Conversacion_Colega_Anterior VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Impacto_Social_Trabajo_Anterior (
    RespuestaID INTEGER PRIMARY KEY,
    Confianza_Liderazgo_Anterior VARCHAR,
    Comodidad_SF_VS_SM_Anterior VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);
    """
    
    try:
        cursor.executescript(script)
        conn.commit()
        print("Tablas creadas correctamente.")
    except sqlite3.Error as e:
        print(f"Error de creación: {e}")
        conn.rollback()
    finally:
        conn.close()
