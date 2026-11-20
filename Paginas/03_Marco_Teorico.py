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

tab_marco, tab_modelado = st.tabs([
    "📚 Marco Teórico",
    "🛠️ Modelado y Limpieza de Datos",
])

with tab_marco:
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
                    Este marco reúne la base conceptual para entender la salud mental en tecnología a partir de OSMI: cómo el <i>burnout</i>, el tecnoestrés y la modalidad de trabajo inciden en el bienestar y la seguridad psicológica del equipo, y por qué la comparación regional depende en gran medida de si el acceso a salud está ligado al empleo (EE. UU.) o respaldado por sistemas públicos y protecciones laborales más amplias (Europa y Oceanía).
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

with tab_modelado:
  st.markdown(
      """
        <div class="resumen-3d-wrapper">
            <div class="resumen-3d-card">
                <span class="etiqueta-resumen">🏷️ Mini Resumen</span>
                <p class="texto-resumen-interno">
                    Se transforma el esquema EAV original de OSMI en un flujo analítico delimitado a <b>2017–2019</b> (EE. UU., Europa y Oceanía): auditoría de datos crudos, normalización 3FN en SQLite, depuración/imputación, modelado dimensional en estrella sobre <b>DuckDB</b> y clasificación emocional de relatos laborales con <b>BM25</b>.
                </p>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  with st.container():
    st.markdown(
        '<span class="marcador-modelado-fijo"></span>', unsafe_allow_html=True
    )
    st.markdown("""
        Garantizar la calidad e integridad de la información es un paso fundamental antes de realizar cualquier análisis estadístico. Por esta razón, en esta sección se detalla el proceso técnico de estructuración, depuración y saneamiento de la base de datos utilizada.

        ### Estructura Original de la Base de Datos OSMI
        Como se indicó en el planteamiento del problema, la información de origen proviene de la encuesta OSMI. Su esquema inicial se compone de tres tablas principales que almacenan las respuestas, el catálogo de preguntas y las ediciones del estudio:
        - **Answer:** Contiene los registros de respuesta (`AnswerText`, `SurveyID`, `UserID`, `QuestionID`).
        - **Question:** Define las preguntas formuladas (`questionid`, `questiontext`).
        - **Survey:** Registra las distintas ediciones de la encuesta (`SurveyID`, `Description`).

        Dado que el modelo original de la base de datos dificulta el procesamiento analítico eficiente, fue indispensable transformar su estructura. A continuación, se examinan las características de la arquitectura de origen.

        ### Modelo EAV (Entidad-Atributo-Valor)
        La base de datos original utiliza el modelo Entidad-Atributo-Valor (EAV). Este esquema ofrece una elevada flexibilidad para incorporar nuevos atributos sin alterar la estructura base, siendo común en herramientas de recolección de encuestas dinámicas como OSMI. No obstante, la flexibilidad del modelo EAV conlleva limitaciones severas para el análisis de datos y la inferencia estadística:
        - Almacenamiento apilado verticalmente en texto plano (`AnswerText`) para variables de distinta naturaleza.
        - Necesidad de realizar múltiples combinaciones (*joins*) complejas y costosas para construir consultas analíticas.
        - Ausencia de validación y control estricto sobre los tipos de datos.

        Para superar estos inconvenientes, se diseñó un canal de ingeniería de datos (ETL) estructurado en etapas: auditoría y delimitación de datos crudos, normalización en un modelo relacional, depuración/imputación, construcción de un esquema dimensional y análisis de sentimientos con nubes de palabras.
        
        ### Etapa 1: Auditoría y Delimitación de Datos Crudos
        La fuente original reúne 4,218 encuestados en las ediciones de 2014, 2016, 2017, 2018 y 2019. Al evaluar la calidad de los datos de origen, se identificaron y corrigieron los siguientes aspectos críticos:
        - **Disparidad temporal y delimitación:** Varias preguntas no estuvieron presentes en todas las versiones del cuestionario (por ejemplo, el cargo laboral solo se incluyó en 2016). Con el fin de asegurar la homogeneidad del estudio, la muestra se acotó al período **2017–2019**, que contiene 76 preguntas constantes e integra a **756 participantes de 2017**, **417 de 2018** y **352 de 2019**.
        - **Valores de relleno o centinela:** Respuestas no aplicables, omisiones o selecciones de *"No sabe"* venían representadas bajo el valor numérico `-1`, campos en blanco o puntos (`.`).
        - **Incongruencias tipográficas y datos atípicos:** Se hallaron campos cuantitativos formateados como texto y registros de edad fuera del rango biológico o laboral esperado (menores de 18 o mayores de 85 años).
        - **Variaciones léxicas:** Falta de estandarización en respuestas abiertas para un mismo concepto, evidenciada en nombres de países (e.g., `"US"`, `"USA"`, `"United States"`) y en las denominaciones de condiciones de salud mental.

        ### Etapa 2: Transformación al Modelo Relacional (3FN)
        Buscando erradicar la redundancia del esquema EAV y garantizar la coherencia referencial, se estructuró un modelo relacional en **Tercera Forma Normal (3FN)** mediante el motor **SQLite**, ejecutado a través del siguiente procedimiento:
        - Configuración de catálogos base.
        - Creación de la entidad transaccional.
        - Pivoteo a tablas temáticas (1:1).
        - Manejo de selecciones múltiples (N:M).
    """)
    with st.expander("💜 **MODELO RELACIONAL**"):
      st.markdown('<div class="img-marco-fija">', unsafe_allow_html=True)
      st.image("assets\Modelo Relacional.jpg", use_container_width=True)
      st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
        ### Etapa 3: Limpieza, Depuración e Imputación de Datos
        Con la base de datos relacional establecida, se aplicaron directrices de saneamiento para prevenir sesgos en los posteriores análisis descriptivos y textuales:
        - **Estandarización de nulos y conversión de tipos:** Los valores centinela (`-1`), cadenas vacías y puntos (`.`) se reemplazaron por valores `NULL` explícitos. Se ejecutaron conversiones explícitas para adecuar escalas numéricas.
        - **Depuración de registros vacíos:** Se removieron mediante sentencias `DELETE` aquellas filas de tablas temáticas que carecían de información en la totalidad de sus campos, situación derivada de la lógica condicional del cuestionario.
        - **Imputación cruzada:** Se imputaron los valores de las variables utilizadas.
        - **Filtro de alcance geográfico:** Se unificaron las variables de país en tres macro regiones de interés (**Estados Unidos, Europa y Oceanía**), excluyendo los registros pertenecientes a otras ubicaciones geográficas.
        - **Procesamiento de texto libre:** Para los campos de respuesta abierta se asignó `NULL` a textos evasivos, monosílabos, expresiones genéricas y kaomojis/emojis. Asimismo, se filtraron entradas con longitud menor a 15 caracteres o con menos de 4 palabras, eliminando palabras de paro (*stopwords*) para optimizar el análisis de sentimiento y la vectorización TF-IDF.

        ### Etapa 4: Modelado Dimensional (DuckDB)
        Si bien la arquitectura en 3FN desplegada en SQLite garantiza la integridad transaccional (OLTP), las operaciones analíticas complejas sufren degradación en su desempeño. Por esta razón, el conjunto de datos se trasladó a un **esquema dimensional en estrella** (siguiendo la metodología de Ralph Kimball) sobre **DuckDB**, un motor columnar orientado al procesamiento analítico (OLAP):
        - **Paso 1 — Proceso de negocio:** Evaluación del acceso a beneficios de salud mental en el sector tecnológico mediante la encuesta anual OSMI (2017–2019), en Estados Unidos, Europa y Oceanía.
        - **Paso 2 — Granularidad:** Una fila por cada respuesta individual emitida por un encuestado en una edición anual delimitada estrictamente al período 2017–2019 y a trabajadores cuyo país de empleo pertenezca a EE. UU., Europa u Oceanía.
        - **Paso 3 — Dimensiones:** Construidas con claves subrogadas y combinaciones únicas como *Tiempo y territorio* o *Perfil del encuestado y empresa*.
        - **Paso 4 — Hechos:** Guarda las métricas como la prioridad o preguntas de respuesta abierta.
    """)
    with st.expander("💜 **MODELO DIMENSIONAL**"):
      st.markdown('<div class="img-marco-fija">', unsafe_allow_html=True)
      st.image("assets\Modelo Dimensional.jpg", use_container_width=True)
      st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
        ### Etapa 5: Análisis de Sentimientos y Nubes de Palabras
        Para aprovechar las respuestas abiertas sobre conversaciones laborales (`Descripcion_Conversacion_Companeros_Sobre_SM` y `Descripcion_Conversacion_Sobre_Companero_SM`) dentro del análisis descriptivo, fue necesario transformar estos relatos cualitativos no estructurados en indicadores cuantificables e integrarlos al modelo dimensional. Para lograrlo, se implementó un flujo de procesamiento de lenguaje natural basado en diccionarios contextuales y el algoritmo **BM25** (*Best Matching 25*), que permite medir la polaridad e intensidad emocional de cada testimonio y extraer visualmente los términos más representativos:
        - **Depuración y tokenización:** Sobre los relatos filtrados en la etapa de limpieza, se normalizaron los textos a minúsculas y se extrajeron sus palabras clave (*tokens*) para evitar sesgos en la clasificación.
        - **Diccionarios temáticos y catálogo (`Dim_Emociones`):** Se construyeron tres léxicos acotados al entorno laboral de OSMI (*Negativa, Positiva y Neutra*) y se pobló `Dim_Emociones` con cinco rangos que combinan polaridad e intensidad (*Muy Alta, Alta y Neutro*).
        - **Clasificación e intensidad con BM25:** Cada relato se evaluó frente a los tres diccionarios actuando como consultas; a diferencia del conteo simple, BM25 pondera la rareza de las palabras y normaliza por la longitud del texto. El puntaje más alto definió la emoción dominante y su magnitud determinó la intensidad, actualizando directamente las claves foráneas en `Fact_Respuesta_Encuestado`.
        - **Nubes de palabras ponderadas:** Los testimonios se agruparon por emoción dominante, removiendo palabras vacías (*stopwords*) y términos repetitivos propios de la encuesta (`mental`, `health`, `coworker`, `work`). El tamaño de cada palabra se ponderó según su peso acumulado en BM25, utilizando paletas de color semánticas (rojo para negativa, verde para positiva y azul para neutra).
        """)