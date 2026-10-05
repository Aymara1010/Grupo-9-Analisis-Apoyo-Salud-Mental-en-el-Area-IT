import duckdb

def inicializar_bd_duckdb(db_path="mental_health_analitica.duckdb"):
    print(f"Creando / Conectando a la base de datos DuckDB: '{db_path}'...")
    conn = duckdb.connect(db_path)

    ddl_tablas = """
    -- Tablas de Dimensiones
    CREATE TABLE IF NOT EXISTS Dim_Encuesta (
        SurveyID INTEGER PRIMARY KEY,
        Descripción VARCHAR
    );

    CREATE TABLE IF NOT EXISTS Dim_Pais (
        PaisID INTEGER PRIMARY KEY ,
        Pais VARCHAR NOT NULL UNIQUE,
        Region VARCHAR
    );

    CREATE TABLE IF NOT EXISTS Dim_Estado_USA (
        EstadoID INTEGER PRIMARY KEY ,
        Estado VARCHAR NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Dim_Info_Usuario (
        InfoID INTEGER PRIMARY KEY ,
        Genero VARCHAR,
        Raza_Etnia VARCHAR
    );

    CREATE TABLE IF NOT EXISTS Dim_Trabajo_Usuario (
        TrabajoID INTEGER PRIMARY KEY ,
        Freelance VARCHAR,
        Perfil_Tecnologico VARCHAR,
        Empresa_Tech VARCHAR
    );

    CREATE TABLE IF NOT EXISTS Dim_Estado_Mental (
        SaludMentalID INTEGER PRIMARY KEY ,
        Historial VARCHAR,
        Tratamiento VARCHAR,
        Condición_Actual VARCHAR
    );

    CREATE TABLE IF NOT EXISTS Dim_Beneficio_Trabajo (
        BeneficiosID INTEGER PRIMARY KEY ,
        Beneficio VARCHAR,
        Privacidad_Tratamiento VARCHAR,
        Conocimiento_Cobertura VARCHAR
    );

    CREATE TABLE IF NOT EXISTS Dim_Emociones (
        EmocionID INTEGER PRIMARY KEY ,
        Emocion VARCHAR,
        Nivel_Emocion VARCHAR
    );

    -- Tabla de Hechos (con clave primaria compuesta)
    CREATE TABLE IF NOT EXISTS Fact_Respuesta_Usuario (
        UserID INTEGER NOT NULL,
        SurveyID INTEGER NOT NULL,
        InfoID INTEGER,
        SaludMentalID INTEGER,
        TrabajoID INTEGER,
        BeneficiosID INTEGER,
        Pais_Vivienda INTEGER,
        Estado_USA_Vivienda INTEGER,
        Pais_Empleo INTEGER,
        Estado_USA_Empleo INTEGER,
        
        Edad INTEGER,
        Prioridad_Salud_Fisica INTEGER,
        Prioridad_Salud_Mental INTEGER,
        Percepción_Apoyo_SM_Industria INTEGER,
        Experiencia_Respuesta_Negativa_SM VARCHAR,
        Sugerencias_Mejora_SM_Industria VARCHAR,
        Sugerencia VARCHAR,
        Descripcion_Conversacion_Companeros_Sobre_SM VARCHAR,
        Emocion_Conversacion_Companeros INTEGER,
        Descripcion_Conversacion_Sobre_Companero_SM VARCHAR,
        Emocion_Conversacion_Sobre_Companero INTEGER,

        PRIMARY KEY (UserID, SurveyID),

        FOREIGN KEY (SurveyID) REFERENCES Dim_Encuesta(SurveyID),
        FOREIGN KEY (InfoID) REFERENCES Dim_Info_Usuario(InfoID),
        FOREIGN KEY (SaludMentalID) REFERENCES Dim_Estado_Mental(SaludMentalID),
        FOREIGN KEY (TrabajoID) REFERENCES Dim_Trabajo_Usuario(TrabajoID),
        FOREIGN KEY (BeneficiosID) REFERENCES Dim_Beneficio_Trabajo(BeneficiosID),
        FOREIGN KEY (Pais_Vivienda) REFERENCES Dim_Pais(PaisID),
        FOREIGN KEY (Estado_USA_Vivienda) REFERENCES Dim_Estado_USA(EstadoID),
        FOREIGN KEY (Pais_Empleo) REFERENCES Dim_Pais(PaisID),
        FOREIGN KEY (Estado_USA_Empleo) REFERENCES Dim_Estado_USA(EstadoID),
        FOREIGN KEY (Emocion_Conversacion_Companeros) REFERENCES Dim_Emociones(EmocionID),
        FOREIGN KEY (Emocion_Conversacion_Sobre_Companero) REFERENCES Dim_Emociones(EmocionID)
    );
    """

    try:
        conn.execute(ddl_tablas)
        print("Tablas creadas exitosamente.")
        
        tablas = conn.execute("SHOW TABLES;").fetchall()
        print(f"Tablas listas en DuckDB ({len(tablas)}): {[t[0] for t in tablas]}")
    except Exception as e:
        print(f"Error al inicializar las tablas: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    inicializar_bd_duckdb()