import pandas as pd
import streamlit as st

# 1. Estilo visual en gama morada acorde a TechWell
st.markdown(
    """
<style>
.tarjeta-diccionario {
    background-color: #F8F4FF;
    border-left: 8px solid #3C096C;
    border-radius: 10px;
    padding: 14px 18px;
    font-family: sans-serif;
    color: black;
    margin-bottom: 14px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.06);
}
.titulo-diccionario {
    font-size: 17px;
    font-weight: bold;
    margin: 0 0 4px 0;
    color: #3C096C;
}
.texto-diccionario {
    font-size: 14px;
    margin: 0;
    line-height: 1.45;
}
</style>
""",
    unsafe_allow_html=True,
)

# 2. Diccionario de datos sincronizado con modelo_dimensional.main
DICCIONARIO_DATOS = [
    # --- Dim_Beneficio_Trabajo ---
    {
        "Tabla": "Dim_Beneficio_Trabajo",
        "Campo": "BeneficiosID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único de la configuración de beneficios laborales de salud mental.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Beneficio_Trabajo",
        "Campo": "Beneficio",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Indica si el empleador incluye cobertura o beneficios de salud mental.",
        "Valores / Reglas": "Utilizado en análisis de cobertura y ausencia de beneficios.",
    },
    {
        "Tabla": "Dim_Beneficio_Trabajo",
        "Campo": "Privacidad_Tratamiento",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Indica si la privacidad o anonimato de quien busca tratamiento está protegida.",
        "Valores / Reglas": "Categoría descriptiva de política laboral.",
    },
    {
        "Tabla": "Dim_Beneficio_Trabajo",
        "Campo": "Conocimiento_Cobertura",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Indica si la persona conoce las opciones de cobertura o recursos de salud mental.",
        "Valores / Reglas": "Evaluado en métricas de conocimiento de beneficios.",
    },
   
    # --- Dim_Categorias_Sugerencia ---
    {
        "Tabla": "Dim_Categorias_Sugerencia",
        "Campo": "CategoriaID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único de la categoría de sugerencia o mejora.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Categorias_Sugerencia",
        "Campo": "Categoria",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Desestigmatización y Cultura Abierta",
        "Descripción": "Agrupación temática de la sugerencia propuesta para la industria tecnológica.",
        "Valores / Reglas": "Utilizada en el análisis de demandas y sugerencias (Objetivo 6).",
    },
    {
        "Tabla": "Dim_Categorias_Sugerencia",
        "Campo": "Descripcion",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Promover espacios abiertos sin estigma",
        "Descripción": "Detalle explicativo asociado a la categoría de sugerencia.",
        "Valores / Reglas": "Texto descriptivo.",
    },
    # --- Dim_Emociones ---
    {
        "Tabla": "Dim_Emociones",
        "Campo": "EmocionID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único de la emoción registrada en conversaciones laborales.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Emociones",
        "Campo": "Emocion",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Positiva / Apoyo",
        "Descripción": "Emoción o actitud identificada en conversaciones sobre salud mental.",
        "Valores / Reglas": "Referenciada desde Emocion_Conversacion_Companeros y Emocion_Conversacion_Sobre_Companero.",
    },
    {
        "Tabla": "Dim_Emociones",
        "Campo": "Nivel_Emocion",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Alto",
        "Descripción": "Clasificación o intensidad asociada a la emoción.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    # --- Dim_Encuesta ---
    {
        "Tabla": "Dim_Encuesta",
        "Campo": "EncuestaID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "2019",
        "Descripción": "Identificador único de la edición o encuesta OSMI.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Encuesta",
        "Campo": "Descripcion",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "OSMI Mental Health in Tech Survey",
        "Descripción": "Descripción de la edición o levantamiento de la encuesta.",
        "Valores / Reglas": "Texto descriptivo.",
    },
   
    # --- Dim_Estado_Mental ---
    {
        "Tabla": "Dim_Estado_Mental",
        "Campo": "SaludMentalID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único del registro de estado o historial de salud mental.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Estado_Mental",
        "Campo": "Historial",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Indica si existe historial familiar o previo de condiciones de salud mental.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    {
        "Tabla": "Dim_Estado_Mental",
        "Campo": "Tratamiento",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Indica si la persona encuestada ha buscado tratamiento profesional por salud mental.",
        "Valores / Reglas": "Normalizado en el flujo analítico.",
    },
    {
        "Tabla": "Dim_Estado_Mental",
        "Campo": "Condicion_Actual",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Possibly",
        "Descripción": "Estado actual percibido o diagnosticado de salud mental del encuestado.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    # --- Dim_Estado_USA ---
    {
        "Tabla": "Dim_Estado_USA",
        "Campo": "EstadoID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único del estado de Estados Unidos.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Estado_USA",
        "Campo": "Estado",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "California",
        "Descripción": "Nombre del estado de EE. UU. asociado a vivienda o empleo.",
        "Valores / Reglas": "Texto descriptivo.",
    },
    # --- Dim_Info_Encuestado ---
    {
        "Tabla": "Dim_Info_Encuestado",
        "Campo": "InfoID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único del perfil sociodemográfico del encuestado.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Info_Encuestado",
        "Campo": "Genero",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Female",
        "Descripción": "Género reportado por la persona encuestada.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    {
        "Tabla": "Dim_Info_Encuestado",
        "Campo": "Raza_Etnia",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "White",
        "Descripción": "Raza o grupo étnico reportado por la persona encuestada.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    # --- Dim_Pais ---
    {
        "Tabla": "Dim_Pais",
        "Campo": "PaisID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único del país.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Pais",
        "Campo": "Pais",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "United States",
        "Descripción": "Nombre del país de vivienda o empleo.",
        "Valores / Reglas": "Texto descriptivo.",
    },
    {
        "Tabla": "Dim_Pais",
        "Campo": "Region",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Europa y Oceanía",
        "Descripción": "Macroregión geográfica asignada al país.",
        "Valores / Reglas": "Ej. USA, Europa y Oceanía.",
    },
  # --- Dim_Trabajo_Encuestado ---
    {
        "Tabla": "Dim_Trabajo_Encuestado",
        "Campo": "TrabajoID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único del contexto laboral del encuestado.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Dim_Trabajo_Encuestado",
        "Campo": "Freelance",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "No",
        "Descripción": "Indica si la persona trabaja de forma independiente o freelance.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    {
        "Tabla": "Dim_Trabajo_Encuestado",
        "Campo": "Perfil_Tecnologico",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Back-end Developer",
        "Descripción": "Rol o perfil técnico desempeñado por el encuestado.",
        "Valores / Reglas": "Base para agrupaciones de puesto / perfil.",
    },
    {
        "Tabla": "Dim_Trabajo_Encuestado",
        "Campo": "Empresa_Tec",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Indica si la organización principal es o no de tecnología.",
        "Valores / Reglas": "Categoría descriptiva.",
    },
    # --- Fact_Respuesta_Encuestado ---
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "RespuestaID",
        "Tipo": "INTEGER",
        "Permite NULL": "No",
        "Clave / Relación": "PK",
        "Ejemplo": "1",
        "Descripción": "Identificador único de cada respuesta registrada en la tabla de hechos.",
        "Valores / Reglas": "Clave primaria entera no nula.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "EncuestadoID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo / Identificador",
        "Ejemplo": "1001",
        "Descripción": "Identificador del participante dentro de la encuesta.",
        "Valores / Reglas": "Entero.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "EncuestaID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Encuesta.EncuestaID",
        "Ejemplo": "2019",
        "Descripción": "Referencia a la edición de encuesta a la que pertenece la respuesta.",
        "Valores / Reglas": "Vinculado a Dim_Encuesta.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "InfoID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Info_Encuestado.InfoID",
        "Ejemplo": "1",
        "Descripción": "Referencia al perfil sociodemográfico del encuestado.",
        "Valores / Reglas": "Vinculado a Dim_Info_Encuestado.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "SaludMentalID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Estado_Mental.SaludMentalID",
        "Ejemplo": "1",
        "Descripción": "Referencia al estado y tratamiento de salud mental del encuestado.",
        "Valores / Reglas": "Vinculado a Dim_Estado_Mental.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "TrabajoID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Trabajo_Encuestado.TrabajoID",
        "Ejemplo": "1",
        "Descripción": "Referencia al perfil laboral y tipo de empresa del encuestado.",
        "Valores / Reglas": "Vinculado a Dim_Trabajo_Encuestado.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "BeneficiosID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Beneficio_Trabajo.BeneficiosID",
        "Ejemplo": "1",
        "Descripción": "Referencia a las condiciones y beneficios de salud mental en el trabajo.",
        "Valores / Reglas": "Vinculado a Dim_Beneficio_Trabajo.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Pais_Vivienda",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Pais.PaisID",
        "Ejemplo": "1",
        "Descripción": "País de residencia o vivienda de la persona encuestada.",
        "Valores / Reglas": "Vinculado a Dim_Pais.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Estado_USA_Vivienda",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Estado_USA.EstadoID",
        "Ejemplo": "1",
        "Descripción": "Estado de EE. UU. de residencia, cuando aplica.",
        "Valores / Reglas": "Vinculado a Dim_Estado_USA.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Pais_Empleo",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Pais.PaisID",
        "Ejemplo": "1",
        "Descripción": "País donde desempeña su empleo la persona encuestada.",
        "Valores / Reglas": "Base para agrupaciones regionales por empleo.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Estado_USA_Empleo",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Estado_USA.EstadoID",
        "Ejemplo": "1",
        "Descripción": "Estado de EE. UU. donde labora el encuestado, cuando aplica.",
        "Valores / Reglas": "Vinculado a Dim_Estado_USA.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Edad",
        "Tipo": "FLOAT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica / Atributo numérico",
        "Ejemplo": "29.0",
        "Descripción": "Edad reportada por la persona encuestada.",
        "Valores / Reglas": "Numérico decimal (FLOAT).",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Prioridad_Salud_Fisica",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica numérica",
        "Ejemplo": "7",
        "Descripción": "Puntaje de prioridad otorgado a la salud física.",
        "Valores / Reglas": "Numérico entero.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Prioridad_Salud_Mental",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica numérica",
        "Ejemplo": "5",
        "Descripción": "Puntaje de prioridad otorgado a la salud mental.",
        "Valores / Reglas": "Usado en promedios y dispersión de prioridad.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Percepcion_Apoyo_SM_Industria",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica numérica",
        "Ejemplo": "3",
        "Descripción": "Calificación o percepción del apoyo a la salud mental en la industria.",
        "Valores / Reglas": "Numérico entero.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Experiencia_Respuesta_Negativa_SM",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Yes",
        "Descripción": "Registro de experiencia o reacción negativa tras abordar salud mental.",
        "Valores / Reglas": "Texto / categoría descriptiva.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Sugerencias_Mejora_SM_Industria",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Mayor flexibilidad laboral",
        "Descripción": "Sugerencia abierta o detalle de mejora expresado por el encuestado.",
        "Valores / Reglas": "Texto descriptivo.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Categoria_Sugerencia_ID",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Categorias_Sugerencia.CategoriaID",
        "Ejemplo": "1",
        "Descripción": "Referencia a la categoría temática asignada a la sugerencia.",
        "Valores / Reglas": "Vinculado a Dim_Categorias_Sugerencia.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Descripcion_Conversacion_Companeros_Sobre_SM",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Conversación informal sobre estrés",
        "Descripción": "Detalle de conversaciones mantenidas con compañeros sobre salud mental.",
        "Valores / Reglas": "Texto descriptivo.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Emocion_Conversacion_Companeros",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Emociones.EmocionID",
        "Ejemplo": "1",
        "Descripción": "Referencia a la emoción asociada a conversaciones con compañeros.",
        "Valores / Reglas": "Vinculado a Dim_Emociones.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Descripcion_Conversacion_Sobre_Companero_SM",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo",
        "Ejemplo": "Apoyo ante carga laboral",
        "Descripción": "Detalle de conversaciones o situaciones vinculadas a la salud mental de un compañero.",
        "Valores / Reglas": "Texto descriptivo.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Emocion_Conversacion_Sobre_Companero",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK → Dim_Emociones.EmocionID",
        "Ejemplo": "1",
        "Descripción": "Referencia a la emoción registrada sobre conversaciones de salud mental de un compañero.",
        "Valores / Reglas": "Vinculado a Dim_Emociones.",
    },
    # Tablas base 
    {
        "Tabla": "answer",
        "Campo": "AnswerText",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo base",
        "Ejemplo": "Yes",
        "Descripción": "Respuesta textual o categórica cruda capturada en la encuesta.",
        "Valores / Reglas": "Tabla fuente raw en modelo_dimensional.main.",
    },
    {
        "Tabla": "answer",
        "Campo": "SurveyID",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK lógica → survey.SurveyID",
        "Ejemplo": "2019",
        "Descripción": "Identificador de encuesta asociado a la respuesta raw.",
        "Valores / Reglas": "BIGINT.",
    },
    {
        "Tabla": "answer",
        "Campo": "UserID",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Identificador de usuario",
        "Ejemplo": "101",
        "Descripción": "Identificador del usuario encuestado en el origen raw.",
        "Valores / Reglas": "BIGINT.",
    },
    {
        "Tabla": "answer",
        "Campo": "QuestionID",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "FK lógica → question.questionid",
        "Ejemplo": "1",
        "Descripción": "Identificador de la pregunta respondida en el origen raw.",
        "Valores / Reglas": "BIGINT.",
    },
    {
        "Tabla": "question",
        "Campo": "questiontext",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo base",
        "Ejemplo": "Does your employer provide mental health benefits?",
        "Descripción": "Texto literal de la pregunta de la encuesta.",
        "Valores / Reglas": "Tabla fuente raw en modelo_dimensional.main.",
    },
    {
        "Tabla": "question",
        "Campo": "questionid",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "PK lógica",
        "Ejemplo": "1",
        "Descripción": "Identificador único de la pregunta en la tabla question.",
        "Valores / Reglas": "BIGINT.",
    },
    {
        "Tabla": "survey",
        "Campo": "SurveyID",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "PK lógica",
        "Ejemplo": "2019",
        "Descripción": "Identificador de la encuesta en la tabla base survey.",
        "Valores / Reglas": "BIGINT.",
    },
    {
        "Tabla": "survey",
        "Campo": "Description",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo base",
        "Ejemplo": "OSMI 2019",
        "Descripción": "Descripción general de la encuesta en la tabla base.",
        "Valores / Reglas": "VARCHAR.",
    },
    # --- Vistas analíticas principales (Objetivo_Uno a Objetivo_Seis) ---
    {
        "Tabla": "Objetivo_Uno",
        "Campo": "region_agrupada",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "USA",
        "Descripción": "Región agrupada evaluada en la vista Objetivo_Uno.",
        "Valores / Reglas": "Vista analítica en modelo_dimensional.main.",
    },
    {
        "Tabla": "Objetivo_Uno",
        "Campo": "Ofrece_Beneficios",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Categoría (VIEW)",
        "Ejemplo": "Yes",
        "Descripción": "Indica si la empresa ofrece beneficios de salud mental.",
        "Valores / Reglas": "Vista Objetivo_Uno.",
    },
    {
        "Tabla": "Objetivo_Uno",
        "Campo": "Total_Empresas",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "500",
        "Descripción": "Conteo total de empresas o registros en la categoría.",
        "Valores / Reglas": "Vista Objetivo_Uno.",
    },
    {
        "Tabla": "Objetivo_Uno",
        "Campo": "Frecuencia_Relativa_Porcentaje",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica porcentual (VIEW)",
        "Ejemplo": "62.5",
        "Descripción": "Porcentaje relativo dentro de la agrupación.",
        "Valores / Reglas": "Vista Objetivo_Uno.",
    },
    {
        "Tabla": "Objetivo_Dos",
        "Campo": "Region_Agrupada",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "Europa y Oceanía",
        "Descripción": "Región agrupada analizada en Objetivo_Dos.",
        "Valores / Reglas": "Vista Objetivo_Dos.",
    },
    {
        "Tabla": "Objetivo_Dos",
        "Campo": "Total_Respuestas_Definitivas",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "300",
        "Descripción": "Total de respuestas definitivas consideradas.",
        "Valores / Reglas": "Vista Objetivo_Dos.",
    },
    {
        "Tabla": "Objetivo_Dos",
        "Campo": "Conocen_SI",
        "Tipo": "HUGEINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "180",
        "Descripción": "Cantidad de respuestas afirmativas sobre conocimiento de cobertura.",
        "Valores / Reglas": "Vista Objetivo_Dos.",
    },
    {
        "Tabla": "Objetivo_Dos",
        "Campo": "Conocen_NO",
        "Tipo": "HUGEINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "120",
        "Descripción": "Cantidad de respuestas negativas sobre conocimiento de cobertura.",
        "Valores / Reglas": "Vista Objetivo_Dos.",
    },
    {
        "Tabla": "Objetivo_Dos",
        "Campo": "Proporcion_SI_PCT",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica porcentual (VIEW)",
        "Ejemplo": "60.0",
        "Descripción": "Porcentaje de respuestas afirmativas ('Sí').",
        "Valores / Reglas": "Vista Objetivo_Dos.",
    },
    {
        "Tabla": "Objetivo_Dos",
        "Campo": "Proporcion_NO_PCT",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica porcentual (VIEW)",
        "Ejemplo": "40.0",
        "Descripción": "Porcentaje de respuestas negativas ('No').",
        "Valores / Reglas": "Vista Objetivo_Dos.",
    },
    {
        "Tabla": "Objetivo_Tres",
        "Campo": "Categoria_Puesto",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "Desarrollo / Ingeniería",
        "Descripción": "Categoría de puesto o rol analizada en Objetivo_Tres.",
        "Valores / Reglas": "Vista Objetivo_Tres.",
    },
    {
        "Tabla": "Objetivo_Tres",
        "Campo": "Region_Agrupada",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "USA",
        "Descripción": "Región agrupada comparada en Objetivo_Tres.",
        "Valores / Reglas": "Vista Objetivo_Tres.",
    },
    {
        "Tabla": "Objetivo_Tres",
        "Campo": "Total_Respuestas",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "250",
        "Descripción": "Total de respuestas por categoría y región.",
        "Valores / Reglas": "Vista Objetivo_Tres.",
    },
    {
        "Tabla": "Objetivo_Tres",
        "Campo": "Promedio_Prioridad",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "5.12",
        "Descripción": "Promedio del puntaje de prioridad de salud mental.",
        "Valores / Reglas": "Vista Objetivo_Tres.",
    },
    {
        "Tabla": "Objetivo_Tres",
        "Campo": "Dispersion_Prioridad",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "2.25",
        "Descripción": "Dispersión del puntaje de prioridad de salud mental.",
        "Valores / Reglas": "Vista Objetivo_Tres.",
    },
    {
        "Tabla": "Objetivo_Cuatro",
        "Campo": "Region_Agrupada",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "USA",
        "Descripción": "Región agrupada evaluada en Objetivo_Cuatro.",
        "Valores / Reglas": "Vista Objetivo_Cuatro.",
    },
    {
        "Tabla": "Objetivo_Cuatro",
        "Campo": "Calificacion_Apoyo",
        "Tipo": "INTEGER",
        "Permite NULL": "Sí",
        "Clave / Relación": "Categoría numérica (VIEW)",
        "Ejemplo": "4",
        "Descripción": "Nivel o calificación de apoyo de salud mental.",
        "Valores / Reglas": "Vista Objetivo_Cuatro.",
    },
    {
        "Tabla": "Objetivo_Cuatro",
        "Campo": "Frecuencia_Absoluta",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "140",
        "Descripción": "Frecuencia absoluta de respuestas por calificación y región.",
        "Valores / Reglas": "Vista Objetivo_Cuatro.",
    },
    {
        "Tabla": "Objetivo_Cuatro",
        "Campo": "Porcentaje_Concentracion",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica porcentual (VIEW)",
        "Ejemplo": "28.4",
        "Descripción": "Porcentaje de concentración de la calificación en la región.",
        "Valores / Reglas": "Vista Objetivo_Cuatro.",
    },
    {
        "Tabla": "Objetivo_Cinco",
        "Campo": "Region_Agrupada",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "Europa y Oceanía",
        "Descripción": "Región agrupada comparada en Objetivo_Cinco.",
        "Valores / Reglas": "Vista Objetivo_Cinco.",
    },
    {
        "Tabla": "Objetivo_Cinco",
        "Campo": "Total_Respuestas",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "346",
        "Descripción": "Cantidad total de respuestas válidas en la región.",
        "Valores / Reglas": "Vista Objetivo_Cinco.",
    },
    {
        "Tabla": "Objetivo_Cinco",
        "Campo": "Promedio_Prioridad",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "5.04",
        "Descripción": "Promedio de prioridad de salud mental en la región.",
        "Valores / Reglas": "Vista Objetivo_Cinco.",
    },
    {
        "Tabla": "Objetivo_Cinco",
        "Campo": "Dispersion_Prioridad",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "2.22",
        "Descripción": "Dispersión del puntaje de prioridad en la región.",
        "Valores / Reglas": "Vista Objetivo_Cinco.",
    },
    {
        "Tabla": "Objetivo_Seis",
        "Campo": "Region",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Dimensión / Agrupación (VIEW)",
        "Ejemplo": "USA",
        "Descripción": "Región evaluada en Objetivo_Seis.",
        "Valores / Reglas": "Vista Objetivo_Seis.",
    },
    {
        "Tabla": "Objetivo_Seis",
        "Campo": "Categoria_Sugerencia",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Categoría (VIEW)",
        "Ejemplo": "Desestigmatización y Cultura Abierta",
        "Descripción": "Categoría principal de sugerencia o demanda.",
        "Valores / Reglas": "Vista Objetivo_Seis.",
    },
    {
        "Tabla": "Objetivo_Seis",
        "Campo": "Detalle_Categoria",
        "Tipo": "VARCHAR",
        "Permite NULL": "Sí",
        "Clave / Relación": "Atributo descriptivo (VIEW)",
        "Ejemplo": "Capacitación y comunicación abierta",
        "Descripción": "Detalle específico de la sugerencia dentro de la categoría.",
        "Valores / Reglas": "Vista Objetivo_Seis.",
    },
    {
        "Tabla": "Objetivo_Seis",
        "Campo": "Total_Menciones",
        "Tipo": "BIGINT",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica (VIEW)",
        "Ejemplo": "85",
        "Descripción": "Número total de menciones registradas.",
        "Valores / Reglas": "Vista Objetivo_Seis.",
    },
    {
        "Tabla": "Objetivo_Seis",
        "Campo": "Porcentaje_Region",
        "Tipo": "DOUBLE",
        "Permite NULL": "Sí",
        "Clave / Relación": "Métrica porcentual (VIEW)",
        "Ejemplo": "24.5",
        "Descripción": "Peso porcentual de la sugerencia dentro de la región.",
        "Valores / Reglas": "Vista Objetivo_Seis.",
    },
]

# Relaciones reales identificadas en Fact_Respuesta_Encuestado
RELACIONES_MODELO = [
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "EncuestaID",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Encuesta",
        "Campo Destino": "EncuestaID",
        "Uso Principal": "Identificación de edición de encuesta",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "InfoID",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Info_Encuestado",
        "Campo Destino": "InfoID",
        "Uso Principal": "Perfil sociodemográfico (género, raza/etnia)",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "SaludMentalID",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Estado_Mental",
        "Campo Destino": "SaludMentalID",
        "Uso Principal": "Historial, tratamiento y condición actual de salud mental",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "TrabajoID",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Trabajo_Encuestado",
        "Campo Destino": "TrabajoID",
        "Uso Principal": "Perfil tecnológico, tipo de empresa y modalidad freelance",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "BeneficiosID",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Beneficio_Trabajo",
        "Campo Destino": "BeneficiosID",
        "Uso Principal": "Beneficios laborales, privacidad y conocimiento de cobertura",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Pais_Vivienda",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Pais",
        "Campo Destino": "PaisID",
        "Uso Principal": "País de residencia del encuestado",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Estado_USA_Vivienda",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Estado_USA",
        "Campo Destino": "EstadoID",
        "Uso Principal": "Estado de EE. UU. de residencia",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Pais_Empleo",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Pais",
        "Campo Destino": "PaisID",
        "Uso Principal": "País y región de empleo para comparaciones regionales",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Estado_USA_Empleo",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Estado_USA",
        "Campo Destino": "EstadoID",
        "Uso Principal": "Estado de EE. UU. de empleo",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Categoria_Sugerencia_ID",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Categorias_Sugerencia",
        "Campo Destino": "CategoriaID",
        "Uso Principal": "Clasificación temática de sugerencias de mejora",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Emocion_Conversacion_Companeros",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Emociones",
        "Campo Destino": "EmocionID",
        "Uso Principal": "Emoción en conversaciones con compañeros",
    },
    {
        "Tabla Origen": "Fact_Respuesta_Encuestado",
        "Campo Origen": "Emocion_Conversacion_Sobre_Companero",
        "Cardinalidad": "N : 1",
        "Tabla Destino": "Dim_Emociones",
        "Campo Destino": "EmocionID",
        "Uso Principal": "Emoción en conversaciones sobre un compañero",
    },
]
# Mapeo con vistas 
MAPEO_VISTAS = [
    {
        "Sección / Vista": "Objetivo_Uno",
        "Tipo": "VIEW",
        "Campos Clave": "region_agrupada, Ofrece_Beneficios",
        "Métricas": "Total_Empresas, Frecuencia_Relativa_Porcentaje",
    },
    {
        "Sección / Vista": "Objetivo_Dos",
        "Tipo": "VIEW",
        "Campos Clave": "Region_Agrupada",
        "Métricas": "Total_Respuestas_Definitivas, Conocen_SI, Conocen_NO, Proporcion_SI_PCT, Proporcion_NO_PCT",
    },
    {
        "Sección / Vista": "Objetivo_Tres",
        "Tipo": "VIEW",
        "Campos Clave": "Categoria_Puesto, Region_Agrupada",
        "Métricas": "Total_Respuestas, Promedio_Prioridad, Dispersion_Prioridad",
    },
    {
        "Sección / Vista": "Objetivo_Cuatro",
        "Tipo": "VIEW",
        "Campos Clave": "Region_Agrupada, Calificacion_Apoyo",
        "Métricas": "Frecuencia_Absoluta, Porcentaje_Concentracion",
    },
    {
        "Sección / Vista": "Objetivo_Cinco",
        "Tipo": "VIEW",
        "Campos Clave": "Region_Agrupada",
        "Métricas": "Total_Respuestas, Promedio_Prioridad, Dispersion_Prioridad",
    },
    {
        "Sección / Vista": "Objetivo_Seis",
        "Tipo": "VIEW",
        "Campos Clave": "Region, Categoria_Sugerencia, Detalle_Categoria",
        "Métricas": "Total_Menciones, Porcentaje_Region",
    },
    {
        "Sección / Vista": "Pregunta_Uno a Pregunta_Seis",
        "Tipo": "VIEW",
        "Campos Clave": "Edición / Edicion, dimensiones y rankings por vista",
        "Métricas": "Porcentajes, proporciones, brechas, rankings y acumulados",
    },
]
df_diccionario = pd.DataFrame(DICCIONARIO_DATOS)
df_relaciones = pd.DataFrame(RELACIONES_MODELO)
df_vistas = pd.DataFrame(MAPEO_VISTAS)

# Encabezado 
st.title("📚 Diccionario de Datos")
st.markdown(
    """
<div class="tarjeta-diccionario">
    <p class="titulo-diccionario">Catálogo De Datos</p>
    <p class="texto-diccionario">
        Documentación sincronizada de tablas dimensionales, tabla de hechos, tablas base y vistas
        analíticas registradas en MotherDuck.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Objetos Documentados", df_diccionario["Tabla"].nunique())
m2.metric("Campos Registrados", len(df_diccionario))
m3.metric("Relaciones (FK)", len(df_relaciones))
m4.metric("Vistas Mapeadas", len(df_vistas))

with st.expander("💡 Mini tutorial: cómo usar el diccionario", expanded=False):
  st.markdown(
      """
        <div class="tarjeta-diccionario">
            <p class="titulo-diccionario">Guía rápida de navegación</p>
            <p class="texto-diccionario">
                <b>1. Filtra por tabla o vista:</b> selecciona una dimensión (<code>Dim_</code>), la tabla de hechos
                (<code>Fact_Respuesta_Encuestado</code>) o una vista analítica (<code>Objetivo_Uno</code> a <code>Objetivo_Seis</code>).<br>
                <b>2. Combina tipo de dato y búsqueda:</b> filtra por <code>INTEGER</code>, <code>VARCHAR</code>, <code>DOUBLE</code> o <code>BIGINT</code>,
                y escribe palabras clave como <code>FK</code>, <code>Region</code>, <code>Prioridad</code> o <code>Beneficio</code>.<br>
                <b>3. Revisa relaciones y vistas:</b> usa las pestañas <b>Relaciones (Fact / Dim)</b> y <b>Vistas Analíticas</b> para ver
                cómo conectan las llaves foráneas y qué métricas alimenta cada vista.<br>
                <b>4. Exporta o reinicia:</b> descarga el resultado filtrado en <b>CSV</b> o pulsa <b>Limpiar filtros</b> para volver al catálogo completo.
            </p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # Pestañas principales
tab_campos, tab_relaciones, tab_vistas = st.tabs([
    "📋 Diccionario de Campos",
    "🔗 Relaciones (Fact / Dim)",
    "📊 Vistas Analíticas",
])

with tab_campos:
    reset_id = st.session_state.get("dic_reset_id", 0)

    if st.button("🔄 Limpiar filtros", key="limpiar_filtros_dic"):
        st.session_state["dic_reset_id"] = reset_id + 1
        st.rerun()

    col_f1, col_f2, col_f3 = st.columns([1.3, 1, 1.7])

    with col_f1:
        tablas_disponibles = ["Todas"] + sorted(
            df_diccionario["Tabla"].unique().tolist()
        )
        tabla_seleccionada = st.selectbox(
            "Filtrar por tabla o vista:",
            tablas_disponibles,
            key=f"filtro_tabla_diccionario_{reset_id}",
        )

    with col_f2:
        tipos_disponibles = ["Todos"] + sorted(
            df_diccionario["Tipo"].unique().tolist()
        )
        tipo_seleccionado = st.selectbox(
            "Tipo de dato:",
            tipos_disponibles,
            key=f"filtro_tipo_diccionario_{reset_id}",
        )

    with col_f3:
        busqueda = st.text_input(
            "Buscar campo, relación o regla:",
            placeholder="Ej. BeneficiosID, Region, FK, DOUBLE...",
            key=f"busqueda_diccionario_{reset_id}",
        )

    df_filtrado = df_diccionario.copy()

    if tabla_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Tabla"] == tabla_seleccionada]

    if tipo_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_seleccionado]

    if busqueda.strip():
        termino = busqueda.strip().lower()
        cols_texto = [
            "Tabla",
            "Campo",
            "Tipo",
            "Permite NULL",
            "Clave / Relación",
            "Ejemplo",
            "Descripción",
            "Valores / Reglas",
        ]
        mascara = pd.Series(False, index=df_filtrado.index)
        for col in cols_texto:
            mascara = mascara | df_filtrado[col].str.lower().str.contains(
                termino, na=False
            )
        df_filtrado = df_filtrado[mascara]

    st.caption(
        f"Mostrando **{len(df_filtrado)}** de **{len(df_diccionario)}** campos."
    )

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tabla": st.column_config.TextColumn("Tabla / Vista", width="medium"),
            "Campo": st.column_config.TextColumn("Campo", width="medium"),
            "Tipo": st.column_config.TextColumn("Tipo", width="small"),
            "Permite NULL": st.column_config.TextColumn("NULL", width="small"),
            "Clave / Relación": st.column_config.TextColumn(
                "Clave / Relación", width="large"
            ),
            "Ejemplo": st.column_config.TextColumn("Ejemplo", width="small"),
            "Descripción": st.column_config.TextColumn(
                "Descripción", width="large"
            ),
            "Valores / Reglas": st.column_config.TextColumn(
                "Valores / Reglas", width="large"
            ),
        },
    )

    if not df_filtrado.empty:
        st.download_button(
            label="⬇️ Descargar diccionario filtrado (CSV)",
            data=df_filtrado.to_csv(index=False, encoding="utf-8-sig").encode(
                "utf-8-sig"
            ),
            file_name="diccionario_datos_modelo_dimensional.csv",
            mime="text/csv",
            key="descargar_diccionario_csv",
        )
    else:
        st.info("No hay campos que coincidan con los filtros seleccionados.")

with tab_relaciones:
    st.caption(
        "Relaciones entre Fact_Respuesta_Encuestado y las tablas dimensionales del modelo."
    )
    st.dataframe(
        df_relaciones,
        use_container_width=True,
        hide_index=True,
    )
    with st.expander("**💫 ESQUEMA ESTRELLA**"):
      st.image("assets/Modelo Dimensional.jpg")

with tab_vistas:
    st.caption(
        "Resumen de vistas disponibles en modelo_dimensional.main y sus métricas principales."
    )
    st.dataframe(
        df_vistas,
        use_container_width=True,
        hide_index=True,
    )

