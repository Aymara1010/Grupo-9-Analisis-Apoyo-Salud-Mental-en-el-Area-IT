import streamlit as st
import os

st.markdown("""
<style>
    .tarjeta-inicio {
        background-color: rgba(239, 206, 250, 0.8); /* Fondo lila claro elegante */
        border-left: 6px solid #7B2CBF; /* Borde izquierdo tono morado */
        border-top: 1px solid rgba(224, 170, 255, 0.4);
        border-right: 1px solid rgba(224, 170, 255, 0.4);
        border-bottom: 1px solid rgba(224, 170, 255, 0.4);
        padding: 30px 35px;
        border-radius: 14px;
        margin-bottom: 30px;
        box-shadow: 0px 6px 20px rgba(16, 0, 43, 0.15);
        transition: all 0.3s ease-in-out; /* Transición fluida para el efecto 3D */
    }
    
    /* Efecto 3D cuando pasas el mouse */
    .tarjeta-inicio:hover {
        transform: translateY(-8px) scale(1.01); /* Se eleva y crece ligeramente */
        box-shadow: 0px 12px 30px rgba(123, 44, 191, 0.25); /* Sombra difuminada morada */
        border-left-color: #BE0AFF; /* Destello de acento al hacer hover */
        background-color: rgba(239, 206, 250, 0.95);
    }

    .titulo-principal {
        color: #10002B !important; /* Forzamos un color oscuro impecable */
        font-size: 2.4em;
        font-weight: 800;
        margin: 0 0 10px 0;
        font-family: sans-serif;
    }
    .subtitulo {
        color: #3C096C;
        font-size: 1.2em;
        font-weight: 600;
        margin: 0;
    }
    .fuente {
        color: #5A189A;
        font-size: 0.9em;
        font-weight: 500;
        margin: 15px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# Renderizado de la tarjeta HTML
st.markdown("""
<div class="tarjeta-inicio">
    <h1 class="titulo-principal">🧠 TechWell: Bienestar Digital</h1>
    <p class="subtitulo">Políticas de bienestar en la industria IT · Análisis exploratorio comparativo</p>
    <p class="fuente">Fuente: Open Sourcing Mental Illness (OSMI) – 2017-2019</p>
</div>
""", unsafe_allow_html=True)

# Banner de imagen inferior y pie de foto
ruta_imagen = "sin imagen"

if os.path.exists(ruta_imagen):
    st.image(ruta_imagen, use_container_width=True)
else:
    st.info(" esperando imagen ... ⏳ (Aún no hay imagen en la carpeta)")

st.markdown("---")
st.markdown("⚠️🔨 En Construcción... 🚧")