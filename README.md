<p align="center">
  <img src="assets/bannerapp.png" alt="Análisis de Apoyo a la Salud Mental en el Área IT" width="100%">
</p>

# 🧠 Análisis de Apoyo a la Salud Mental en el Área IT


Este trabajo consiste en un proyecto de análisis de datos aplicado busca realizar un análisis comparativo y estadístico sobre el acceso a beneficios de salud mental, políticas de bienestar y percepción del apoyo organizacional en el sector tecnológico, contrastando los panoramas de Estados Unidos, Europa y Oceanía pre pandemia. Con el objetivo de identificar brechas críticas en la cobertura médica y evaluar las diferencias en la cultura corporativa entre regiones.


Para lograr esto, la investigación de este proyecto se fundamenta en el procesamiento y análisis de datos históricos provenientes de las encuestas globales de Open Source Mental Illness (OSMI) de los periodos 2017-2019. 

## 📝 Metodología Estadística

Este trabajo adopta un diseño de investigación descriptivo. En consecuencia, los hallazgos presentados se limitan a caracterizar y resumir las propiedades del fenómeno estudiado, sin pretensiones de generalización estadística o inferencial.

## 🎯 Objetivo General

Evaluar y comparar estadísticamente la provisión de apoyo, las políticas de bienestar y la percepción organizacional de la salud mental en el sector tecnológico entre Estados Unidos, Europa y Oceanía durante el período 2017 - 2019.

## 📋 Objetivos Específicos

1. **Comparar la frecuencia relativa de empresas tecnológicas que ofrecen beneficios de salud mental entre Estados Unidos, Europa y Oceanía.**
   * *Explicación:* Hacer una tabla cruzada para contar cuántos encuestados de EE. UU. marcaron "SÍ" en beneficios, frente a los de Europa y Oceanía.

2. **Determinar la proporción de empleados que conocen sus opciones de atención de salud mental laboral según su región geográfica.**
   * *Explicación:* Calcular el porcentaje de personas que afirman conocer sus opciones de cobertura, separando los datos por ubicación.

3. **Calcular y comparar el puntaje promedio y la dispersión de la importancia que los empleadores otorgan a la salud mental por categoría de puesto.**
   * *Explicación:* Determinar el nivel de prioridad que las empresas asignan a la salud mental mediante el cálculo de promedios y medidas de variabilidad, comparando el comportamiento del sector en Estados Unidos frente a Europa y Oceanía.

4. **Analizar la distribución de frecuencias de la calificación que otorgan los empleados al apoyo general de la industria tecnológica en temas de salud mental según su ubicación.**
   * *Explicación:* Evaluar la percepción de los empleados sobre el respaldo de la industria tecnológica, comparando las tendencias y concentraciones de respuestas según su zona geográfica.

5. **Calcular y comparar el puntaje promedio de importancia que los empleadores otorgan a la salud mental.**
   * *Explicación:* Separar los datos de EE. UU., los de Europa y Oceanía, y calcular medidas de tendencia central y de dispersión para cada grupo.

6. **Identificar las necesidades actuales sobre el apoyo y los beneficios de salud mental en la industria tecnológica.**
   * *Explicación:* Extraer y priorizar las demandas y carencias principales de los empleados mediante técnicas de minería de textos y análisis de sentimientos aplicados a sus comentarios y propuestas de mejora, comparando los hallazgos de EE. UU. frente a Europa y Oceanía.

### Técnicas Usadas:

Cálculo de frecuencias absolutas y relativas para categorizar la oferta de beneficios por región.
Elaboración de gráficos de barras apiladas para comparar el nivel de conocimiento de cobertura entre EE. UU., Europa y Oceanía.
Análisis de proporciones para evaluar la percepción de la seriedad en el tratamiento de la salud mental.
Tabulación de datos para resumir la frecuencia de campañas de bienestar organizacional según el país.


## 🛠️ Stack Tecnológico

El proyecto está construido en una arquitectura modular que integra análisis de datos, persistencia en la nube e inteligencia artificial:

* **Python (SQLite):** Lenguaje principal utilizado para la extracción, limpieza y procesamiento de datos, así como para la lógica de integración entre las bases de datos.

* **MotherDuck:** La utilizamos para guardar los conjuntos de datos del proyecto y ejecutar las consultas SQL

* **Supabase:** Aloja nuestros datos de la base de datos normalizada como proyecto 

* **Google AI Studio:** Integramos el modelo generativo configurado como **agente consejero**, encargado de interpretar el contexto del usuario y ofrecer recomendaciones personalizadas dentro de la plataforma.

## 💻 Modelado y Limpieza de Datos:

* **Modelado de Datos:** Estructuramos la información con dos enfoques que se complementan: un modelo relacional (normalizado) para garantizar la integridad referencial en operaciones transaccionales, y un modelo dimensional (tablas de hechos y dimensiones) optimizado para consultas analíticas rápidas.

* **Análisis de Sentimientos (Nubes de Palabras):** Aplicación de técnicas de procesamiento de texto para evaluar la polaridad de los registros e identificar los conceptos y palabras clave más frecuentes mediante nubes de palabras.

* **Imputación de Datos:** Tratamiento de valores nulos, evitando la pérdida de muestra y preservando la consistencia del conjunto de datos para el análisis posterior.

## 📚 Base de Datos

### Fuente:
La base de datos utilizada para este proyecto es de Kaggle y proviene de Open Source Mental Illness (OSMI), la fuente original tiene datos desde 2014, el proyecto se acota al período 2017–2019 por consistencia en las variables.                                                                                       

[👉 Ver Base de Datos](https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry)

### Modelo Dimensional:
Moodelo Dimensional derivado de la base de datos original, utilizado en la tanto el la app como en el dashboard.

<p align="center">
  <img src="assets\Modelo Dimensional.jpg" alt="Modelo Dimensional" width="100%">
</p>

## 📊 Despliegue Analítico:

### Informe Dinámico en Streamlit:
[🧠 Visita Nuestra App de Streamlit](https://encuesta-salud-mental-osmi.streamlit.app/)

### Dashboard en PowerBI:
[📊 Explora Nuestro Dashboard en PowerBI](https://app.powerbi.com/view?r=eyJrIjoiNTU0YmU5YmMtYTdhYi00ZjA0LWIwYjQtNzNhNzE0M2QwZTQwIiwidCI6IjRjODE4Zjc5LWFiODQtNDU1Mi05YjdjLTJmZTcxNWIwZDBkNSIsImMiOjR9)

## ⚙️ ¿Cómo Ejecutar el Proyeto?

## 1. Clona el Repositorio
```bash
git clone [https://github.com/Aymara1010/Grupo-9-Analisis-Apoyo-Salud-Mental-en-el-Area-IT.git](https://github.com/Aymara1010/Grupo-9-Analisis-Apoyo-Salud-Mental-en-el-Area-IT.git)
cd Grupo-9-Analisis-Apoyo-Salud-Mental-en-el-Area-IT
```
## 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

## 3. Configura credenciales y ejecuta la App

```bash
streamlit run app.py
```

## 📂 Estrucura del Repositorio
El repositorio de este proyecto está estructurado de la siguiente manera:
```bash
├── Base de Datos/            # Limpieza de la Base de Datos.
├── Paginas/                  # Páginas de la App de Streamlit
├── PowerBI/                  # Páginas de la App de Streamlit
├── assets/                   # Elementos visuales.
├── app.py                    # Código principal de la App de Streamlit
├── requirements.txt          # Listado de librerías de Python
├── .gitignore
└── README.md                 # Este archivo
```

## 👥 Creado Por
**Grupo 9 - EECA UCV** 

- **Aymara Andersen** (@Aymara1010)
- **Angelo Freda** (@angelofreda4315-code)
- **Christopher Escalante** (@christopherescalanteb-pixel)
- **Randy Conde** (@randyl21)
- **Rehide De Pablos** (@depablosrehide-cdm)
- **Andrea Figuera** (figueraandrea25-hub)