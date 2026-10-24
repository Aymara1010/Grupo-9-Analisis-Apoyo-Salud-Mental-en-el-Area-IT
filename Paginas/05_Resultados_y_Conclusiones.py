import streamlit as st
# Aquí va página de los resultados (Analisis y Conclusiones)

# función para los querys
def run_query(query, ttl="1h"):
    conn = st.connection("motherduck", type="sql")
    return conn.query(query, ttl=ttl)

st.markdown("⚠️🔨 En Construcción...")