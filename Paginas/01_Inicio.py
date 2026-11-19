import os
import plotly.express as px
import streamlit as st

# Título y tarjeta
st.markdown(
"""
<style>
.welcome-card {
    background: linear-gradient(135deg, #10002B, #3C096C);
    border: 2px solid #7B2CBF;
    border-left: 8px solid #E0AAFF;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease-in-out;
    margin: 20px auto;
    text-align: center;
}

.welcome-card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0px 12px 30px rgba(224, 170, 255, 0.35);
    border-left-color: #FFD60A;
    border-color: #E0AAFF;
}

.welcome-badge {
    color: #E0AAFF;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: bold;
    margin-bottom: 12px;
    display: block;
}

h2.welcome-title {
    color: #FFFFFF !important;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 15px;
}

.welcome-text {
    color: #E0AAFF;
    font-size: 16px;
    line-height: 1.6;
    margin: 0 auto;
    max-width: 800px;
}
</style>

<div class="welcome-card">
    <span class="welcome-badge">Resumen Ejecutivo</span>
    <h2 class="welcome-title">🧠 TechWell: Bienestar Digital</h2>
    <p class="welcome-text">
        Explora los indicadores clave y hallazgos obtenidos del análisis comparativo de salud mental 
        en el sector tecnológico (OSMI 2017-2019) entre Estados Unidos, Europa y Oceanía.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Enlace hacia el Power BI
st.markdown(
"""
<div style='
background-color: #FFFFFF;
padding: 12px 20px;
border-radius: 10px;
border-left: 6px solid #581C87;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
margin-bottom: 20px;
display: flex;
align-items: center;
justify-content: space-between;
'>
<span style='color: #000000; font-weight: 600; font-size: 1rem;'>📊 ¿Quieres explorar el reporte interactivo completo?</span>
<a href="https://app.powerbi.com/view?r=eyJrIjoiYmE3MjdjM2YtZjJhNC00MTM1LWE3YWQtN2ZhMjAxZGNhY2I0IiwidCI6IjRjODE4Zjc5LWFiODQtNDU1Mi05YjdjLTJmZTcxNWIwZDBkNSIsImMiOjR9" target="_blank" style='
background-color: #581C87;
color: #FFFFFF;
padding: 8px 16px;
border-radius: 6px;
text-decoration: none;
font-weight: 600;
font-size: 0.95rem;
'>Ver Dashboard en Power BI ↗</a>
</div>
""",
unsafe_allow_html=True
)

st.markdown("---")

# Creación de las pestañas
tab1, tab2 = st.tabs(["📖 Introducción, Componentes y Técnicas", "📈 Gráficos y Visualizaciones"])

with tab1:
    # Tarjeta de Introducción
    st.markdown(
        """
        <div style='
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 10px;
            border-left: 6px solid #581C87;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            margin-top: 10px;
            margin-bottom: 20px;
        '>
            <h3 style='color: #000000; font-weight: 700; margin-top: 0; margin-bottom: 10px;'>
                Introducción
            </h3>
            <p style='margin: 0; font-size: 1rem; line-height: 1.6; color: #000000;'>
                Este trabajo consiste en un proyecto de análisis de datos aplicado que busca realizar un análisis comparativo y estadístico sobre el acceso a beneficios de salud mental, políticas de bienestar y percepción del apoyo organizacional en el sector tecnológico, contrastando los panoramas de Estados Unidos, Europa y Oceanía pre pandemia. Con el objetivo de identificar brechas críticas en la cobertura médica y evaluar las diferencias en la cultura corporativa entre regiones.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div style='
                background-color: #FFFFFF;
                padding: 20px;
                border-radius: 10px;
                border-left: 6px solid #581C87;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
                height: 100%;
            '>
                <h4 style='color: #000000; margin-top: 0; margin-bottom: 10px; font-weight: 700;'>Ingeniería de datos</h4>
                <p style='margin: 0; color: #000000; font-size: 0.95rem; line-height: 1.5;'>
                    Uso de Python y SQL para la limpieza, depuración y estructuración de una base de datos cruda.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col2:
        st.markdown(
            """
            <div style='
                background-color: #FFFFFF;
                padding: 20px;
                border-radius: 10px;
                border-left: 6px solid #581C87;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
                height: 100%;
            '>
                <h4 style='color: #000000; margin-top: 0; margin-bottom: 10px; font-weight: 700;'>Análisis estadístico comparativo</h4>
                <p style='margin: 0; color: #000000; font-size: 0.95rem; line-height: 1.5;'>
                    Aplicación de estadística descriptiva y comparativa para evaluar diferencias regionales y responder a las preguntas de investigación planteadas.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
st.write("")
st.write("")   

# Tarjeta de Técnicas a utilizar
st.markdown(
        """
        <div style='
            background-color: #FFFFFF;
            padding: 22px;
            border-radius: 10px;
            border-left: 6px solid #581C87;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            margin-bottom: 20px;
        '>
            <h3 style='color: #000000; font-weight: 700; margin-top: 0; margin-bottom: 12px;'>
                Técnicas a utilizar:
            </h3>
            <ul style='color: #000000; font-size: 0.95rem; line-height: 1.6; margin: 0; padding-left: 20px;'>
                <li style='margin-bottom: 8px;'>Cálculo de frecuencias absolutas y relativas para categorizar la oferta de beneficios por región.</li>
                <li style='margin-bottom: 8px;'>Elaboración de gráficos de barras para comparar el nivel de conocimiento de cobertura entre EE. UU., Europa y Oceanía.</li>
                <li style='margin-bottom: 8px;'>Análisis de proporciones para evaluar la percepción de la seriedad en el tratamiento de la salud mental.</li>
                <li style='margin-bottom: 0;'>Tabulación de datos para resumir la frecuencia de campañas de bienestar organizacional según el país.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("💜 Gracias, por tú interés en este proyecto 💕")