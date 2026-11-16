import streamlit as st
import duckdb
# Aquí va página de pregunta profesores 

# Conexion y Tokens
md_token = st.secrets["MOTHERDUCK_TOKEN"]
conn = duckdb.connect(f"md:?motherduck_token={md_token}")

# Diccionario con Consultas
consultas_sugeridas = {
    "Pregunta 1": {
        "mostrar": """SELECT ... """,
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Uno"
    },
    "Pregunta 2": {
        "mostrar": """SELECT ...""",
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Dos"
    },
    "Pregunta 3": {
        "mostrar": """SELECT ...""",
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Tres"
    },
    "Pregunta 4": {
        "mostrar": """SELECT ...""",
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Cuatro"
    },
    "Pregunta 5": {
        "mostrar": """SELECT ...""",
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Cinco"
    },
    "Pregunta 6": {
        "mostrar": """SELECT ...""",
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Seis"
    }
}

if "texto_mostrar" not in st.session_state:
    st.session_state["texto_mostrar"] = ""
    st.session_state["comando_ejecutar"] = ""
if "hubo_error" not in st.session_state:
    st.session_state["error"] = False

st.subheader("💡 Ejecutar Consultas")

# Control de errores
if st.session_state["error"]:
    st.warning("⚠️ La consulta presentó un error. La terminal se ha vaciado para que vuelvas a intentarlo.")
    st.session_state["error"] = False

cols = st.columns(len(consultas_sugeridas))
for i, (nombre_boton, datos_consulta) in enumerate(consultas_sugeridas.items()):
    with cols[i]:
        if st.button(nombre_boton, use_container_width=True):
            st.session_state["texto_mostrar"] = datos_consulta["mostrar"]
            st.session_state["comando_ejecutar"] = datos_consulta["ejecutar"]

st.markdown("**SQL Terminal:**")
consulta_editada = st.text_area(
    "Terminal", 
    value=st.session_state["texto_mostrar"], 
    height=300, 
    label_visibility="collapsed"
)

# Ejecutar Consulta
if st.button("🚀 Ejecutar Query"):
    if consulta_editada.strip():
        try:
            if consulta_editada == st.session_state["texto_mostrar"]:
                query_final = st.session_state["comando_ejecutar"]
            else:
                query_final = consulta_editada

            df_resultado = conn.execute(query_final).fetchdf()
            
            st.success("Consulta ejecutada correctamente.")
            st.dataframe(df_resultado, use_container_width=True)
       
        except Exception as e:
            st.session_state["texto_mostrar"] = ""
            st.session_state["comando_ejecutar"] = ""
            st.session_state["error"] = True
            st.rerun()
    else:
        st.warning("El terminal está vacío.")