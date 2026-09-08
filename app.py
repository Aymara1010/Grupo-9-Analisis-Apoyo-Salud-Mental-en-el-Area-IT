import streamlit as st
# Configuración de la App
st.set_page_config(page_title="Análisis Salud Mental", page_icon="🧠", layout="wide")

# Configuración de las Páginas del proyecto
pages = [
    st.Page("Paginas/01_Inicio.py", title="Inicio"),
    st.Page("Paginas/02_Planteamiento.py", title="Planteamiento de Problema"),
    st.Page("Paginas/03_Marco_Teorico.py", title="Marco Teórico"),
    st.Page("Paginas/04_Marco_Metodologico.py", title="Marco Metodologico"),
    st.Page("Paginas/05_Resultados_y_Conclusiones.py", title="Resultados y Conclusiones")
    ]

page = st.navigation(pages)
page.run()