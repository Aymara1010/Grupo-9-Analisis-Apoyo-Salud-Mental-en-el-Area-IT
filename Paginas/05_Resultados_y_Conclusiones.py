import streamlit as st
import duckdb
# Aquí va página de los resultados (Analisis y Conclusiones)

# función para los querys
md_token = st.secrets["MOTHERDUCK_TOKEN"]
conn = duckdb.connect(f"md:?motherduck_token={md_token}")

st.header("Objetivo 1")
df = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Uno").fetchdf()
st.table(df)

st.header("Objetivo 2")
df2 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Dos").fetchdf()
st.table(df2)

st.header("Objetivo 3")
df3 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Tres").fetchdf()
st.table(df3)

st.header("Objetivo 4")
df4 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cuatro").fetchdf()
st.table(df4)

st.header("Objetivo 5")
df5 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cinco").fetchdf()
st.table(df5)

st.header("Objetivo 6")
df6 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Seis").fetchdf()
st.table(df6)