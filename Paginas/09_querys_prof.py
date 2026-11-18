import streamlit as st
import duckdb
# Aquí va página de pregunta profesores 

# Conexion y Tokens
md_token = st.secrets["MOTHERDUCK_TOKEN"]
conn = duckdb.connect(f"md:?motherduck_token={md_token}")

# Diccionario con Consultas
consultas_sugeridas = {
    "Pregunta 1": {
        "mostrar": """WITH proporciones AS (
     SELECT a.QuestionID AS Pregunta, a.SurveyID AS Edicion, 
      ROUND(100.0 * SUM(CASE WHEN a.AnswerText = '-1' THEN 1 ELSE 0 END) / COUNT(a.AnswerText) ,2) AS Pct_Centinelas,
      ROUND(100.0 * SUM(CASE WHEN a.AnswerText = '-1' THEN 0 ELSE 1 END) / COUNT(a.AnswerText) ,2) AS Pct_Respuestas,
       CASE 
	       WHEN ROUND(100.0 * SUM(CASE WHEN a.AnswerText = '-1' THEN 1 ELSE 0 END) / COUNT(a.AnswerText) ,2) < 10 THEN 'Menor que 10%'
           WHEN ROUND(100.0 * SUM(CASE WHEN a.AnswerText = '-1' THEN 1 ELSE 0 END) / COUNT(a.AnswerText) ,2) BETWEEN 10 AND 50 THEN 'Entre 10% y 50%'
       ELSE 'Mayor que 50%' END AS Clasificacion
     FROM Answer a
     GROUP BY a.QuestionID, a.SurveyID),
    Anteriores As (
     SELECT Pregunta,
       LAG(Edicion) OVER(PARTITION BY Pregunta ORDER BY Edicion) AS Edicion_Anterior,
       Edicion,
       LAG(Pct_Centinelas) OVER(PARTITION BY Pregunta ORDER BY Edicion) AS Pct_Centinela_Anterior,
       Pct_Centinelas,
       LAG(Pct_Respuestas) OVER(PARTITION BY Pregunta ORDER BY Edicion) AS Pct_Respuestas_Anterior,
       Pct_Respuestas,
       LAG(Clasificacion) OVER(PARTITION BY Pregunta ORDER BY Edicion) AS Clasificacion_Anterior,
       Clasificacion
     FROM proporciones)
SELECT Pregunta, Edicion, Edicion_Anterior, Pct_Centinelas, Pct_Centinela_Anterior,
       Pct_Centinelas - Pct_Centinela_Anterior AS Diferencia_Pct_Centinela,
       Pct_Respuestas, Pct_Respuestas_Anterior, Clasificacion, Clasificacion_Anterior
FROM Anteriores
WHERE (Pct_Centinelas - Pct_Centinela_Anterior) > 15""",
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
        "mostrar": """WITH preguntas AS (
    SELECT
        (SELECT questionid FROM Question WHERE questiontext = 'Have you ever sought treatment for a mental health disorder from a mental health professional?') AS q_tratamiento,
        (SELECT questionid FROM Question WHERE questiontext = 'Does your employer provide mental health benefits as part of healthcare coverage?') AS q_beneficio,
        (SELECT questionid FROM Question WHERE questiontext = 'Do you know the options for mental health care available under your employer-provided health coverage?') AS q_conocimiento
),
base AS (
    SELECT
        a.UserID,
        a.SurveyID,
        MAX(CASE WHEN a.QuestionID = p.q_tratamiento THEN a.AnswerText END) AS busco_tratamiento,
        MAX(CASE WHEN a.QuestionID = p.q_beneficio THEN a.AnswerText END) AS beneficio,
        MAX(CASE WHEN a.QuestionID = p.q_conocimiento THEN a.AnswerText END) AS conocimiento
    FROM Answer a
    JOIN preguntas p ON 1 = 1
    WHERE a.QuestionID IN (p.q_tratamiento, p.q_beneficio, p.q_conocimiento)
    GROUP BY a.UserID, a.SurveyID
),
base_limpia AS (
    SELECT
        SurveyID,
        CASE WHEN busco_tratamiento = '1' THEN 1 ELSE 0 END AS busco_tratamiento,
        CASE WHEN beneficio IN ('Don''t know', 'I don''t know') THEN 'No sé' ELSE beneficio END AS beneficio,
        CASE WHEN conocimiento = 'I am not sure' THEN 'No sé' ELSE conocimiento END AS conocimiento
    FROM base
    WHERE beneficio IS NOT NULL AND beneficio <> '-1'
      AND conocimiento IS NOT NULL AND conocimiento <> '-1'
),
edicion AS (
    SELECT SurveyID,
           AVG(busco_tratamiento) AS proporcion_tratamiento_edicion
    FROM base_limpia
    GROUP BY SurveyID
),
grupos AS (
    SELECT
        b.SurveyID,
        b.beneficio || ' / ' || b.conocimiento AS grupo,
        COUNT(*) AS tamano_grupo,
        AVG(b.busco_tratamiento) AS proporcion_tratamiento_grupo
    FROM base_limpia b
    GROUP BY b.SurveyID, b.beneficio, b.conocimiento
    HAVING COUNT(*) >= 30
)
SELECT
    g.SurveyID AS edicion,
    g.grupo,
    g.tamano_grupo AS tamano_grupo,
    ROUND(g.tamano_grupo * 1.0 / SUM(g.tamano_grupo) OVER (PARTITION BY g.SurveyID), 4) AS participacion_sobre_total,
    ROUND(g.proporcion_tratamiento_grupo, 4) AS proporcion_tratamiento_grupo,
    ROUND(e.proporcion_tratamiento_edicion, 4) AS proporcion_tratamiento_edicion,
    ROUND(g.proporcion_tratamiento_grupo / e.proporcion_tratamiento_edicion, 4) AS razon_vs_edicion,
    CASE WHEN RANK() OVER (PARTITION BY g.SurveyID ORDER BY g.proporcion_tratamiento_grupo DESC) = 1
         THEN 'Mayor propensión' END AS marca_mayor,
    CASE WHEN RANK() OVER (PARTITION BY g.SurveyID ORDER BY g.proporcion_tratamiento_grupo ASC) = 1
         THEN 'Menor propensión' END AS marca_menor
FROM grupos g
JOIN edicion e ON e.SurveyID = g.SurveyID
ORDER BY g.SurveyID, g.proporcion_tratamiento_grupo DESC;""",
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
    st.session_state["texto_mostrar"] = "-- Selecciona una pregunta"
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
            st.session_state["texto_mostrar"] = "-- Selecciona una pregunta"
            st.session_state["comando_ejecutar"] = ""
            st.session_state["error"] = True
            st.rerun()
    else:
        st.warning("El terminal está vacío.")