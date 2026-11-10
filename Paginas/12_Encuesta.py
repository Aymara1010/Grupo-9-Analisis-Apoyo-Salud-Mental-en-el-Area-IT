import streamlit as st
import random
from sqlalchemy import text
from conexion import engine
from google import genai
from google.genai import types

@st.cache_resource(show_spinner=False)
def obtener_cliente_ia():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def pedir_consejo_ia(resumen_respuestas):
    cliente = obtener_cliente_ia()
    instrucciones = (
        "Actúa como un consejero de bienestar laboral en el área de tecnología, basándote en el contexto OSMI. "
        "Con los datos del usuario, dale un consejo cercano, empático y directo dividido en 3 partes: "
        "1. Qué tal se ve su entorno de trabajo actual (comparando el apoyo a la salud mental vs física y sus beneficios). "
        "2. Una recomendación personal según su historial y la privacidad en su trabajo. "
        "3. Un consejo práctico que pueda aplicar hoy mismo. "
        "No pases de 200 palabras, evita dar diagnósticos médicos y responde en Markdown todo en un texto de tres parrafos."
    )
    
    respuesta = cliente.models.generate_content_stream(
        model="gemini-3.5-flash-lite",
        contents=resumen_respuestas,
        config=types.GenerateContentConfig(
            system_instruction=instrucciones,
            temperature=0.7
        )
    )
    
    for fragmento in respuesta:
        if fragmento.text:
            yield fragmento.text

# --- CONFIGURACIÓN DE ESTILO PERSONALIZADO (LILA / MORADO) ---
st.markdown("""
    <style>
    div[data-testid="stForm"] {
        background-color: rgba(255, 255, 255, 0.85);
        border: 2px solid #d8b4fe;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(131, 56, 236, 0.08);
    }
    .stButton>button {
        background: linear-gradient(90deg, #7B2CBF 0%, #3C096C 100%);
        color: white;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 0.6rem 2rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #5a189a 0%, #240046 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(60, 9, 108, 0.3);
    }
    h1, h2, h3 {
        color: #3C096C !important;
    }
    .mensaje-motivacional {
        background-color: #ffffff;
        border-left: 5px solid #7B2CBF;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💜 📝 Encuesta sobre Bienestar y Salud Mental en el Sector Tecnológico")
st.markdown("""
Esta encuesta recopila métricas sobre **bienestar emocional, antecedentes y cultura organizacional** 
en el sector de tecnología. Tu participación es totalmente confidencial y anónima.
""")

st.divider()

if "encuesta_enviada" not in st.session_state:
    st.session_state.encuesta_enviada = False
if "consejo_ia" not in st.session_state:
    st.session_state.consejo_ia = None
if "datos_prompt" not in st.session_state:
    st.session_state.datos_prompt = ""

if not st.session_state.encuesta_enviada:
    with st.form("encuesta_osmi"):

         # ------------------- SECCIÓN 1: PERFIL GENERAL ------------------

        st.subheader("1. Perfil Demográfico y Laboral")
        
        col1, col2 = st.columns(2)
        
        with col1:
            edad = st.number_input("Edad", min_value=15, max_value=100, value=None)
            genero = st.selectbox("Género", ["Femenino", "Masculino", "No binario", "Prefiero no decirlo"], index=None)
            facultad = st.selectbox("Facultad de Estudio", ["Ciencias Económicas y Sociales", "Ingeniería", "Ciencias", "Otra"], index=None) 
        with col2:
            area_tech = st.selectbox("Área Tecnológica", ["Desarrollo de Software", "Data Science / Análisis", "Ciberseguridad", "Otra"], index=None)
            rol = st.selectbox("¿Tu rol principal en la empresa está relacionado con la tecnología/TI?", ["Sí", "No"], index=None)
            empresa_tech = st.selectbox("¿Es tu empleador principalmente una empresa u orgnizacion tecnologia?", ["Sí", "No"], index=None)

        st.markdown("---")
        
        st.subheader("2. Salubridad Emocional e Historial Individual")
        col3, col4 = st.columns(2)
        with col3:
            antecedentes = st.radio("¿Tienes antecedentes familiares de afecciones de salud mental?", ["Sí", "No", "No lo sé"], index=None)
            buscado_tratamiento = st.radio("¿Has buscado tratamiento profesional?", ["Sí", "No"], index=None)
        with col4:
            condicion_actual = st.radio("Actualmente, ¿consideras que tienes una condición de salud mental?", ["Sí", "No", "Tal vez / No lo sé"], index=None)

        st.markdown("---")
        
        st.subheader("3. Percepción del Entorno Laboral y Beneficios")
        col5, col6 = st.columns(2)
        with col5:
            beneficios = st.radio("¿Tu empresa ofrece beneficios explícitos para salud mental?", ["Sí", "No", "No lo sé"], index=None)
            privacidad = st.radio("¿Tu empleador protege la privacidad si buscas tratamiento?", ["Sí", "No", "No lo sé"], index=None)
        with col6:
            cobertura = st.radio("¿Conoces los detalles de la cobertura de salud mental ofrecida?", ["Sí", "No", "No aplica"], index=None)
        
        st.markdown("<br>", unsafe_allow_html=True)
        imp_mental = st.slider("Importancia que tu empresa le da a la Salud Mental (1-10)", 1, 10, 5)
        imp_fisica = st.slider("Importancia que tu empresa le da a la Salud Física (1-10)", 1, 10, 5)

        
        enviado = st.form_submit_button("💜 Enviar Encuesta", use_container_width=True)

    if enviado:
        campos_faltantes = (
            edad is None or genero is None or facultad is None or area_tech is None or rol is None or 
            empresa_tech is None or antecedentes is None or buscado_tratamiento is None or 
            condicion_actual is None or beneficios is None or privacidad is None or cobertura is None)

        if campos_faltantes:
            st.warning("⚠️ Por favor, completa todas las preguntas antes de enviar la encuesta.")
        else:
            datos = {
                "p_edad": edad, "p_genero": genero, "p_facultad": facultad, "p_area": area_tech,
                "p_rol": 1 if rol == "Sí" else 0, "p_emp": 1 if empresa_tech == "Sí" else 0, 
                "p_ant": antecedentes, "p_trat": 1 if buscado_tratamiento == "Sí" else 0,
                "p_cond": condicion_actual, "p_ben": beneficios, "p_priv": privacidad,
                "p_cob": cobertura, "p_imp_m": imp_mental, "p_imp_f": imp_fisica
            }
            
            query = text("""
                INSERT INTO public.estudiante (
                    edad, genero, facultad_estudio, area_tecnologica, rol_especifico,
                    empresa_puramente_tecnologia, antecedentes_familiares, 
                    buscado_tratamiento, condicion_actual,
                    beneficios_empresa, privacidad_tratamiento, conoce_cobertura,
                    importancia_salud_mental_empresa, importancia_salud_fisica_empresa
                ) VALUES (
                    :p_edad, :p_genero, :p_facultad, 
                    :p_area, :p_rol, :p_emp,
                    :p_ant, :p_trat, :p_cond,
                    :p_ben, :p_priv, :p_cob,
                    :p_imp_m, :p_imp_f
                )
            """)
            
            try:
                with engine.begin() as con:
                    con.execute(query, datos)
                
                st.session_state.datos_prompt = (
                    f"Edad: {edad}, Género: {genero}, Facultad: {facultad}, Área: {area_tech}, "
                    f"Rol TI: {rol}, Empresa Tech: {empresa_tech}, Antecedentes: {antecedentes}, "
                    f"Buscó tratamiento: {buscado_tratamiento}, Condición actual: {condicion_actual}, "
                    f"Beneficios: {beneficios}, Privacidad: {privacidad}, Cobertura: {cobertura}, "
                    f"Importancia Mental: {imp_mental}/10, Importancia Física: {imp_fisica}/10"
                )
                st.session_state.encuesta_enviada = True
                st.rerun()

            except Exception as e:
                st.error(f"Error al enviar la encuesta: {e}")

else:
    st.success("¡Tus respuestas se han guardado exitosamente en nuestra base de datos!")
    st.balloons()

    st.subheader("💜 Recomendación de tu Consejero Virtual")
    with st.container(border=True):
        if st.session_state.consejo_ia is None:
            try:
                with st.spinner("Cargando Consejo Perzonalizado..."):
                  st.session_state.consejo_ia = st.write_stream(
                    pedir_consejo_ia(st.session_state.datos_prompt)
                 )
            except Exception: # as e:
               st.warning("No se pudo cargar la recomendación en este momento.") #st.error(e)
        else:
            st.markdown(st.session_state.consejo_ia)

    st.markdown("""
        <div class="mensaje-motivacional">
            <h3 style="margin-top: 0; color: #3C096C;">💜 ¡Muchas gracias por tu participación!</h3>
            <p style="font-size: 1.05rem; color: #2b2b2b;">
                Tu contribución es fundamental para generar conciencia, visibilizar el bienestar emocional 
                y promover culturas de trabajo más saludables e inclusivas en el sector tecnológico.
            </p>
            <blockquote style="border-left: 3px solid #7B2CBF; padding-left: 10px; font-style: italic; color: #5a189a; margin-top: 10px;">
                "Cuidar de tu salud mental no es un lujo, es una prioridad. Tómate una pausa cuando lo necesites." 🌿✨
            </blockquote>
        </div>
    """, unsafe_allow_html=True)