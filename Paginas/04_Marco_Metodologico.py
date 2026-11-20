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
   