import streamlit as st
import os

# ESTILOS Y TARJETA DE BIENVENIDA CON EFECTO 3D
st.markdown("""
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
    
    /* EFECTO 3D CUANDO PASAS EL MOUSE */
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

    /* Forzamos el color blanco para evitar que Streamlit lo cambie a negro */
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
        <span class="welcome-badge">Dashboard Estadístico e Interactivo</span>
        <h2 class="welcome-title">Bienvenida al Análisis de Salud Mental en el Sector IT</h2>
        <p class="welcome-text">
            Explora las dinámicas, brechas y contrastes de los beneficios de bienestar laboral en la industria tecnológica entre 
            <strong>Estados Unidos, Europa y Oceanía (2017 - 2019)</strong>. Una herramienta diseñada para transformar datos complejos 
            en evidencia clara y accesible.
        </p>
    </div>
""", unsafe_allow_html=True)

#video
ruta_video = "SIN VIDEO AUN"  

if os.path.exists(ruta_video):
    # Si el archivo existe
    col_v1, col_v2, col_v3 = st.columns([1, 8, 1])
    with col_v2:
        st.video(ruta_video)
else:
    # Si no existe
    st.info("⏳ Esperando video de introducción... (El archivo aún no se ha agregado a la carpeta)")

st.markdown("---")
st.markdown("⚠️🔨 En Construcción... 🚧")