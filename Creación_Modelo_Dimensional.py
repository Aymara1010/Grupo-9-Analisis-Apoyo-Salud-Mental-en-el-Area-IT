import duckdb
from matplotlib.pylab import cond

def crear_tablas(duckdb_path="mental_health_dimensional.duckdb"):
    print(f"Conectando a DuckDB en: {duckdb_path}")
    conn = duckdb.connect(duckdb_path)

    print("Creando secuencias y dimensiones base...")

    ddl_base = """
    CREATE SEQUENCE IF NOT EXISTS seq_info START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_trabajo START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_emociones START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_beneficio START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_estado_mental START 1;
    CREATE SEQUENCE IF NOT EXISTS seq_fact_respuesta START 1;

    -- Dimensión Encuesta
    CREATE TABLE IF NOT EXISTS Dim_Encuesta (
        SurveyID INTEGER PRIMARY KEY,
        Descripción VARCHAR
    );

    -- Dimensión País
    CREATE TABLE IF NOT EXISTS Dim_Pais (
        PaisID INTEGER PRIMARY KEY,
        Pais VARCHAR NOT NULL UNIQUE,
        Region VARCHAR
    );

    -- Dimensión Estado USA
    CREATE TABLE IF NOT EXISTS Dim_Estado_USA (
        EstadoID INTEGER PRIMARY KEY,
        Estado VARCHAR NOT NULL UNIQUE
    );
    """
    try:
        conn.execute(ddl_base)
        print("Tablas base creadas.")
    except Exception as e:
        print(f"Error al inicializar tablas base: {e}")
    finally:
        conn.close()

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
    """
try:
    cond.execute(ddl_perfil_y_beneficios)

    print("Dimensiones de perfil y beneficios creadas.")

except Exception as e:
        print(f"Error al inicializar perfil y beneficios: {e}")