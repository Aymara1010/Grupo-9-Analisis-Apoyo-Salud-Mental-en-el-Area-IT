import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

def estilizar_grafico(fig, titulo, formato_texto='.1f', es_porcentaje=True):
    """funcion para graficos colores de letras"""
    formato = f'%{{text:{formato_texto}}}{"%" if es_porcentaje else ""}'
    
    fig.update_traces(
        texttemplate=formato,
        textposition='outside',
        textfont=dict(color='black', size=11, weight='bold')
    )
    
    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", font=dict(color="black", size=16)),
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="sans-serif", color="black", size=12),
        xaxis=dict(showgrid=False, title_font=dict(color="black"), tickfont=dict(color="black")),
        yaxis=dict(showgrid=True, gridcolor='rgba(123, 44, 191, 0.1)', title_font=dict(color="black"), tickfont=dict(color="black")),
        legend=dict(font=dict(color="black"), title=dict(font=dict(color="black")))
    )
    return fig

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

# OBJETIVO 1
fig1 = px.bar(
    df1, x='region_agrupada', y='Frecuencia_Relativa_Porcentaje', color='Ofrece_Beneficios',
    barmode='group', text='Frecuencia_Relativa_Porcentaje',
    color_discrete_sequence=['#7B2CBF', '#c77dff', '#E0AAFF', '#3C096C', '#5a189a'],
    labels={'region_agrupada': 'Región', 'Frecuencia_Relativa_Porcentaje': 'Frecuencia Relativa (%)', 'Ofrece_Beneficios': 'Ofrece Beneficios'}
)

estilizar_grafico(
    fig1, 
    titulo="Frecuencia Relativa de Empresas Tecnológicas con Beneficios de Salud Mental", 
    formato_texto='.1f', 
    es_porcentaje=True
)

renderizar_bloque(
    1, "Comparación de frecuencia de beneficios de salud mental por región",
    "Comparar la frecuencia relativa de empresas tecnológicas que ofrecen beneficios de salud mental entre Estados Unidos, Europa y Oceanía.",
    "El análisis de la distribución porcentual indica que <b>Estados Unidos</b> concentra el mayor porcentaje de respuestas afirmativas en la provisión de beneficios de salud mental. En contraste, el bloque de <b>Europa y Oceanía</b> exhibe una mayor dispersión relativa entre las categorías de respuesta ('Sí', 'No' y 'No lo sé'), lo que evidencia divergencias estructurales significativas en las políticas corporativas de asistencia según la delimitación geográfica.",
    fig1, "g_obj1"
)

#OBJETIVO 2
df2_melted = df2.melt(id_vars=['Region_Agrupada', 'Total_Respuestas_Definitivas'], 
                      value_vars=['Proporcion_SI_PCT', 'Proporcion_NO_PCT'],
                      var_name='Respuesta', value_name='Porcentaje')
df2_melted['Respuesta'] = df2_melted['Respuesta'].replace({'Proporcion_SI_PCT': 'Sí conoce', 'Proporcion_NO_PCT': 'No conoce'})

fig2 = px.bar(
    df2_melted, x='Region_Agrupada', y='Porcentaje', color='Respuesta',
    barmode='group', text='Porcentaje',
    color_discrete_map={'Sí conoce': '#7B2CBF', 'No conoce': '#E0AAFF'},
    labels={'Region_Agrupada': 'Región', 'Porcentaje': 'Proporción (%)'}
)

estilizar_grafico(
    fig2,
    titulo="Proporción de Empleados que Conocen sus Opciones de Cobertura",
    formato_texto='.1f',
    es_porcentaje=True
)

renderizar_bloque(
    2, "Proporción de empleados que conocen sus opciones de atención",
    "Determinar la proporción de empleados que conocen sus opciones de atención de salud mental laboral según su región geográfica.",
    "El análisis comparativo de proporciones evidencia un contraste estructural profundo entre regiones. En <b>Estados Unidos</b>, el conocimiento de las opciones de cobertura se encuentra distribuido de forma equitativa (50.71% afirma conocerlas frente a un 49.29% que las desconoce). En marcado contraste, el bloque de <b>Europa y Oceanía</b> muestra un déficit crítico de información, donde el <b>73.98%</b> de los empleados ignora sus alternativas de atención, lo que subraya la urgencia de optimizar los canales de comunicación y transparencia corporativa en dicha zona geográfica.",
    fig2, "g_obj2"
)

# --- OBJETIVO 3 ---
fig3 = px.bar(
    df3, x='Categoria_Puesto', y='Promedio_Prioridad', color='Region_Agrupada',
    barmode='group', error_y='Dispersion_Prioridad', text='Promedio_Prioridad',
    color_discrete_sequence=['#3C096C', '#7B2CBF'],
    labels={'Categoria_Puesto': 'Categoría de Puesto', 'Promedio_Prioridad': 'Promedio de Prioridad (Escala)'}
)

# Colocar el texto DENTRO de la barra con color blanco para evitar que la línea de error lo cruce
fig3.update_traces(
    texttemplate='%{text:.2f}',
    textposition='inside',
    insidetextanchor='start', # Esto coloca el texto en la base (parte baja) de la barra
    textfont=dict(color='white', size=12, weight='bold')
)

fig3.update_layout(
    title=dict(text="<b>Promedio y Dispersión de la Prioridad Otorgada por Categoría de Puesto</b>", font=dict(color="black", size=16)),
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="sans-serif", color="black", size=12),
    xaxis=dict(showgrid=False, title_font=dict(color="black"), tickfont=dict(color="black")),
    yaxis=dict(showgrid=True, gridcolor='rgba(123, 44, 191, 0.1)', title_font=dict(color="black"), tickfont=dict(color="black")),
    legend=dict(font=dict(color="black"), title=dict(font=dict(color="black")))
)

renderizar_bloque(
    3, "Promedio y dispersión de la importancia otorgada por categoría de puesto",
    "Calcular y comparar el puntaje promedio y la dispersión de la importancia que los empleadores otorgan a la salud mental por categoría de puesto.",
    "El análisis estadístico descriptivo muestra que los puntajes promedio de prioridad se sitúan en rangos intermedios (oscilando entre 4.93 y 6.09). No obstante, la evaluación de la variabilidad debe interpretarse a la luz del tamaño muestral (<i>n</i>): mientras que las categorías con mayor representación poblacional muestran estimaciones robustas y homogéneas entre regiones, los subgrupos con menor frecuencia de respuesta (especialmente <i>n</i>=11 en Europa y Oceanía) presentan una mayor vulnerabilidad a la dispersión, lo que evidencia que la percepción de la prioridad corporativa se consolida con mayor estabilidad en los roles con mayor densidad de datos.",
    fig3, "g_obj3"
)