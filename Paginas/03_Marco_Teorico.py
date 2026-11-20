import streamlit as st
# Aquí va página del Marco Teorico (Antecedentes y Conceptos)

st.title("Marco Teórico📖")
st.markdown("----")

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

.resumen-3d-card:hover {
    transform: translateY(-6px) rotateX(2deg) rotateY(-1.5deg);
    box-shadow:
        0 24px 38px rgba(60, 9, 108, 0.25),
        0 8px 0 #240046;
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

/* Estiliza el contenedor de Streamlit que contiene el marcador */
div[data-testid="stVerticalBlock"]:has(.marcador-marco-fijo) {
    background: #ffffff;
    border-left: 5px solid #7B2CBF;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 6px 16px rgba(60, 9, 108, 0.08);
}

.marcador-marco-fijo {
    display: none;
}

.img-marco-fija img {
    border-radius: 14px;
    box-shadow: 0 10px 22px rgba(60, 9, 108, 0.14);
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown('<div class="img-marco-fija">', unsafe_allow_html=True)
st.image("assets/puntos.png", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.write("")

#mini resumen
st.markdown(
    """
<div class="resumen-3d-wrapper">
    <div class="resumen-3d-card">
        <span class="etiqueta-resumen">🏷️ Mini Resumen</span>
        <p class="texto-resumen-interno">
            Este marco reúne la base conceptual para entender la salud mental en tecnología a partir de los datos: cómo el tecnoestrés y la modalidad de trabajo inciden en el bienestar y la seguridad psicológica del equipo, y por qué la comparación regional depende en gran medida de si el acceso a salud está ligado al empleo (EE. UU.) o respaldado por sistemas públicos y protecciones laborales más amplias (Europa y Oceanía).
        </p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
#texto de info
with st.container():
  st.markdown('<span class="marcador-marco-fijo"></span>', unsafe_allow_html=True)
  st.markdown("""

 1. Antecedentes de la Investigación
El estudio de la salud mental en el entorno laboral ha cobrado especial relevancia en la última década.
 En el sector tecnológico, organizaciones como Open Source Mental Illness (OSMI) han liderado la recolección de datos empíricos desde 2014 para visibilizar la frecuencia de trastornos mentales en profesionales de IT. 
 Investigaciones previas a la pandemia de COVID-19 ya advertían sobre una crisis de estrés y agotamiento en el sector, impulsada por las exigencias de la transformación digital. 
 Estos estudios establecen que la falta de apoyo organizacional no solo deteriora el bienestar individual, sino que eleva las tasas de rotación y reduce la productividad, sentando el precedente para comparar cómo diferentes regiones del mundo mitigan esta problemática.
2. Bases Teóricas
El presente estudio se fundamenta en las siguientes dimensiones teóricas que explican la interacción entre el empleado y su entorno:
- **El Síndrome de Burnout y la Carga Cognitiva:** En el sector tecnológico, la exigencia de actualización constante y el cumplimiento de plazos ajustados (metodologías ágiles) generan una alta carga cognitiva que, sostenida en el tiempo, desencadena el desgaste profesional o Burnout.
- **Impacto Psicosocial de la Modalidad de Trabajo:** El trabajo remoto (100%), si bien ofrece flexibilidad, propicia el aislamiento social y la hiperconectividad; mientras que los modelos híbridos o presenciales enfrentan desafíos de autonomía y dinámica de oficina.
- **Cultura Organizacional y Seguridad Psicológica:** La responsabilidad del bienestar recae en la empresa a través de beneficios explícitos y la protección de la privacidad, mitigando el estigma para que los empleados busquen tratamiento.
- **Vulnerabilidad Demográfica y Ocupacional:** Variables como la edad (perfiles Junior frente a la curva de aprendizaje), el género (presión en un sector dominado por hombres) y los antecedentes familiares interactúan directamente con los estresores ambientales.
3. Definición de Términos Básicos
Para la estandarización y correcta interpretación del estudio, se definen los siguientes conceptos clave:
- **Síndrome de Burnout:** Fenómeno clínico-ocupacional resultante del estrés crónico en el lugar de trabajo, caracterizado por agotamiento extremo, distanciamiento mental y reducción de la eficacia.
- **Seguridad Psicológica:** Creencia compartida por los miembros de un equipo de que el entorno es seguro para tomar riesgos interpersonales, como revelar una condición de salud mental sin temor a represalias o despidos.
- **Tecnoestrés:** Estado psicológico negativo relacionado con el uso constante de la tecnología, la sobreinformación o la hiperconectividad, muy común en roles de IT.
- **Beneficios Corporativos en Salud Mental:** Conjunto de prestaciones no salariales provistas por el empleador, que incluyen seguros médicos privados, programas de asistencia al empleado (EAP) y días libres por salud mental.

### 4. Marco Legal 
Dado el enfoque comparativo de esta investigación, el marco regulatorio y estructural de la salud actúa como el diferenciador macroeconómico principal:
- **Estados Unidos:** Carece de un sistema de salud pública universal para la población general activa. El acceso a tratamientos psicológicos o psiquiátricos depende casi en su totalidad de los seguros médicos proporcionados por el empleador (regulados por normativas como ERISA y ACA).
- **Europa y Oceanía:** La mayoría de los países en estas regiones cuentan con sistemas de salud pública universal financiados por el Estado y leyes laborales con fuertes protecciones obligatorias para el bienestar del trabajador.

""")