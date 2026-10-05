import sqlite3
import os

def normalizar_base_de_datos(db_path="mental_health.sqlite"):

    if not os.path.exists(db_path):
        print(f"No se encontró el archivo.")
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

CREATE TABLE IF NOT EXISTS Trabajos (
    PuestoID INTEGER PRIMARY KEY AUTOINCREMENT,
    Puesto_Trabajo_Categoria VARCHAR NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Condiciones (
    CondicionID INTEGER PRIMARY KEY AUTOINCREMENT,
    Condicion VARCHAR NOT NULL UNIQUE
);

-- Encuesta y Preguntas

CREATE TABLE IF NOT EXISTS Encuesta (
    SurveyID INTEGER PRIMARY KEY,
    Description VARCHAR NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Pregunta (
    QuestionID INTEGER PRIMARY KEY,
    QuestionText VARCHAR NOT NULL,
    Tabla_Destino VARCHAR,
    Columna_Destino VARCHAR
);

CREATE TABLE IF NOT EXISTS Pregunta_Encuesta (
    QuestionID INTEGER NOT NULL,
    SurveyID INTEGER NOT NULL,
    PRIMARY KEY (QuestionID, SurveyID),
    FOREIGN KEY (QuestionID) REFERENCES Pregunta(QuestionID) ON DELETE CASCADE,
    FOREIGN KEY (SurveyID) REFERENCES Encuesta(SurveyID) ON DELETE CASCADE
);

-- Respuestas (Núcleo de la bd)
CREATE TABLE IF NOT EXISTS Respuesta (
    RespuestaID INTEGER PRIMARY KEY AUTOINCREMENT,
    UsuarioID INTEGER NOT NULL,
    SurveyID INTEGER NOT NULL,
    FOREIGN KEY (SurveyID) REFERENCES Encuesta(SurveyID) ON DELETE CASCADE,
    UNIQUE(UsuarioID, SurveyID)
);

-- Información General del Usuario
CREATE TABLE IF NOT EXISTS Info_Usuario (
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

CREATE TABLE IF NOT EXISTS Usuarios_Vive_USA (
    RespuestaID INTEGER PRIMARY KEY,
    Estado_USA_Vivienda INTEGER,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (Estado_USA_Vivienda) REFERENCES Estados_USA(EstadoID)
);

CREATE TABLE IF NOT EXISTS Usuarios_Trabaja_USA (
    RespuestaID INTEGER PRIMARY KEY,
    Estado_USA_Empleo INTEGER,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (Estado_USA_Empleo) REFERENCES Estados_USA(EstadoID));

CREATE TABLE IF NOT EXISTS Trabajo_Usuario (
    RespuestaID INTEGER PRIMARY KEY,
    Freelance INTEGER CHECK (Freelance IN (0, 1, NULL)),
    Num_Empleados VARCHAR,
    Empresa_Tec INTEGER CHECK (Empresa_Tec IN (0, 1, NULL)),
    Perfil_Tecnologico INTEGER CHECK (Perfil_Tecnologico IN (0, 1, NULL)),
    Experiencia_Laboral_Previa INTEGER CHECK (Experiencia_Laboral_Previa IN (0, 1, NULL)),
    Empresa_Tec_Anterior INTEGER CHECK (Empresa_Tec_Anterior IN (0, 1, NULL)),
    Trabajo_Remoto_50 VARCHAR,
    Trabajo_Remoto VARCHAR,
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
    Notas_Comentarios_Adicionales VARCHAR,
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE
);

-- Tablas para Relaciones N:M
CREATE TABLE IF NOT EXISTS Trabajo_Respuesta (
    RespuestaID INTEGER NOT NULL,
    PuestoID INTEGER NOT NULL,
    PRIMARY KEY (RespuestaID, PuestoID),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (PuestoID) REFERENCES Trabajos(PuestoID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Condicion_Diagnosticada (
    RespuestaID INTEGER NOT NULL,
    CondicionID INTEGER NOT NULL,
    PRIMARY KEY (RespuestaID, CondicionID),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (CondicionID) REFERENCES Condiciones(CondicionID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Condicion_Sospechada (
    RespuestaID INTEGER NOT NULL,
    CondicionID INTEGER NOT NULL,
    PRIMARY KEY (RespuestaID, CondicionID),
    FOREIGN KEY (RespuestaID) REFERENCES Respuesta(RespuestaID) ON DELETE CASCADE,
    FOREIGN KEY (CondicionID) REFERENCES Condiciones(CondicionID) ON DELETE CASCADE
);
    """
    
    try:
        cursor.executescript(script)
        conn.commit()
        print("Tablas creadas correctamente.")
    except sqlite3.Error as e:
        print("Error de creación")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    normalizar_base_de_datos("mental_health.sqlite")