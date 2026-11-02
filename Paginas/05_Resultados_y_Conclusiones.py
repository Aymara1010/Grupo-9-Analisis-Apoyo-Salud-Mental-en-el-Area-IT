import streamlit as st
import pandas as pd
import time as t
# Aquí va página de los resultados (Analisis y Conclusiones)

# función para los querys
@st.cache_data(ttl="1h")
def run_query(query):
    conn = st.connection("motherduck", type="sql")
    return conn.query(query)

st.header("Objetivo 1")
df = run_query(" SELECT * FROM Objetivo_Uno")
st.table(df)

st.header("Objetivo 2")
df2 = run_query(" SELECT * FROM Objetivo_Dos")
st.table(df2)

st.header("Objetivo 3")
df3 = run_query(" SELECT * FROM Objetivo_Tres")
st.table(df3)

st.header("Objetivo 4")
df4 = run_query(" SELECT * FROM Objetivo_Cuatro")
st.table(df4)

st.header("Objetivo 5")
df5 = run_query(" SELECT * FROM Objetivo_Cinco")
st.table(df5)

st.header("Objetivo 6")
df6 = run_query(" SELECT * FROM Objetivo_Seis")
st.table(df6)

st.markdown("⚠️🔨 En Construcción...")