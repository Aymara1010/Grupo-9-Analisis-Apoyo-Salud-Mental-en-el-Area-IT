import streamlit as st
# Aquí va página del planteamiento (Objetivos y variables)
st.header("Planteamiento del problema")
st.write(""" La industria tecnológica a nivel global, se ha caracterizado por ser un ambiente altamente competitivo, con ritmos de trabajo apresurados, plazos estrictos y una constante exigencia de innovación. Todas estas condiciones han proporcionado un aumento  notable en los niveles de estrés, ansiedad y desgaste profesional. Aunque en los últimos años el bienestar emocional ha cobrado mayor importancia en la agenda profesional, la manera en la que las empresas abordan y proveen apoyo en la salud mental varía drásticamente dependiendo de la ubicación geográfica.

En este sentido, surge un dilema particular al comprar a Estados Unidos con el resto del mundo. En Estados unidos, el acceso a la salud mental está fuertemente relacionado los beneficios dados por el empleador (seguros médicos privados, programas de asistencia) mientras que en otros países existen sistemas de salud pública universal o marcos regulatorios laborales, esta diferencia estructural plantea interrogantes sobre la calidad, equidad y percepción de apoyo que realmente reciben los trabajadores tecnológicos.

El problema central se basa en desconocer las diferencias en la cobertura médica, por esto resulta de interés analizar de forma estadística y comparativa si el modelo de beneficios centrado en las empresas de EE:UU ofrece una mejor cobertura para la salud mental que los modelos del resto del mundo, o por el contrario genera mayores barreras de acceso. 
""")st.header("Justificación de la Investigación")

st.header("Justificación de la Investigación")

st.markdown(""" La salud mental en el ámbito laboral del área IT ha dejado de ser un tema secundario para convertirse en un factor crítico
que impacta no solo la calidad de vida del empleado, sino también la productividad y retención de talento en las organizaciones.
Por lo tanto, visibilizar y entender cómo se aborda esta problemática es fundamental para el desarrollo sostenible del sector. 
El presente análisis se justifica al proporcionar una evaluación comparativa e identificar las brechas existentes entre las políticas de bienestar de las empresas tecnológicas en Estados Unidos frente a las del resto del mundo. 
Al contrastar un modelo donde el acceso a la salud mental depende fuertemente de los beneficios otorgados por el empleador (EE. UU.) contra modelos con marcos regulatorios o sistemas de salud pública diferentes, 
el estudio permite determinar qué enfoques generan una mayor percepción de apoyo, equidad y conocimiento de cobertura por parte de los trabajadores. 
Finalmente, desde una perspectiva analítica y metodológica, esta investigación transforma datos categóricos y cualitativos provenientes de encuestas aplicadas entre 2014 y 2019 en métricas cuantitativas claras. 
A través de la limpieza estructurada en SQL y la visualización de datos en plataformas como Power BI y Python, se busca entregar una herramienta interactiva (dashboard) que facilite a los departamentos de Recursos Humanos y líderes organizacionales la toma de decisiones basadas en evidencia, impulsando así mejoras reales en la cultura organizacional de la industria tecnológica.""")

st.header("Variables Seleccionadas")
st.markdown("""
Para cumplir con los objetivos de este análisis comparativo entre Estados Unidos y el resto del mundo, hemos seleccionado las siguientes **6 variables clave** de la base de datos:

*   **País (ID 3):** *What country do you live in?*
    Permite segmentar la muestra de individuos encuestados según su ubicación geográfica.
*   **Beneficio (ID 10):** *Does your employer provide mental health benefits as part of healthcare coverage?*
    Evalúa la provisión directa de beneficios de salud mental por parte de las empresas tecnológicas.
*   **Conocimiento_Cobertura (ID 14):** *Do you know the options for mental health care available under your employer-provided health coverage?*
    Mide el nivel de información y transparencia organizacional hacia los empleados.
*   **Prioridad_Salud_Mental (ID 65):** *Overall, how much importance does your employer place on mental health?*
    Cuantifica la percepción del empleado sobre el nivel de importancia que la empresa le otorga a la salud mental.
*   **Percepción_Apoyo_SM_Industria (ID 85):** *Overall, how well do you think the tech industry supports employees with mental health issues?*
    Mide la evaluación general del empleado respecto al apoyo de la industria tecnológica en su conjunto.
*   **Sugerencias_Mejora_SM_Industria (ID 86):** *Briefly describe what you think the industry as a whole and/or employers could do to improve mental health support for employees.*
    Variable cualitativa abierta que permitirá identificar necesidades actuales y barreras de acceso.
""")

