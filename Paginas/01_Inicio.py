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

st.markdown("---")
