import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

#1. estilo general pag
st.markdown("""
<style>
.tarjeta-objetivo, .tarjeta-kpi {
    border-radius: 10px;
    padding: 15px 20px;
    font-family: sans-serif;
    color: black;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08);
}
.tarjeta-objetivo {
    background-color: #F8F4FF;
    border-left: 8px solid #3C096C;
}
.tarjeta-kpi {
    background-color: #F8F4FF; 
    border-left: 6px solid #7B2CBF; 
}
.titulo-obj {
    font-size: 20px;
    font-weight: bold;
    margin: 0;
    color: #3C096C;
}
.texto-obj, .texto-kpi {
    font-size: 15px;
    margin: 6px 0 0 0;
    line-height: 1.4;
}
.titulo-kpi {
    font-size: 13px;
    font-weight: bold;
    color: #3C096C;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# 2 conexion motherduck
md_token = st.secrets["MOTHERDUCK_TOKEN"]
conn = duckdb.connect(f"md:?motherduck_token={md_token}")