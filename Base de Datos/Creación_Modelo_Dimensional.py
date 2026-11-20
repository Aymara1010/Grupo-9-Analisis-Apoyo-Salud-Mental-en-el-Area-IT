import duckdb


def crear_tablas(duckdb_path="mental_health_dimensional.duckdb"):
    print(f"Conectando a DuckDB en: {duckdb_path}")
    conn = duckdb.connect(duckdb_path)

    print("Creando secuencias y dimensiones...")

    ddl_base = """
    CREATE SEQUENCE IF NOT EXISTS seq_info START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_trabajo START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_emociones START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_beneficio START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_estado_mental START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_fact_respuesta START 1;

    -- Dimensión Encuesta
    CREATE TABLE IF NOT EXISTS Dim_Encuesta (
        EncuestaID INTEGER PRIMARY KEY,
        Descripcion VARCHAR
    );

    -- Dimensión País
    CREATE TABLE IF NOT EXISTS Dim_Pais (
        PaisID INTEGER PRIMARY KEY,
        Pais VARCHAR,
        Region VARCHAR
    );

    -- Dimensión Estado USA
    CREATE TABLE IF NOT EXISTS Dim_Estado_USA (
        EstadoID INTEGER PRIMARY KEY,
        Estado VARCHAR
    );
    """

    ddl_perfil_y_beneficios = """
    -- Dimensión Info Encuestado
    CREATE TABLE IF NOT EXISTS Dim_Info_Encuestado (
        InfoID INTEGER PRIMARY KEY DEFAULT nextval('seq_info'),
        Genero VARCHAR,
        Raza_Etnia VARCHAR
    );

    -- Dimensión Trabajo Encuestado
    CREATE TABLE IF NOT EXISTS Dim_Trabajo_Encuestado (
        TrabajoID INTEGER PRIMARY KEY DEFAULT nextval('seq_trabajo'),
        Freelance VARCHAR,
        Perfil_Tecnologico VARCHAR,
        Empresa_Tec VARCHAR
    );

    -- Dimensión Beneficio Trabajo
    CREATE TABLE IF NOT EXISTS Dim_Beneficio_Trabajo (
        BeneficiosID INTEGER PRIMARY KEY DEFAULT nextval('seq_beneficio'),
        Beneficio VARCHAR,
        Privacidad_Tratamiento VARCHAR,
        Conocimiento_Cobertura VARCHAR
    );

    -- Dimensión Estado Mental
    CREATE TABLE IF NOT EXISTS Dim_Estado_Mental (
        SaludMentalID INTEGER PRIMARY KEY DEFAULT nextval('seq_estado_mental'),
        Historial VARCHAR,
        Tratamiento VARCHAR,
        Condicion_Actual VARCHAR
    );

    -- Dimensión Emociones
    CREATE TABLE IF NOT EXISTS Dim_Emociones (
        EmocionID INTEGER PRIMARY KEY DEFAULT nextval('seq_emociones'),
        Emocion VARCHAR,
        Nivel_Emocion VARCHAR
    );

    -- Sugerencias
    CREATE TABLE IF NOT EXISTS Dim_Categorias_Sugerencia (
        CategoriaID INTEGER PRIMARY KEY,
        Categoria VARCHAR,
        Descripcion VARCHAR
    );
    """

    try:
        conn.execute(ddl_base)
        conn.execute(ddl_perfil_y_beneficios)
        print("Dimensiones creadas.")
    except Exception as e:
        print(f"Error al inicializar dimensiones: {e}")
    finally:
        conn.close()
        
def crear_tabla_hechos(duckdb_path="mental_health_dimensional.duckdb"):
    conn = duckdb.connect(duckdb_path)

    ddl_hechos = """
    -- Tabla de Hechos Principal
    CREATE TABLE IF NOT EXISTS Fact_Respuesta_Encuestado (
        RespuestaID INTEGER PRIMARY KEY DEFAULT nextval('seq_fact_respuesta'),

        EncuestadoID INTEGER,
        EncuestaID INTEGER,
        InfoID INTEGER,
        SaludMentalID INTEGER,
        TrabajoID INTEGER,
        BeneficiosID INTEGER,
        Pais_Vivienda INTEGER,
        Estado_USA_Vivienda INTEGER,
        Pais_Empleo INTEGER,
        Estado_USA_Empleo INTEGER,

        Edad FLOAT,
        Prioridad_Salud_Fisica INTEGER,
        Prioridad_Salud_Mental INTEGER,
        Percepcion_Apoyo_SM_Industria INTEGER,
        Experiencia_Respuesta_Negativa_SM VARCHAR,
        Sugerencias_Mejora_SM_Industria VARCHAR,
        Categoria_Sugerencia_ID INTEGER,
        Descripcion_Conversacion_Companeros_Sobre_SM VARCHAR,
        Emocion_Conversacion_Companeros INTEGER,
        Descripcion_Conversacion_Sobre_Companero_SM VARCHAR,
        Emocion_Conversacion_Sobre_Companero INTEGER,

        FOREIGN KEY (EncuestaID) REFERENCES Dim_Encuesta(EncuestaID),
        FOREIGN KEY (InfoID) REFERENCES Dim_Info_Encuestado(InfoID),
        FOREIGN KEY (SaludMentalID) REFERENCES Dim_Estado_Mental(SaludMentalID),
        FOREIGN KEY (TrabajoID) REFERENCES Dim_Trabajo_Encuestado(TrabajoID),
        FOREIGN KEY (BeneficiosID) REFERENCES Dim_Beneficio_Trabajo(BeneficiosID),
        FOREIGN KEY (Pais_Vivienda) REFERENCES Dim_Pais(PaisID),
        FOREIGN KEY (Estado_USA_Vivienda) REFERENCES Dim_Estado_USA(EstadoID),
        FOREIGN KEY (Pais_Empleo) REFERENCES Dim_Pais(PaisID),
        FOREIGN KEY (Estado_USA_Empleo) REFERENCES Dim_Estado_USA(EstadoID),
        FOREIGN KEY (Emocion_Conversacion_Companeros) REFERENCES Dim_Emociones(EmocionID),
        FOREIGN KEY (Emocion_Conversacion_Sobre_Companero) REFERENCES Dim_Emociones(EmocionID),
        FOREIGN KEY (Categoria_Sugerencia_ID) REFERENCES Dim_Categorias_Sugerencia(CategoriaID)
    );
    """

    try:
        conn.execute(ddl_hechos)
        print("Tabla de hechos creada.")
    except Exception as e:
        print(f"Error al crear tabla de hechos: {e}")
    finally:
        conn.close()