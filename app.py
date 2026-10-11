import streamlit as st
# Configuración de la App
st.set_page_config(page_title="Análisis Salud Mental", page_icon="🧠", layout="wide")

#Detalles del menú y degradado de fondos
st.markdown('' 
    """
    <style>
    /* Degradado de fondo */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #EFBDEB 30%, #B68CB8 40%, #6461A0 60%) !important;
    }
    /* Borde lateral  */
    [data-testid="stSidebar"] {
        border-right: 3px solid #6461A0;
    }  
    /* Estilo para los botones del menú */
    a[data-testid="stPageLink-NavLink"] {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        transition: background-color 0.3s ease;
    }
    /* Estilo cuando el mouse pasa por encima o la página está activa */
    a[data-testid="stPageLink-NavLink"]:hover, 
    a[data-testid="stPageLink-NavLink"][aria-current="page"] {
        background-color: rgba(226, 183, 20, 0.15) !important;
        border: 1px solid #E88EED !important;
        color: #E88EED !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#Definición de las paginas
p_welcom = st.Page("Paginas/08_Welcome.py", title="Bienvenida")
p_vista = st.Page("Paginas/01_Inicio.py", title="Vista General")
p_intro = st.Page("paginas/06_introduccion.py", title="Introducción")
p_equipo = st.Page("paginas/07_Equipo_investigacion.py", title="Equipo de Investigación")

p_plant = st.Page("Paginas/02_Planteamiento.py", title="Lectura General ")
p_teorico = st.Page("Paginas/03_Marco_Teorico.py", title="Metodología")
p_metodo = st.Page("Paginas/04_Marco_Metodologico.py", title="Diccionario de Datos")

p_resultados = st.Page("Paginas/05_Resultados_y_Conclusiones.py", title="Resultados y Conclusiones")
p_querys_prof = st.Page("Paginas/09_querys_prof.py", title="Querys Generales")
p_consultas = st.Page("Paginas/11_sql_interactivo.py", title="Consultas Aquí")
p_bibli = st.Page("Paginas/10_Bibliografia.py", title="Bibliografía")

todas_las_paginas = [p_welcom, p_vista, p_intro, p_equipo, p_plant, p_teorico, p_metodo, p_resultados, p_querys_prof, p_consultas, p_bibli]
pg = st.navigation(todas_las_paginas, position="hidden")