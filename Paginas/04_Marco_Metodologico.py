import pandas as pd
import streamlit as st

# Diccionario de datos base del modelo dimensional
DICCIONARIO_DATOS = [
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "SaludMentalID",
        "Tipo": "INTEGER",
        "Clave / Relación": "FK → Dim_Estado_Mental.SaludMentalID",
        "Descripción": (
            "Identificador de la dimensión asociada al estado mental y búsqueda"
            " de tratamiento."
        ),
        "Valores / Reglas": "Entero vinculado a Dim_Estado_Mental.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "BeneficiosID",
        "Tipo": "INTEGER",
        "Clave / Relación": "FK → Dim_Beneficio_Trabajo.BeneficiosID",
        "Descripción": (
            "Identificador de la dimensión de beneficios laborales de salud"
            " mental."
        ),
        "Valores / Reglas": "Entero vinculado a Dim_Beneficio_Trabajo.",
    },
    {
        "Tabla": "Fact_Respuesta_Encuestado",
        "Campo": "Pais_Empleo",
        "Tipo": "INTEGER",
        "Clave / Relación": "FK → Dim_Pais.PaisID",
        "Descripción": "País donde desempeña su empleo la persona encuestada.",
        "Valores / Reglas": "Se cruza con Dim_Pais para agrupar por región.",
    },
    {
        "Tabla": "Dim_Estado_Mental",
        "Campo": "Tratamiento",
        "Tipo": "VARCHAR",
        "Clave / Relación": "Atributo descriptivo",
        "Descripción": (
            "Indica si la persona encuestada ha buscado tratamiento por"
            " afecciones de salud mental."
        ),
        "Valores / Reglas": (
            "Normalizado con LOWER(TRIM(...)) ('yes', 'sí', 'si', 's', etc.)."
        ),
    },
    {
        "Tabla": "Dim_Beneficio_Trabajo",
        "Campo": "Beneficio",
        "Tipo": "VARCHAR",
        "Clave / Relación": "Atributo descriptivo",
        "Descripción": (
            "Indica si el empleador provee beneficios de salud mental como"
            " parte del paquete laboral."
        ),
        "Valores / Reglas": (
            "Evaluado en métricas de cobertura / ausencia de beneficios."
        ),
    },
    {
        "Tabla": "Dim_Pais",
        "Campo": "Region",
        "Tipo": "VARCHAR",
        "Clave / Relación": "Atributo descriptivo",
        "Descripción": (
            "Macroregión geográfica asignada al país del encuestado."
        ),
        "Valores / Reglas": "Ej. Estados Unidos, Europa y Oceanía.",
    },
]

df_diccionario = pd.DataFrame(DICCIONARIO_DATOS)

st.subheader("📚 Diccionario de Datos — Esquema Dimensional")
st.caption(
    "Consulta la estructura, relaciones y reglas de negocio de las tablas"
    " utilizadas en el análisis."
)

col_f1, col_f2 = st.columns([1, 2])

with col_f1:
    tablas_disponibles = ["Todas"] + sorted(
        df_diccionario["Tabla"].unique().tolist()
    )
    tabla_seleccionada = st.selectbox(
        "Filtrar por tabla:", tablas_disponibles, key="filtro_tabla_diccionario"
    )

with col_f2:
    busqueda = st.text_input(
        "Buscar campo o descripción:",
        placeholder="Ej. Tratamiento, Region, FK...",
        key="busqueda_diccionario",
    )

df_filtrado = df_diccionario.copy()

if tabla_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Tabla"] == tabla_seleccionada]

if busqueda.strip():
    termino = busqueda.strip().lower()
    mascara = (
        df_filtrado["Campo"].str.lower().str.contains(termino, na=False)
        | df_filtrado["Descripción"].str.lower().str.contains(termino, na=False)
        | df_filtrado["Valores / Reglas"]
        .str.lower()
        .str.contains(termino, na=False)
        | df_filtrado["Clave / Relación"]
        .str.lower()
        .str.contains(termino, na=False)
    )
    df_filtrado = df_filtrado[mascara]

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True,
)