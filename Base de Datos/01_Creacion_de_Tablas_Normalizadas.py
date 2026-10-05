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