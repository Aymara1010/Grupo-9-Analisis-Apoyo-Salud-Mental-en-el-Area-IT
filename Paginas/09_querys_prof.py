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
        "mostrar": """WITH por_encuestado AS (
    SELECT
        a.SurveyID,
        a.UserID,
        MAX(CASE WHEN a.QuestionID = 64 THEN CAST(TRIM(a.AnswerText) AS REAL) END) AS val_fisica,
        MAX(CASE WHEN a.QuestionID = 65 THEN CAST(TRIM(a.AnswerText) AS REAL) END) AS val_mental,
        MAX(CASE WHEN a.QuestionID = 8 THEN TRIM(a.AnswerText) END) AS tramo_empresa
    FROM Answer a
    WHERE a.QuestionID IN (64, 65, 8) AND TRIM(a.AnswerText) <> '-1'
    GROUP BY a.SurveyID, a.UserID
    HAVING val_fisica IS NOT NULL AND val_mental IS NOT NULL AND tramo_empresa IS NOT NULL
),
brechas_ordenadas AS (
    SELECT SurveyID, tramo_empresa, val_fisica, val_mental,
        (val_fisica - val_mental) AS brecha,
        ROW_NUMBER() OVER (PARTITION BY SurveyID, tramo_empresa ORDER BY (val_fisica - val_mental)) AS rn_tramo,
        COUNT(*) OVER (PARTITION BY SurveyID, tramo_empresa) AS cnt_tramo,
        ROW_NUMBER() OVER (PARTITION BY SurveyID ORDER BY (val_fisica - val_mental)) AS rn_edicion,
        COUNT(*) OVER (PARTITION BY SurveyID) AS cnt_edicion
    FROM por_encuestado
),
mediana_por_edicion AS (
    SELECT SurveyID, AVG(brecha) AS brecha_mediana_edicion
    FROM brechas_ordenadas
    WHERE rn_edicion BETWEEN cnt_edicion / 2.0 AND (cnt_edicion / 2.0) + 1
    GROUP BY SurveyID
),
metricas_por_tramo AS (
    SELECT b.SurveyID, b.tramo_empresa,
        CASE b.tramo_empresa
            WHEN '1-5' THEN 1
            WHEN '6-25' THEN 2
            WHEN '26-100' THEN 3
            WHEN '100-500' THEN 4
            WHEN '500-1000' THEN 5
            WHEN 'More than 1000' THEN 6
            ELSE 99
        END AS orden_tamano,
        COUNT(*) AS n_encuestados,
        AVG(CASE WHEN b.rn_tramo BETWEEN b.cnt_tramo / 2.0 AND (b.cnt_tramo / 2.0) + 1 THEN b.brecha END) AS brecha_mediana_tramo,
        1.0 * SUM(b.val_mental >= b.val_fisica) / COUNT(*) AS prop_mental_ge_fisica
    FROM brechas_ordenadas b
    GROUP BY b.SurveyID, b.tramo_empresa
)
SELECT
    s.Description AS "Edición",
    m.tramo_empresa AS "Tamaño de Empresa",
    m.n_encuestados AS "Cantidad de Encuestados",
    ROUND(m.brecha_mediana_tramo, 2) AS "Brecha Mediana (Física - Mental)",
    ROUND(m.prop_mental_ge_fisica, 4) AS "Proporción Salud Mental >= Física",
    RANK() OVER (PARTITION BY m.SurveyID ORDER BY m.brecha_mediana_tramo DESC) AS "Ranking de Brecha en la Edición",
    ROUND(e.brecha_mediana_edicion, 2) AS "Brecha Mediana de la Edición",
    ROUND(m.brecha_mediana_tramo - e.brecha_mediana_edicion, 2) AS "Diferencia vs. Mediana de la Edición"
FROM metricas_por_tramo m
INNER JOIN mediana_por_edicion e ON m.SurveyID = e.SurveyID
INNER JOIN Survey s ON m.SurveyID = s.SurveyID
ORDER BY m.SurveyID, m.orden_tamano;""",
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

consulta = st.session_state["texto_mostrar"]
comando = st.session_state["comando_ejecutar"]

st.markdown("**SQL Terminal:**")
st.code(consulta, height=400, language="sql") 

# Ejecutar Consulta
if st.button("🚀 Ejecutar Query", type="primary"):
    query_a_validar = (comando or consulta or "").strip()
    if query_a_validar and query_a_validar != "-- Selecciona una pregunta":
        try:
            query_final = comando.strip() if (comando and comando.strip()) else consulta.strip()

            df_resultado = conn.execute(query_final).fetchdf()

            st.success("Consulta ejecutada correctamente.")
            st.dataframe(df_resultado, hide_index=True, use_container_width=True)

        except Exception as e:
            st.session_state["texto_mostrar"] = "-- Selecciona una pregunta"
            st.session_state["comando_ejecutar"] = ""
            st.session_state["error"] = True
            st.rerun()
    else:
        st.warning("El terminal está vacío.")