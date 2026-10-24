
import streamlit as st
from sqlalchemy import text
from conexion import engine

st.title("📝 Encuesta: Salud Mental en el Área IT")
st.markdown("Tu participación nos ayuda a entender mejor el panorama actual. Los datos son anónimos.")

with st.form("encuesta_osmi"):
    
    st.subheader("1. Perfil Demográfico y Laboral")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad = st.number_input("Edad", min_value=15, max_value=100, value=28)
        genero = st.selectbox("Género", ["Femenino", "Masculino", "No binario", "Prefiero no decirlo"])
        exp_tech = st.selectbox("Años de experiencia en el sector", ["Menos de 1 año", "1-3 años", "3-5 años", "Más de 5 años"])
        modalidad = st.selectbox("Modalidad de Trabajo Actual", ["Remoto (100% desde casa)", "Híbrido", "Presencial"])

    with col2:
        facultad = st.selectbox("Facultad de Estudio", ["Ciencias Económicas y Sociales", "Ingeniería", "Ciencias", "Otra"])
        area_tech = st.selectbox("Área Tecnológica", ["Desarrollo de Software", "Data Science / Análisis", "Ciberseguridad", "Otra"])
        rol = st.selectbox("Rol Específico", ["Desarrollador Frontend", "Desarrollador Backend", "Data Analyst", "Otro"])
        freelance = st.selectbox("¿Trabajas como Freelance?", ["Sí", "No"])
        empresa_tech = st.selectbox("¿Trabajas en una empresa puramente de tecnología?", ["Sí", "No"])

    st.markdown("---")
    
    st.subheader("2. Salubridad Emocional e Historial Individual")
    col3, col4 = st.columns(2)
    with col3:
        antecedentes = st.radio("¿Tienes antecedentes familiares de afecciones de salud mental?", ["Sí", "No", "No lo sé"])
        buscado_tratamiento = st.radio("¿Has buscado tratamiento profesional?", ["Sí", "No"])
    with col4:
        condicion_actual = st.radio("Actualmente, ¿consideras que tienes una condición de salud mental?", ["Sí", "No", "Tal vez / No lo sé"])

