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
