import streamlit as st
import duckdb
# Aquí va página de los resultados (Analisis y Conclusiones)

# función para los querys
md_token = st.secrets["MOTHERDUCK_TOKEN"]
conn = duckdb.connect(f"md:?motherduck_token={md_token}")

st.header("Objetivo 1")
st.markdown("Comparar la frecuencia relativa de empresas tecnológicas que ofrecen beneficios de salud mental entre Estados Unidos, Europa y Oceanía.")
df = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Uno").fetchdf()
st.table(df)

st.header("Objetivo 2")
st.markdown("Determinar la proporción de empleados que conocen sus opciones de atención de salud mental laboral según su región geográfica.")
df2 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Dos").fetchdf()
st.table(df2)

st.header("Objetivo 3")
st.markdown("Calcular y comparar el puntaje promedio y la dispersión de la importancia que los empleadores otorgan a la salud mental por categoría de puesto.")
df3 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Tres").fetchdf()
st.table(df3)

st.header("Objetivo 4")
st.markdown("Analizar la distribución de frecuencias de la calificación que otorgan los empleados al apoyo general de la industria tecnológica en temas de salud mental según su ubicación.")
df4 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cuatro").fetchdf()
st.table(df4)

st.header("Objetivo 5")
st.markdown("Calcular y comparar el puntaje promedio de importancia que los empleadores otorgan a la salud mental.")
df5 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cinco").fetchdf()
st.table(df5)

st.header("Objetivo 6")
st.markdown("Identificar las necesidades actuales sobre el apoyo y los beneficios de salud mental en la industria tecnológica.")
df6 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Seis").fetchdf()
st.table(df6)