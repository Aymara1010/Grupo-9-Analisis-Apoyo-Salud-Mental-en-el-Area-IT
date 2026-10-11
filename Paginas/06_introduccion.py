import streamlit as st
# Aquí va página de inicio (Introducción al proyecto)
st.markdown(
    """
    <div style='padding: 10px 0;'>
        <h1 style='color: ##1B4332; font-size: 2.2rem; font-weight: 700; line-height: 1.2; margin-bottom: 8px;'>
            Análisis Comparativo en Salud Mental IT
        </h1>
        <p style='color: #07393C; font-size: 1.1rem; font-weight: 400; margin-top: 0;'>
            Provisión de Apoyo y Prestaciones en el Ámbito Tecnológico entre Estados Unidos, Europa y Oceanía.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Introducción")
with st.container(border=True):
    st.markdown("Este trabajo consiste en un proyecto de análisis de datos aplicado busca realizar un análisis comparativo y estadístico sobre el acceso a beneficios de salud mental, políticas de bienestar y percepción del apoyo organizacional en el sector tecnológico, contrastando los panoramas de Estados Unidos, Europa y Oceanía pre pandemia. Con el objetivo de identificar brechas críticas en la cobertura médica y evaluar las diferencias en la cultura corporativa entre regiones.")
st.write("")
st.subheader("El proyecto combina dos componentes principales:")
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("#### Ingeniería de datos")
        st.caption("Uso de Python y SQL para la limpieza, depuración y estructuración de una base de datos cruda.")
with col2:
    with st.container(border=True):
        st.markdown("#### Análisis estadístico comparativo")
        st.caption("Aplicación de estadística descriptiva y comparativa para evaluar diferencias regionales y responder a las preguntas de investigación planteadas.")
st.write("")
st.subheader("Técnicas a utilizar:")
with st.container(border=True):
    st.markdown("""
- Cálculo de frecuencias absolutas y relativas para categorizar la oferta de beneficios por región.
- Elaboración de gráficos de barras apiladas para comparar el nivel de conocimiento de cobertura entre EE. UU., Europa y Oceanía.
- Análisis de proporciones para evaluar la percepción de la seriedad en el tratamiento de la salud mental.
- Tabulación de datos para resumir la frecuencia de campañas de bienestar organizacional según el país.
    """)