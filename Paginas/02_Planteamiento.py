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
  