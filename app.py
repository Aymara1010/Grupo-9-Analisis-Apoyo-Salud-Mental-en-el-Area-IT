import base64
from pathlib import Path
import duckdb
import streamlit as st

# Configuración de la App
st.set_page_config(page_title="Análisis Salud Mental", page_icon="🧠", layout="wide")

# Preparación del Caché
@st.cache_resource(show_spinner=False)
def iniciar_conexion():
    md_token = st.secrets["MOTHERDUCK_TOKEN"]
    return duckdb.connect(f"md:?motherduck_token={md_token}")

@st.cache_data(ttl=3600, show_spinner=False)
def preload_data():
    conn = iniciar_conexion()
    conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Uno").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Dos").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Tres").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cuatro").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cinco").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Seis").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Pregunta_Uno").fetchdf()
    conn.execute("SELECT * FROM modelo_dimensional.Pregunta_Cuatro").fetchdf()
   
with st.spinner("Conectando la Base de Datos..."):   
    preload_data()


#Detalles del menú y degradado de fondos

# --- Pato motivador en el índice lateral ---
FRASES_PATO = [
    "🦆 Vas súper bien, sigue avanzando paso a paso.",
    "✨ No tienes que resolver tu vida hoy, solo llegar a mañana",
    "💧 Pausa para agua: los buenos datos también necesitan mente fresca.",
    "🚀 Lo difícil ya lo estás resolviendo; ya vas en buen camino.",
    "💜 Cada ajuste te acerca a la meta.",
    "🧠 Si algo no cuadra a la primera, se revisa y se acomoda.",
    "🌟 ¡Ánimo! Ya casi tienes todo listo para lucir el proyecto.",
    "🔥 Constancia mata prisa. ¡Tú puedes con esto!",
]

def _gif_a_base64(ruta_gif: str) -> str | None:
  archivo = Path(ruta_gif)
  if not archivo.exists():
    return None
  return base64.b64encode(archivo.read_bytes()).decode("utf-8")


def mostrar_pato_sidebar(ruta_gif: str = "assets/pato_muneco.gif"):
  if "indice_frase_pato" not in st.session_state:
    st.session_state["indice_frase_pato"] = 0
  if "burbuja_pato_abierta" not in st.session_state:
    st.session_state["burbuja_pato_abierta"] = False

  gif_b64 = _gif_a_base64(ruta_gif)

  st.markdown("---")
  st.markdown(
      """
        <style>
        .pato-sidebar-card {
            background: linear-gradient(145deg, #F8F4FF 0%, #EDE2FF 100%);
            border-left: 5px solid #7B2CBF;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
            text-align: center;
            box-shadow: 0 6px 14px rgba(60, 9, 108, 0.14);
            color: #1a1025;
        }
        .pato-sidebar-avatar {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto 8px auto;
            border: 2px solid #7B2CBF;
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
        }
        .pato-sidebar-avatar img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .pato-sidebar-frase {
            font-size: 0.85rem;
            line-height: 1.35;
            margin-top: 6px;
        }
        </style>
        """,
      unsafe_allow_html=True,
  )

  if gif_b64:
    avatar_html = f'<div class="pato-sidebar-avatar"><img src="data:image/gif;base64,{gif_b64}" alt="Pato motivador"></div>'
  else:
    avatar_html = '<div class="pato-sidebar-avatar">🦆</div>'

  frase_html = ""
  if st.session_state["burbuja_pato_abierta"]:
    frase_actual = FRASES_PATO[st.session_state["indice_frase_pato"]]
    frase_html = f'<div class="pato-sidebar-frase">{frase_actual}</div>'

  st.markdown(
      f"""
        <div class="pato-sidebar-card">
            {avatar_html}
            <b>Pato TechWell</b>
            {frase_html}
        </div>
        """,
      unsafe_allow_html=True,
  )

  etiqueta_btn = (
      "🦆 Otra frase"
      if st.session_state["burbuja_pato_abierta"]
      else "🦆 ¡Apriétame!"
  )
  if st.button(etiqueta_btn, key="btn_pato_sidebar", use_container_width=True):
    if st.session_state["burbuja_pato_abierta"]:
      st.session_state["indice_frase_pato"] = (
          st.session_state["indice_frase_pato"] + 1
      ) % len(FRASES_PATO)
    else:
      st.session_state["burbuja_pato_abierta"] = True
    st.rerun()

st.markdown( 
  ""
    """
    <style>
    /* Degradado de fondo */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #EFBDEB 30%, #B68CB8 40%, #6461A0 60%) !important;
    }
    /* Borde lateral  */
    [data-testid="stSidebar"] {
        border-right: 3px solid #6461A0;
    }  
    /* Estilo para los botones del menú */
    a[data-testid="stPageLink-NavLink"] {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        transition: background-color 0.3s ease;
    }
    /* Estilo cuando el mouse pasa por encima o la página está activa */
    a[data-testid="stPageLink-NavLink"]:hover, 
    a[data-testid="stPageLink-NavLink"][aria-current="page"] {
        background-color: rgba(226, 183, 20, 0.15) !important;
        border: 1px solid #E88EED !important;
        color: #E88EED !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#Definición de las paginas
p_welcom = st.Page("Paginas/08_Welcome.py", title="Bienvenida")
p_vista = st.Page("Paginas/01_Inicio.py", title="Vista General")

p_plant = st.Page("Paginas/02_Planteamiento.py", title="Lectura General ")
p_teorico = st.Page("Paginas/03_Marco_Teorico.py", title="Metodología")
p_metodo = st.Page("Paginas/04_Marco_Metodologico.py", title="Diccionario de Datos")

p_resultados = st.Page("Paginas/05_Resultados_y_Conclusiones.py", title="Resultados y Conclusiones")
p_querys_prof = st.Page("Paginas/09_querys_prof.py", title="Querys Generales")
p_bibli = st.Page("Paginas/10_Bibliografia.py", title="Bibliografía")
p_encuesta = st.Page("Paginas/12_Encuesta.py", title="📝 Llenar Encuesta")

todas_las_paginas = [p_welcom, p_vista, p_plant, p_teorico, p_metodo, p_resultados, p_querys_prof, p_bibli, p_encuesta]
pg = st.navigation(todas_las_paginas, position="hidden")

# Texto y Orden del menú
with st.sidebar:  #avisos y notas
    st.markdown("# TechWell Analítica 💻 ")
    mostrar_pato_sidebar()
    st.markdown("---")
    #cuadros para seleccionar 
    #inicio
    with st.expander("🚀 **inicio**", expanded=True):
        st.page_link(p_welcom)
        st.page_link(p_vista)

    #Presentación Académica
    with st.expander("📖 **Presentación Académica**", expanded=True):
        st.page_link(p_plant)
        st.page_link(p_teorico)
        st.page_link(p_metodo)
    
    #Análisis y Cierre
    with st.expander("📊 **Análisis**", expanded=True):
        st.page_link(p_resultados)
        st.page_link(p_querys_prof)
        st.page_link(p_bibli)
        
    with st.expander("📝 **Participación**", expanded=True):
        st.page_link(p_encuesta)


pg.run()