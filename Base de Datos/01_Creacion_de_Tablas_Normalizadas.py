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
    Empresa_Seriedad_SM_VS_SF VARCHAR,
    Conocimiento_Opciones_SM_Empleador VARCHAR,
    Empresa_Programa_Bienestar_SM VARCHAR,
    Empresa_Recursos_Ayuda_SM VARCHAR,
    Facilidad_Licencia_Medica_SM VARCHAR,
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
    Interferencia_SM_Trabajo_General VARCHAR,
    Perjuicio_Carrera_SM VARCHAR,
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
    Empresa_Anterior_Seriedad_SM_VS_SF VARCHAR,
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
    Consecuencias_SM_Empleador_Anterior VARCHAR,
    Consecuencias_SF_Empleador_Anterior VARCHAR,
    Disposicion_SM_Companeros_Anteriores VARCHAR,
    Consecuencias_SM_Companeros_Anteriores VARCHAR,
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