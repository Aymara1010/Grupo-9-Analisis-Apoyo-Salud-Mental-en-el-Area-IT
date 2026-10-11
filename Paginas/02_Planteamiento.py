import streamlit as st
from PIL import Image

# Aquí va página del planteamiento (Objetivos y variables)
@st.cache_data #carga de imagen
def cache_imagenes(path):
    """
    Lee la imagen del disco una sola vez y la guarda en cache
    """
    return Image.open(path)
#destacar palabras clave en el texto
st.markdown("""
    <style>
    .destaque {
        color: #3C096C; /* Morado */"
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.image("assets/planteamiento_banner.jpg", use_container_width=True)

#tabs para organizar el contenido de la página
tab1, tab2, tab3, tab4 = st.tabs (["Planteamiento del problema 🌍","Objetivos 🎯 ", "Justificación de la Investigación 📚", "Variables Seleccionadas ✅"])

with tab1:
 
    st.subheader("Planteamiento del problema")
    with st.container(border=True):
        st.markdown("La industria tecnológica a nivel global, se ha caracterizado por ser un ambiente altamente competitivo, con ritmos de trabajo apresurados, plazos estrictos y una constante exigencia de innovación. Todas estas condiciones han proporcionado un aumento notable en los niveles de estrés, ansiedad y desgaste profesional. Aunque en los últimos años el bienestar emocional ha cobrado mayor importancia en la agenda profesional, la manera en la que las empresas abordan y proveen apoyo en la salud mental varía drásticamente dependiendo de la ubicación geográfica.")
        st.write("")
        st.markdown("En este sentido, surge un dilema particular al comparar a Estados Unidos con el resto del mundo. En Estados Unidos, el acceso a la salud mental está fuertemente relacionado con los beneficios dados por el empleador (seguros médicos privados, programas de asistencia), mientras que en otros países existen sistemas de salud pública universal o marcos regulatorios laborales. Esta diferencia estructural plantea interrogantes sobre la calidad, equidad y percepción de apoyo que realmente reciben los trabajadores tecnológicos.")
        st.write("")
        st.markdown("El problema central radica en la brecha de evidencia estadística sobre cómo estos distintos modelos estructurales impactan el acceso real a la atención. Por ello, resulta de gran interés analizar de forma cuantitativa y comparativa si el modelo de beneficios corporativos de EE. UU. proporciona una cobertura más efectiva para la salud mental o si, por el contrario, genera mayores barreras de acceso en comparación con los esquemas globales")    
    
    #pregunta de investigación
    st.markdown(""" 
    <style>
        .pregunta-container {
            background-color: #E0AAFF; /* Fondo Morado Claro */
        border-left: 10px solid #7B2CBF; /* Borde Izquierdo Oscuro */
        border: 2px solid #5A189A; /* Borde general para recortarla del fondo */
        padding: 30px;
        border-radius: 10px;
        margin: 40px 0px;
        box-shadow: 0px 8px 20px rgba(16, 0, 43, 0.4); /* Sombra oscura profunda */
        }
        .pregunta-texto {
            color: #3C096C; /* Morado */
            font-size: 24px;
            font-weight: bold;
            font-style: italic;
            line-height: 1.5;
            text-align: center;
        }
        .pregunta-label {
            color: #10002B; /* Morado oscuro */
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
            display: block;
        }
    </style>

    <div class="pregunta-container">
        <span class="pregunta-label">Interrogante de Investigación</span>
        <p class="pregunta-texto">
            "¿Ofrece el modelo de beneficios de salud mental centrado en las empresas de EE. UU. una mejor cobertura y apoyo para los trabajadores tecnológicos en comparación con los modelos de Europa y Oceanía, o por el contrario genera mayores barreras de acceso para los años 2017-2019?"
        </p>
    </div>
    """, unsafe_allow_html=True)
  
  with tab2:

  #objetivo general y objetivos específicos
    st.markdown("""
    <style>
    .obj-general-card {
        background: linear-gradient(135deg, #3C096C, #7B2CBF);
        color: #FFFFFF;
        border: 3px solid #E0AAFF;
        padding: 25px 35px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 8px 25px rgba(123, 44, 191, 0.4);
        margin: 10px auto 30px auto;
    }
    .obj-general-label {
        font-size: 13px; text-transform: uppercase; letter-spacing: 3px;
        color: #E0AAFF; font-weight: bold; margin-bottom: 10px; display: block;
    }
    .obj-general-text {
        font-size: 19px; line-height: 1.5; font-weight: 600; margin: 0;
    }
    
    /* TARJETAS DE OBJETIVOS ESPECÍFICOS CON EFECTO HOVER */
    .obj-esp-card {
        background-color: #10002B;
        border-left: 6px solid #E0AAFF;
        border-top: 1px solid #3C096C; 
        border-right: 1px solid #3C096C; 
        border-bottom: 1px solid #3C096C;
        padding: 20px; 
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px; 
        min-height: 140px;
        transition: all 0.3s ease-in-out; /* Animación fluida */
    }
    
    /* EFECTO CUANDO PASAS EL MOUSE */
    .obj-esp-card:hover {
        transform: translateY(-8px) scale(1.02); /* Se eleva y crece un poco */
        box-shadow: 0px 10px 25px rgba(224, 170, 255, 0.35); /* Resplandor claro */
        border-left-color: #FFD60A; /* Cambia el borde a un acento llamativo */
        border-color: #7B2CBF;
    }

    .obj-esp-numero {
        color: #E0AAFF; font-size: 12px; font-weight: bold; text-transform: uppercase;
        letter-spacing: 1px; margin-bottom: 8px; display: block;
    }
    .obj-esp-text {
        color: #FFFFFF; font-size: 14px; line-height: 1.5; margin: 0;
    }
    </style>

    <div class="obj-general-card">
        <span class="obj-general-label">🎯 Objetivo General</span>
        <p class="obj-general-text">
            "Evaluar y comparar estadísticamente la provisión de apoyo, las políticas de bienestar y la percepción organizacional de la salud mental en el sector tecnológico entre Estados Unidos, Europa y Oceanía durante el período 2017 - 2019."
        </p>
    </div>
""", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center; color: #E0AAFF; margin-bottom: 25px;'>📌 Objetivos Específicos</h4>", unsafe_allow_html=True)

# OBJETIVOS ESPECÍFICOS
    objetivos = [
    ("Objetivo Específico 01", "Comparar la frecuencia relativa de empresas tecnológicas que ofrecen beneficios de salud mental entre EE. UU., Europa y Oceanía."),
    ("Objetivo Específico 02", "Determinar la proporción de empleados que conocen sus opciones de atención de salud mental laboral según su región geográfica."),
    ("Objetivo Específico 03", "Evaluar el puntaje promedio y la dispersión de la importancia que los empleadores otorgan a la salud mental por categoría de puesto."),
    ("Objetivo Específico 04", "Analizar la distribución de frecuencias de la calificación que otorgan los empleados al apoyo general de la industria tecnológica."),
    ("Objetivo Específico 05", "Examinar la evolución temporal del puntaje promedio de importancia otorgada por los empleadores durante el periodo 2017 - 2019."),
    ("Objetivo Específico 06", "Identificar las necesidades actuales y carencias de apoyo mediante minería de textos y análisis de sentimientos en comentarios."),
    ("Objetivo Específico 07", "Analizar los motivos y el nivel de molestia en conversaciones laborales reportadas por empleados que vivieron una mala respuesta corporativa.")
]

    # DISTRIBUCIÓN columnas
    col1, col2 = st.columns(2)

    with col1:
      for num, texto in objetivos[0:5:2]:  # Impares (1, 3, 5)
        st.markdown(f"""
            <div class="obj-esp-card">
                <span class="obj-esp-numero">{num}</span>
                <p class="obj-esp-text">{texto}</p>
            </div>
        """, unsafe_allow_html=True)

        with col2:
      for num, texto in objetivos[1:6:2]:  # Pares (2, 4, 6)
        st.markdown(f"""
            <div class="obj-esp-card">
                <span class="obj-esp-numero">{num}</span>
                <p class="obj-esp-text">{texto}</p>
            </div>
        """, unsafe_allow_html=True)

# Objetivo 7 centrado al fondo
    num_7, texto_7 = objetivos[6]
    st.markdown(f"""
    <div class="obj-esp-card" style="max-width: 650px; margin: 0 auto 20px auto;">
        <span class="obj-esp-numero" style="text-align: center;">{num_7}</span>
        <p class="obj-esp-text" style="text-align: center;">{texto_7}</p>
    </div>
""", unsafe_allow_html=True)
    
    with tab3:
    st.subheader("Justificación de la Investigación")
    with st.container(border=True):
        st.markdown("""La salud mental en el ámbito laboral del área IT ha dejado de ser un tema secundario para convertirse en un factor crítico que impacta no solo la calidad de vida del empleado, sino también la productividad y retención de talento en las organizaciones. Por lo tanto, visibilizar y entender cómo se aborda esta problemática es fundamental para el desarrollo sostenible del sector. El presente análisis se justifica al proporcionar una evaluación comparativa e identificar las brechas existentes entre las políticas de bienestar de las empresas tecnológicas en Estados Unidos frente a las de Europa y Oceanía. Al contrastar un modelo donde el acceso a la salud mental depende fuertemente de los beneficios otorgados por el empleador (EE. UU.) contra modelos con marcos regulatorios o sistemas de salud pública diferentes, el estudio permite determinar qué enfoques generan una mayor percepción de apoyo, equidad y conocimiento de cobertura por parte de los trabajadores. 
        """)
        st.write("")
        st.markdown("""Finalmente, desde una perspectiva analítica y metodológica, esta investigación transforma datos categóricos y cualitativos provenientes de encuestas aplicadas entre 2014 y 2019 en métricas cuantitativas claras. A través de la limpieza estructurada en SQL y la visualización de datos en plataformas como Power BI y Python, se busca entregar una herramienta interactiva (dashboard) que facilite a los departamentos de Recursos Humanos y líderes organizacionales la toma de decisiones basadas en evidencia, impulsando así mejoras reales en la cultura organizacional de la industria tecnológica. 
        """)