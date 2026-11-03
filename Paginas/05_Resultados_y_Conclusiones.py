import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

#1. estilo general pag
st.markdown("""
<style>
.tarjeta-objetivo, .tarjeta-kpi {
    border-radius: 10px;
    padding: 15px 20px;
    font-family: sans-serif;
    color: black;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08);
}
.tarjeta-objetivo {
    background-color: #F8F4FF;
    border-left: 8px solid #3C096C;
}
.tarjeta-kpi {
    background-color: #F8F4FF; 
    border-left: 6px solid #7B2CBF; 
}
.titulo-obj {
    font-size: 20px;
    font-weight: bold;
    margin: 0;
    color: #3C096C;
}
.texto-obj, .texto-kpi {
    font-size: 15px;
    margin: 6px 0 0 0;
    line-height: 1.4;
}
.titulo-kpi {
    font-size: 13px;
    font-weight: bold;
    color: #3C096C;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# 2 conexion motherduck
md_token = st.secrets["MOTHERDUCK_TOKEN"]
conn = duckdb.connect(f"md:?motherduck_token={md_token}")

#carga de los datos desde mama pato 
df1 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Uno").fetchdf()
df2 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Dos").fetchdf()
df3 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Tres").fetchdf()
df4 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cuatro").fetchdf()
df5 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Cinco").fetchdf()
df6 = conn.execute("SELECT * FROM modelo_dimensional.Objetivo_Seis").fetchdf()

#renderizado de los objetivos
def renderizar_bloque(numero, titulo_obj, texto_desc, texto_concl, figura, key_fig):
    with st.expander(f"📌 Objetivo {numero}: {titulo_obj}", expanded=(numero==1)):
        st.markdown(f"""
        <div class="tarjeta-objetivo">
            <h3 class="titulo-obj">Descripción del Objetivo</h3>
            <p class="texto-obj">{texto_desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.plotly_chart(figura, use_container_width=True, key=key_fig)
            
        st.markdown(f"""
        <div class="tarjeta-kpi">
            <div class="titulo-kpi">💡 Conclusión Específica</div>
            <p class="texto-kpi">{texto_concl}</p>
        </div>
        """, unsafe_allow_html=True)