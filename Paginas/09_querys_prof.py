import streamlit as st
import duckdb
# Aquí va página de pregunta profesores 

st.markdown(
    """
<style>
.resumen-3d-wrapper {
    perspective: 1100px;
    margin-bottom: 22px;
}

.resumen-3d-card {
    background: linear-gradient(145deg, #F8F4FF 0%, #EDE2FF 100%);
    border-left: 7px solid #3C096C;
    border-top: 1px solid rgba(123, 44, 191, 0.25);
    border-right: 1px solid rgba(123, 44, 191, 0.25);
    border-bottom: 5px solid #3C096C;
    border-radius: 16px;
    padding: 18px 22px;
    color: #1a1025;
    box-shadow:
        0 14px 26px rgba(60, 9, 108, 0.16),
        0 5px 0 #240046;
    transform-style: preserve-3d;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.etiqueta-resumen {
    display: inline-block;
    background: linear-gradient(135deg, #7B2CBF 0%, #3C096C 100%);
    color: #ffffff;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 10px;
    box-shadow: 0 3px 0 #240046;
}

.texto-resumen-interno {
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0;
    color: #1a1025;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("CONSULTAS SQL")
st.caption("Salud Mental en la Industria Tecnológica — OSMI Database | Formulario B")

with st.expander("🗄️ Esquema de la base de datos", expanded=False):
    st.markdown("""
    **Tablas disponibles:**
    * `Answer (AnswerText, SurveyID, UserID, QuestionID)`
    * `Question (questionid, questiontext)`
    * `Survey (SurveyID, Description)`

    Cada fila de `Answer` es la respuesta de un usuario a una pregunta dentro de una edición de la encuesta. Un mismo `UserID` pertenece a una sola edición. Las preguntas de opción múltiple generan varias filas para el mismo usuario y la misma pregunta.
    """)

st.divider()

st.markdown(
      """
        <div class="resumen-3d-wrapper">
            <div class="resumen-3d-card">
                <span class="etiqueta-resumen">🏷️ Mini Resumen</span>
                <p class="texto-resumen-interno">
                    Este marco reúne la base conceptual para entender la salud mental en tecnología a partir de OSMI: cómo el <i>burnout</i>, el tecnoestrés y la modalidad de trabajo inciden en el bienestar y la seguridad psicológica del equipo, y por qué la comparación regional depende en gran medida de si el acceso a salud está ligado al empleo (EE. UU.) o respaldado por sistemas públicos y protecciones laborales más amplias (Europa y Oceanía).
                </p>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )


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
        "mostrar": """WITH respuestas_codificadas AS (
    SELECT
        a.SurveyID,
        a.UserID,
        CASE
            WHEN a.QuestionID IN (10, 23) THEN 'Existencia de beneficios'
            WHEN a.QuestionID IN (14, 24) THEN 'Conocimiento de la cobertura'
            WHEN a.QuestionID IN (15, 25) THEN 'Comunicación formal'
            WHEN a.QuestionID IN (16, 26) THEN 'Disponibilidad de recursos'
            WHEN a.QuestionID IN (17, 27) THEN 'Protección del anonimato'
        END AS dimension,
        CASE WHEN a.QuestionID IN (10, 14, 15, 16, 17) THEN 'actual'
            ELSE 'anterior'
        END AS bloque,
        CASE
            WHEN LOWER(TRIM(a.AnswerText)) IN (
                'yes',
                'yes, they all did',
                'yes, i was aware of all of them',
                'yes, always',
                'very easy',
                'somewhat easy'
            ) THEN 2
            WHEN LOWER(TRIM(a.AnswerText)) IN (
                'some did',
                'i was aware of some',
                'sometimes',
                'neither easy nor difficult'
            ) THEN 1
            WHEN LOWER(TRIM(a.AnswerText)) IN (
                'no',
                'no, none did',
                'none did',
                'no, i only became aware later',
                'somewhat difficult',
                'difficult',
                'very difficult'
            ) THEN 0
        END AS puntaje
    FROM Answer a
    WHERE a.QuestionID IN (10, 23, 14, 24, 15, 25, 16, 26, 17, 27)
      AND TRIM(a.AnswerText) <> '-1'),
pares_por_usuario AS (
    SELECT
        SurveyID,
        UserID,
        dimension,
        MAX(CASE WHEN bloque = 'actual' THEN puntaje END) AS puntaje_actual,
        MAX(CASE WHEN bloque = 'anterior' THEN puntaje END) AS puntaje_anterior
    FROM respuestas_codificadas
    WHERE puntaje IS NOT NULL
    GROUP BY SurveyID, UserID, dimension
    HAVING puntaje_actual IS NOT NULL AND puntaje_anterior IS NOT NULL),
metricas_por_dimension AS (
    SELECT
        p.SurveyID,
        s.Description AS edicion,
        p.dimension,
        COUNT(*) AS n_encuestados,
        1.0 * SUM(p.puntaje_actual > p.puntaje_anterior) / COUNT(*) AS prop_mejoro,
        1.0 * SUM(p.puntaje_actual < p.puntaje_anterior) / COUNT(*) AS prop_empeoro,
        1.0 * SUM(p.puntaje_actual = p.puntaje_anterior) / COUNT(*) AS prop_mantuvo
    FROM pares_por_usuario p
    INNER JOIN Survey s
        ON p.SurveyID = s.SurveyID
    GROUP BY p.SurveyID, s.Description, p.dimension),
metricas_con_ranking AS (
    SELECT
        m.*,
        RANK() OVER (PARTITION BY m.SurveyID ORDER BY m.prop_mejoro DESC ) AS ranking_mejora,
        SUM(m.n_encuestados) OVER (
            PARTITION BY m.SurveyID
            ORDER BY m.prop_mejoro DESC, m.dimension ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ) AS acumulado_encuestados
    FROM metricas_por_dimension m )
SELECT
    edicion AS "Edición",
    dimension AS "Dimensión",
    n_encuestados AS "Encuestados Considerados",
    ROUND(prop_mejoro, 4) AS "Proporción que Mejoró",
    ROUND(prop_empeoro, 4) AS "Proporción que Empeoró",
    ROUND(prop_mantuvo, 4) AS "Proporción que se Mantuvo",
    ranking_mejora AS "Ranking por Mejora en la Edición",
    acumulado_encuestados AS "Total Acumulado de Encuestados"
FROM metricas_con_ranking
ORDER BY SurveyID, ranking_mejora, dimension;""",
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
        "mostrar": """WITH por_encuestado AS (
    SELECT
        a.SurveyID,
        a.UserID,
        CASE
            WHEN LOWER(a.AnswerText) LIKE 'mood disorder%'
              OR LOWER(a.AnswerText) IN ('depression', 'seasonal affective disorder') THEN 'Mood Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'anxiety disorder%'
              OR LOWER(a.AnswerText) = 'post-partum / anxiety' THEN 'Anxiety Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'attention deficit%'
              OR LOWER(a.AnswerText) LIKE 'add (%'
              OR LOWER(a.AnswerText) LIKE '%adhd%' THEN 'Attention Deficit Hyperactivity Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'post-traumatic%'
              OR LOWER(a.AnswerText) LIKE 'ptsd%' THEN 'Post-traumatic Stress Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'stress response%'
              OR LOWER(a.AnswerText) IN ('burn out', 'burnout') THEN 'Stress Response Syndromes'
            WHEN LOWER(a.AnswerText) LIKE 'personality disorder%'
              OR LOWER(a.AnswerText) = 'schizotypal personality disorder' THEN 'Personality Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'addictive disorder%'
              OR LOWER(a.AnswerText) = 'sexual addiction' THEN 'Addictive Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'dissociative disorder%'
              OR LOWER(a.AnswerText) LIKE 'depersonali%' THEN 'Dissociative Disorder'
            WHEN LOWER(a.AnswerText) LIKE 'eating disorder%' THEN 'Eating Disorder'
            ELSE TRIM(a.AnswerText)
        END AS condicion,
        MAX(a.QuestionID = 115) AS diag,
        MAX(a.QuestionID = 116) AS sosp
    FROM Answer a
    WHERE a.QuestionID IN (115, 116)
      AND TRIM(a.AnswerText) <> '-1'
    GROUP BY a.SurveyID, a.UserID, condicion),
resumen AS (
    SELECT
        p.SurveyID,
        s.Description AS edicion,
        p.condicion,
        SUM(p.diag) AS diagnosticados,
        SUM(p.sosp) AS solo_sospechados,
        COUNT(*) AS total,
        ROUND(1.0 * SUM(p.sosp) / COUNT(*), 3) AS proporcion_sospecha,
        RANK() OVER (
            PARTITION BY p.SurveyID
            ORDER BY 1.0 * SUM(p.sosp) / COUNT(*) DESC
        ) AS ranking
    FROM por_encuestado p
    JOIN Survey s ON p.SurveyID = s.SurveyID
    GROUP BY p.SurveyID, s.Description, p.condicion
    HAVING COUNT(*) >= 15)
SELECT
    edicion AS "Edición",
    condicion AS "Condición de Salud Mental",
    diagnosticados AS "Diagnosticados",
    solo_sospechados AS "Solo Sospechados",
    total AS "Total Encuestados",
    proporcion_sospecha AS "Proporción de Sospecha",
    ranking AS "Ranking por Proporción de Sospecha",
    CASE
        WHEN LAG(r.ranking) OVER (PARTITION BY r.condicion ORDER BY r.SurveyID) IS NULL THEN 'Sin edición anterior'
        WHEN ranking < LAG(r.ranking) OVER (PARTITION BY r.condicion ORDER BY r.SurveyID) THEN 'Subió'
        WHEN ranking > LAG(r.ranking) OVER (PARTITION BY r.condicion ORDER BY r.SurveyID) THEN 'Bajó'
        ELSE 'Mantuvo'
    END AS "Variación respecto a Edición Anterior"
FROM resumen r
ORDER BY SurveyID, ranking, condicion;""",
        "ejecutar": "SELECT * FROM modelo_dimensional.Pregunta_Cinco"
    },
    "Pregunta 6": {
        "mostrar": """WITH por_encuestado AS (
    SELECT
        a.SurveyID,
        a.UserID,
        MAX(CASE WHEN a.QuestionID IN (93, 118) THEN
                CASE
                    WHEN LOWER(TRIM(a.AnswerText)) IN ('always', 'yes') THEN 'Remoto'
                    WHEN LOWER(TRIM(a.AnswerText)) = 'sometimes' THEN 'Híbrido'
                    WHEN LOWER(TRIM(a.AnswerText)) IN ('never', 'no') THEN 'Presencial'
                END END) AS modalidad,
        MAX(CASE WHEN a.QuestionID IN (18, 99) THEN LOWER(TRIM(a.AnswerText)) = 'yes' END) AS fav_companeros,
        MAX(CASE WHEN a.QuestionID IN (19, 100) THEN LOWER(TRIM(a.AnswerText)) = 'yes' END) AS fav_supervisor
    FROM Answer a
    WHERE a.QuestionID IN (93, 118, 18, 99, 19, 100)
      AND TRIM(a.AnswerText) <> '-1'
    GROUP BY a.SurveyID, a.UserID
    HAVING modalidad IS NOT NULL AND fav_companeros IS NOT NULL AND fav_supervisor IS NOT NULL),
metricas AS (
    SELECT
        e.SurveyID,
        s.Description AS edicion,
        e.modalidad,
        COUNT(*) AS n_encuestados,
        1.0 * SUM(e.fav_companeros) / COUNT(*) AS prop_companeros,
        1.0 * SUM(e.fav_supervisor) / COUNT(*) AS prop_supervisor,
        (1.0 * SUM(e.fav_companeros) - SUM(e.fav_supervisor)) / COUNT(*) AS diferencia
    FROM por_encuestado e
    INNER JOIN Survey s
        ON e.SurveyID = s.SurveyID
    GROUP BY e.SurveyID, s.Description, e.modalidad
    HAVING COUNT(*) >= 25),
metricas_con_ventanas AS (
    SELECT
        m.*,
        RANK() OVER (ORDER BY m.diferencia DESC) AS ranking_diferencia,
        1.0 * SUM(m.n_encuestados) OVER (
            PARTITION BY m.SurveyID
            ORDER BY m.prop_supervisor ASC, m.modalidad ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / SUM(m.n_encuestados) OVER (PARTITION BY m.SurveyID) AS prop_acumulada_encuestados
    FROM metricas m)
SELECT
    sub.edicion AS "Edición",
    sub.modalidad AS "Modalidad de Trabajo",
    sub.n_encuestados AS "Cantidad de Encuestados",
    ROUND(sub.prop_companeros, 4) AS "Proporción Favorable Compañeros",
    ROUND(sub.prop_supervisor, 4) AS "Proporción Favorable Supervisor",
    ROUND(sub.diferencia, 4) AS "Diferencia (Compañeros - Supervisor)",
    sub.ranking_diferencia AS "Ranking por Diferencia",
    ROUND(sub.prop_acumulada_encuestados, 4) AS "Proporción Acumulada de Encuestados"
FROM metricas_con_ventanas sub
ORDER BY sub.SurveyID, sub.prop_supervisor ASC, sub.modalidad ASC;""",
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