import streamlit as st
# Aquí va página del planteamiento (Objetivos y variables)
st.header("Planteamiento del problema")
st.write(""" La industria tecnológica a nivel global, se ha caracterizado por ser un ambiente altamente competitivo, con ritmos de trabajo apresurados, plazos estrictos y una constante exigencia de innovación. Todas estas condiciones han proporcionado un aumento  notable en los niveles de estrés, ansiedad y desgaste profesional. Aunque en los últimos años el bienestar emocional ha cobrado mayor importancia en la agenda profesional, la manera en la que las empresas abordan y proveen apoyo en la salud mental varía drásticamente dependiendo de la ubicación geográfica.

En este sentido, surge un dilema particular al comprar a Estados Unidos con el resto del mundo. En Estados unidos, el acceso a la salud mental está fuertemente relacionado los beneficios dados por el empleador (seguros médicos privados, programas de asistencia) mientras que en otros países existen sistemas de salud pública universal o marcos regulatorios laborales, esta diferencia estructural plantea interrogantes sobre la calidad, equidad y percepción de apoyo que realmente reciben los trabajadores tecnológicos.

El problema central se basa en desconocer las diferencias en la cobertura médica, por esto resulta de interés analizar de forma estadística y comparativa si el modelo de beneficios centrado en las empresas de EE.UU ofrece una mejor cobertura para la salud mental que los modelos del resto del mundo, o por el contrario genera mayores barreras de acceso. 
""")

st.header("Justificación de la Investigación")

st.markdown("""La salud mental en el ámbito laboral del área IT ha dejado de ser un tema secundario para convertirse en un factor crítico que impacta no solo la calidad de vida del empleado, sino también la productividad y retención de talento en las organizaciones. Por lo tanto, visibilizar y entender cómo se aborda esta problemática es fundamental para el desarrollo sostenible del sector. El presente análisis se justifica al proporcionar una evaluación comparativa e identificar las brechas existentes entre las políticas de bienestar de las empresas tecnológicas en Estados Unidos frente a las de Europa y Oceanía. Al contrastar un modelo donde el acceso a la salud mental depende fuertemente de los beneficios otorgados por el empleador (EE. UU.) contra modelos con marcos regulatorios o sistemas de salud pública diferentes, el estudio permite determinar qué enfoques generan una mayor percepción de apoyo, equidad y conocimiento de cobertura por parte de los trabajadores. 

Finalmente, desde una perspectiva analítica y metodológica, esta investigación transforma datos categóricos y cualitativos provenientes de encuestas aplicadas entre 2014 y 2019 en métricas cuantitativas claras. A través de la limpieza estructurada en SQL y la visualización de datos en plataformas como Power BI y Python, se busca entregar una herramienta interactiva (dashboard) que facilite a los departamentos de Recursos Humanos y líderes organizacionales la toma de decisiones basadas en evidencia, impulsando así mejoras reales en la cultura organizacional de la industria tecnológica. 
""")

st.header("Variables Seleccionadas")
st.markdown("""
Cada posible variable está asociada a una pregunta y a su respectiva id, las mayoría de las respuestas a estas preguntas suelen ser categóricas (Sí o No).

Para cumplir con los objetivos de este análisis comparativo entre Estados Unidos, Europa y Oceania, hemos seleccionado las siguientes **10 variables clave** de la base de datos:

## 1. Variable: Pais_Vivienda (País de Residencia)

Pregunta original: (id: 3) "What country do you live in?"

Definición conceptual / operacional: Nación en la cual reside habitualmente el encuestado. Se agrupan geográficamente en regiones (Estados Unidos, Europa y Oceanía) para el análisis territorial comparativo.

Tipo de variable: Cualitativa.

Nivel / Escala de medición: Nominal.

Categorías / Valores posibles: Nombres de países registrados (ej. United States, United Kingdom, Germany, Australia).

Tabla destino: Info_Usuario (Clave foránea hacia País).

## 2. Variable: Estado_USA_Vivienda (Estado de Residencia en EE. UU.)

Pregunta original: (id: 4) "If you live in the United States, which state or territory do you live in?"

Definición conceptual / operacional: Estado o territorio federal de residencia dentro de los Estados Unidos para los encuestados domiciliados en dicho país.

Tipo de variable: Cualitativa.

Nivel / Escala de medición: Nominal.

Categorías / Valores posibles: Nombres de entidades subnacionales de EE. UU. (ej. California, New York, Texas).

Tabla destino: Usuarios_USA (Clave foránea hacia Estados_USA).

## 3. Variable: Pais_Empleo (País del Lugar de Trabajo)

Pregunta original: (id: 50) "What country do you work in?"

Definición conceptual / operacional: País donde se localiza la sede laboral o empresa empleadora del trabajador tecnológico. Constituye la variable de segmentación geográfica primaria (EE. UU. frente a Europa y Oceanía).

Tipo de variable: Cualitativa.

Nivel / Escala de medición: Nominal.

Categorías / Valores posibles: Nombres de países registrados (agrupados en EE. UU., Europa y Oceanía).

Tabla destino: Info_Usuario (Clave foránea hacia Pais).

## 4. Variable: Estado_USA_Empleo (Estado del Empleo en EE. UU.)

Pregunta original: (id: 51) "What US state or territory do you work in?"

Definición conceptual / operacional: Estado o territorio estadounidense en el que se ubica la entidad empleadora del encuestado.

Tipo de variable: Cualitativa.

Nivel / Escala de medición: Nominal.

Categorías / Valores posibles: Nombres de estados de EE. UU. (California, Washington, Massachusetts, etc.).

Tabla destino: Usuarios_USA (Clave foránea hacia Estados_USA).

## 5. Variable: Prioridad_Salud_Mental (Importancia Empresarial a la Salud Mental)

Pregunta original: (id: 65) "Overall, how much importance does your employer place on mental health?"

Definición conceptual / operacional: Puntuación numérica percibida por el empleado respecto a la relevancia o prioridad institucional que su empresa otorga al bienestar mental.

Tipo de variable: Cuantitativa discreta.

Nivel / Escala de medición: Intervalar / Escala discreta.

Categorías / Valores posibles: Números enteros del 0 (ninguna importancia) al 10 (máxima importancia).

Tabla destino: Beneficios_Trabajo_Actual.

## 6. Variable: Percepcion_Apoyo_SM_Industria (Evaluación del Apoyo de la Industria Tech)

Pregunta original: (id: 85) "Overall, how well do you think the tech industry supports employees with mental health issues?"

Definición conceptual / operacional: Nivel de respaldo percibido que el sector tecnológico general brinda a los trabajadores con trastornos o dificultades de salud mental.

Tipo de variable: Cuantitativa discreta / Cualitativa ordinal.

Nivel / Escala de medición: Ordinal / Intervalar.

Categorías / Valores posibles: Escala entera de 1 (apoyo deficiente / pésimo) a 5 (apoyo óptimo / excelente).

Tabla destino: Opinion_Industria.

## 7. Variable: Sugerencias_Mejora_SM_Industria (Recomendaciones de los Empleados)

Pregunta original: (id: 86) "Briefly describe what you think the industry as a whole and/or employers could do to improve mental health support for employees."

Definición conceptual / operacional: Propuestas abiertas y recomendaciones redactadas por los empleados para optimizar las políticas de bienestar mental corporativas. Se procesa mediante matrices de términos ponderados (TF-IDF) y cálculo de polaridad continua.

Tipo de variable: Cualitativa (Texto no estructurado).

Nivel / Escala de medición: Nominal / Corpus textual.

Categorías / Valores posibles: Descripciones de experiencias.

Tabla destino: Opinion_Industria.

## 8. Variable: Experiencia_Respuesta_Negativa_SM (Reporte de Reacción Desfavorable)

Pregunta original: (id: 56) "Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?"

Definición conceptual / operacional: Indicador de haber vivido o presenciado una respuesta insensible, mal gestionada o punitiva ante una dificultad de salud mental en el trabajo. Opera como criterio de filtro para analizar situaciones de conflicto.

Tipo de variable: Cualitativa.

Nivel / Escala de medición: Nominal (Dicotómica / Politómica).

Categorías / Valores posibles: Yes, No, Maybe (o sus equivalentes binarios/categóricos).

Tabla destino: Experiencia_Trabajo_Actual.

## 9. Variable: Descripcion_Conversacion_Companeros_SM (Diálogo Propio con Compañeros)

Pregunta original: (id: 61) "Describe the conversation with coworkers you had about your mental health including their reactions."

Definición conceptual / operacional: Relato cualitativo emitido por el trabajador sobre el diálogo entablado con compañeros de trabajo al revelar su condición de salud mental, incluyendo sus reacciones percibidas. Se analiza mediante frecuencias léxicas y sentimiento.

Tipo de variable: Cualitativa (Texto no estructurado).

Nivel / Escala de medición: Nominal / Corpus textual.

Categorías / Valores posibles: Descripciones de experiencias

Tabla destino: Experiencia_Trabajo_Actual.

## 10. Variable: Descripcion_Conversacion_Companero_SM (Diálogo Revelado por un Compañero)

Pregunta original: (id: 63) "Describe the conversation your coworker had with you about their mental health (please do not use names)."

Definición conceptual / operacional: Testimonio abierto en el que el empleado narra la situación y el intercambio comunicativo cuando un par laboral compartió su estado de salud mental.

Tipo de variable: Cualitativa (Texto no estructurado).

Nivel / Escala de medición: Nominal / Corpus textual.

Categorías / Valores posibles: Descripciones de experiencias

Tabla destino: Experiencia_Trabajo_Actual.
""")