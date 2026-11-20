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