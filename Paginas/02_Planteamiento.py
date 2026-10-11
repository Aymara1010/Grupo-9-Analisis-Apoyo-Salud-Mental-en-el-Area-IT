import streamlit as st
from PIL import Image

# Aquí va página del planteamiento (Objetivos y variables)
@st.cache_data #carga de imagen
def cache_imagenes(path):
    """
    Lee la imagen del disco una sola vez y la guarda en cache
    """
    return Image.open(path)
#destacar palabras clave en el texto
st.markdown("""
    <style>
    .destaque {
        color: #3C096C; /* Morado */"
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.image("assets/planteamiento_banner.jpg", use_container_width=True)
