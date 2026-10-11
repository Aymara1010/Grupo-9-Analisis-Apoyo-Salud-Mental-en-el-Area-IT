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