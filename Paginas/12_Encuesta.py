
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

    st.markdown("---")
    
    st.subheader("3. Percepción del Entorno Laboral y Beneficios")
    col5, col6 = st.columns(2)
    with col5:
        beneficios = st.radio("¿Tu empresa ofrece beneficios explícitos para salud mental?", ["Sí", "No", "No lo sé"])
        privacidad = st.radio("¿Tu empleador protege la privacidad si buscas tratamiento?", ["Sí", "No", "No lo sé"])
    with col6:
        cobertura = st.radio("¿Conoces los detalles de la cobertura de salud mental ofrecida?", ["Sí", "No", "No aplica"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    imp_mental = st.slider("Importancia que tu empresa le da a la Salud Mental (1-10)", 1, 10, 5)
    imp_fisica = st.slider("Importancia que tu empresa le da a la Salud Física (1-10)", 1, 10, 5)

    
    enviado = st.form_submit_button("💜 Enviar Encuesta", use_container_width=True)

if enviado:

    datos = {
        "p_edad": edad, "p_genero": genero, "p_exp": exp_tech, "p_mod": modalidad,
        "p_facultad": facultad, "p_area": area_tech, "p_rol": rol, "p_free": freelance,
        "p_emp": empresa_tech, "p_ant": antecedentes, "p_trat": buscado_tratamiento,
        "p_cond": condicion_actual, "p_ben": beneficios, "p_priv": privacidad,
        "p_cob": cobertura, "p_imp_m": imp_mental, "p_imp_f": imp_fisica
    }
    
    query = text("""
        INSERT INTO public.estudiante (
            edad, genero, experiencia_tecnologica, modalidad_trabajo, facultad_estudio, 
            area_tecnologica, rol_especifico, trabaja_freelance, empresa_puramente_tecnologia,
            antecedentes_familiares, buscado_tratamiento, condicion_actual,
            beneficios_empresa, privacidad_tratamiento, conoce_cobertura,
            importancia_salud_mental_empresa, importancia_salud_fisica_empresa
        ) VALUES (
            :p_edad, :p_genero, :p_exp, :p_mod, :p_facultad, 
            :p_area, :p_rol, :p_free, :p_emp,
            :p_ant, :p_trat, :p_cond,
            :p_ben, :p_priv, :p_cob,
            :p_imp_m, :p_imp_f
        )
    """)
    
    try:
        with engine.begin() as con:
            con.execute(query, datos)
        st.success("¡Tus respuestas se han guardado exitosamente en nuestra base de datos!")
        st.balloons()
    except Exception as e:
        st.error(f"Error al enviar la encuesta: {e}")