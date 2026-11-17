import os
import streamlit as st

# cambiar a false para quitar el agradecimiento a los profes
MOSTRAR_PROFESORES = True  # Cambiar a false para no mostrar más

#tarjetas
st.markdown(
    """
    <style>
    /* Tarjeta de bienvenida principal (Morado oscuro original) */
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
    
    /* Etiquetas de profesores y equipo */
    .custom-card {
        background: linear-gradient(135deg, #d8b4fe, #c084fc);
        border: 2px solid #7B2CBF;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(123, 44, 191, 0.25);
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }
    
    .custom-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0px 10px 25px rgba(123, 44, 191, 0.4);
        border-color: #10002B;
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
""",
    unsafe_allow_html=True,
)
st.markdown("---")

# agradecimiento prof
if MOSTRAR_PROFESORES:
  st.markdown(
      "<h3 style='text-align: center; color: #7B2CBF;'>🎓 Agradecimiento"
      " Académico</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #14213D; max-width: 700px; margin:"
      " 0 auto 20px auto;'>Este proyecto es el resultado de la constancia,"
      " investigación y rigor estadístico. Queremos expresar nuestro más"
      " profundo agradecimiento a nuestros profesores por su constante guía y"
      " apoyo en la Escuela de Estadística de la UCV."
      " Que nunca sientan que toda su dedicación fue en vano. Gracias.</p>",
      unsafe_allow_html=True,
  )

  col_p1, col_p2 = st.columns(2)

  with col_p1:
    ruta_profe_1 = "assets/profe_olover.jpg"
    if os.path.exists(ruta_profe_1):
      st.image(ruta_profe_1, use_container_width=True)
    else:
      st.info("⏳ Esperando foto del Prof. 1... 🚧")

    st.markdown(
        """
            <div class="custom-card">
                <h4 style="color: #10002B; margin-bottom: 5px; font-weight: bold;">Prof. Oliver Triveño </h4>
                <p style="color: #3C096C; font-size: 0.9rem; margin: 0; font-weight: 500;">Gracias por tanta paciencia, por ser nuestro santo salvador </p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col_p2:
    ruta_profe_2 = "assets/profe_jesus.jpg"
    if os.path.exists(ruta_profe_2):
      st.image(ruta_profe_2, use_content_width=True)
    else:
      st.info("⏳ Esperando foto del Prof. 2... 🚧")

    st.markdown(
        """
            <div class="custom-card">
                <h4 style="color: #10002B; margin-bottom: 5px; font-weight: bold;">Prof. Jesús Ochoa </h4>
                <p style="color: #3C096C; font-size: 0.9rem; margin: 0; font-weight: 500;">Gracias por querer y hacer todo lo posible por que seamos los mejores profesionales desde siempre </p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")