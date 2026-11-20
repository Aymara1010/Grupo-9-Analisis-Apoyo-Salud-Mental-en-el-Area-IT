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
   