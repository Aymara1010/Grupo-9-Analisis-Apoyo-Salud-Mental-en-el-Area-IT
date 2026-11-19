import streamlit as st
import plotly.graph_objects as go
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

# Etiqueta principal y descarga de reporte CSV
st.title("Resultados y Conclusiones")

resumen_objs = [
    (
        "Objetivo 1",
        "Comparación de frecuencia de beneficios de salud mental por región",
        (
            "Comparar la frecuencia relativa de empresas tecnológicas que ofrecen"
            " beneficios de salud mental entre Estados Unidos, Europa y"
            " Oceanía."
        ),
        (
            "El análisis de la distribución porcentual indica que Estados"
            " Unidos concentra el mayor porcentaje de respuestas afirmativas."
        ),
    ),
    (
        "Objetivo 2",
        "Proporción de empleados que conocen sus opciones de atención",
        (
            "Determinar la proporción de empleados que conocen sus opciones de"
            " atención de salud mental laboral según su región geográfica."
        ),
        (
            "En Estados Unidos el conocimiento es cercano al 50.71%, mientras"
            " que en Europa y Oceanía el 73.98% desconoce sus opciones."
        ),
    ),
    (
        "Objetivo 3",
        (
            "Promedio y dispersión de la importancia otorgada por categoría de"
            " puesto"
        ),
        (
            "Calcular y comparar el puntaje promedio y la dispersión de la"
            " importancia que los empleadores otorgan a la salud mental por"
            " categoría de puesto."
        ),
        (
            "Los puntajes promedio oscilan entre 4.93 y 6.09, con mayor"
            " dispersión en subgrupos de menor tamaño muestral."
        ),
    ),
    (
        "Objetivo 4",
        "Distribución de frecuencias de la calificación del apoyo general",
        (
            "Evaluar la percepción de los empleados sobre el respaldo de la"
            " industria tecnológica según su zona geográfica."
        ),
        (
            "Las respuestas se concentran en los niveles intermedios de la"
            " escala en ambas regiones."
        ),
    ),
]

df_reporte = pd.DataFrame(
    resumen_objs, columns=["Objetivo", "Titulo", "Descripcion", "Conclusion"]
)

st.download_button(
    label="Descargar reporte CSV",
    data=df_reporte.to_csv(index=False).encode("utf-8"),
    file_name="reporte_resultados_conclusiones.csv",
    mime="text/csv",
)

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

# OBJETIVO 3
def preparar_df3(df_raw: pd.DataFrame):
  df_work = df_raw.copy()

  col_puesto = (
      "Perfil_Tecnologico"
      if "Perfil_Tecnologico" in df_work.columns
      else "Categoria_Puesto"
  )
  col_region = "Region" if "Region" in df_work.columns else "Region_Agrupada"

  tiene_microdatos = "Prioridad_Salud_Mental" in df_work.columns

  if tiene_microdatos:
    df_work["Prioridad_Salud_Mental"] = pd.to_numeric(
        df_work["Prioridad_Salud_Mental"], errors="coerce"
    )
    df_work = df_work.dropna(
        subset=[col_puesto, col_region, "Prioridad_Salud_Mental"]
    )
    df_resumen = df_work.groupby(
        [col_puesto, col_region], as_index=False
    ).agg(
        Promedio_Prioridad=("Prioridad_Salud_Mental", "mean"),
        Dispersion_Prioridad=("Prioridad_Salud_Mental", "std"),
        N_Muestra=("Prioridad_Salud_Mental", "count"),
    )
    df_resumen["Dispersion_Prioridad"] = df_resumen[
        "Dispersion_Prioridad"
    ].fillna(0.0)
  else:
    df_resumen = df_work.copy()
    if "Dispersion_Prioridad" not in df_resumen.columns:
      df_resumen["Dispersion_Prioridad"] = 0.0
    if "N_Muestra" not in df_resumen.columns:
      df_resumen["N_Muestra"] = pd.NA

  return df_work, df_resumen, col_puesto, col_region, tiene_microdatos


df3_micro, df3_resumen, col_puesto_3, col_region_3, es_micro_3 = preparar_df3(df3)

titulo_obj3 = (
    "Promedio y dispersión de la importancia otorgada por categoría de puesto"
)
desc_obj3 = (
    "Calcular y comparar el puntaje promedio y la dispersión de la importancia"
    " que los empleadores otorgan a la salud mental por categoría de puesto."
)
concl_obj3 = (
    "El análisis estadístico descriptivo muestra que los puntajes promedio de"
    " prioridad se sitúan en rangos intermedios (oscilando entre 4.93 y 6.09)."
    " No obstante, la evaluación de la variabilidad debe interpretarse a la"
    " luz del tamaño muestral (<i>n</i>): mientras que las categorías con"
    " mayor representación poblacional muestran estimaciones robustas y"
    " homogéneas entre regiones, los subgrupos con menor frecuencia de"
    " respuesta (especialmente <i>n</i>=11 en Europa y Oceanía) presentan una"
    " mayor vulnerabilidad a la dispersión, lo que evidencia que la"
    " percepción de la prioridad corporativa se consolida con mayor"
    " estabilidad en los roles con mayor densidad de datos."
)

with st.expander(f"📌 Objetivo 3: {titulo_obj3}", expanded=False):
  st.markdown(
      f"""
        <div class="tarjeta-objetivo">
            <h3 class="titulo-obj">Descripción del Objetivo</h3>
            <p class="texto-obj">{desc_obj3}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  tab3_1, tab3_2, tab3_3 = st.tabs([
      "📊 1. Panorama de Promedios",
      "📦 2. Radiografía de Dispersión",
      "🔗 3. Brecha Regional",
  ])

  with tab3_1:
    with st.container(border=True):
      fig3_1 = px.bar(
          df3_resumen,
          x=col_puesto_3,
          y="Promedio_Prioridad",
          color=col_region_3,
          barmode="group",
          text="Promedio_Prioridad",
          color_discrete_sequence=["#3C096C", "#7B2CBF", "#C77DFF"],
          labels={
              col_puesto_3: "Categoría de Puesto",
              "Promedio_Prioridad": "Puntaje Promedio de Prioridad",
              col_region_3: "Región",
          },
      )
      fig3_1.update_traces(
          texttemplate="%{text:.2f}",
          textposition="outside",
          textfont=dict(color="black", size=11, weight="bold"),
      )
      fig3_1.update_layout(
          title=dict(
              text=(
                  "<b>1. Puntaje Promedio de Prioridad por Categoría de"
                  " Puesto</b>"
              ),
              font=dict(color="black", size=15),
          ),
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="sans-serif", color="black", size=12),
          xaxis=dict(
              showgrid=False,
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          yaxis=dict(
              showgrid=True,
              gridcolor="rgba(123, 44, 191, 0.12)",
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          legend=dict(
              font=dict(color="black"),
              title=dict(font=dict(color="black")),
          ),
      )
      st.plotly_chart(fig3_1, use_container_width=True, key="g_obj3_1")

  with tab3_2:
    with st.container(border=True):
      if es_micro_3:
        fig3_2 = px.box(
            df3_micro,
            x=col_puesto_3,
            y="Prioridad_Salud_Mental",
            color=col_region_3,
            points="outliers",
            color_discrete_sequence=["#3C096C", "#7B2CBF", "#E0AAFF"],
            labels={
                col_puesto_3: "Categoría de Puesto",
                "Prioridad_Salud_Mental": "Prioridad Salud Mental",
                col_region_3: "Región",
            },
        )
        titulo_g2 = (
            "<b>2. Distribución y Dispersión (Caja y Bigotes) por Categoría de"
            " Puesto</b>"
        )
        y_label_g2 = "Prioridad Salud Mental"
      else:
        fig3_2 = px.bar(
            df3_resumen,
            x=col_puesto_3,
            y="Dispersion_Prioridad",
            color=col_region_3,
            barmode="group",
            text="Dispersion_Prioridad",
            color_discrete_sequence=["#5A189A", "#9D4EDD", "#E0AAFF"],
            labels={
                col_puesto_3: "Categoría de Puesto",
                "Dispersion_Prioridad": "Dispersión de Prioridad",
                col_region_3: "Región",
            },
        )
        fig3_2.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(color="black", size=11, weight="bold"),
        )
        titulo_g2 = "<b>2. Dispersión de Prioridad por Categoría de Puesto</b>"
        y_label_g2 = "Dispersión de Prioridad"

      fig3_2.update_layout(
          title=dict(text=titulo_g2, font=dict(color="black", size=15)),
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="sans-serif", color="black", size=12),
          xaxis=dict(
              showgrid=False,
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          yaxis=dict(
              title=dict(text=y_label_g2, font=dict(color="black")),
              showgrid=True,
              gridcolor="rgba(123, 44, 191, 0.12)",
              tickfont=dict(color="black"),
          ),
          legend=dict(
              font=dict(color="black"),
              title=dict(font=dict(color="black")),
          ),
      )
      st.plotly_chart(fig3_2, use_container_width=True, key="g_obj3_2")

  with tab3_3:
    with st.container(border=True):
      df3_piv = df3_resumen.pivot_table(
          index=col_puesto_3,
          columns=col_region_3,
          values="Promedio_Prioridad",
          aggfunc="mean",
      ).reset_index()

      regiones_3 = [c for c in df3_piv.columns if c != col_puesto_3]
      fig3_3 = go.Figure()

      if len(regiones_3) >= 2:
        r1, r2 = regiones_3[0], regiones_3[1]
        for _, fila in df3_piv.iterrows():
          if pd.notna(fila[r1]) and pd.notna(fila[r2]):
            fig3_3.add_trace(
                go.Scatter(
                    x=[fila[r1], fila[r2]],
                    y=[fila[col_puesto_3], fila[col_puesto_3]],
                    mode="lines",
                    line=dict(color="#C77DFF", width=3),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

      colores_puntos = ["#3C096C", "#7B2CBF", "#9D4EDD"]
      for idx, reg in enumerate(regiones_3):
        fig3_3.add_trace(
            go.Scatter(
                x=df3_piv[reg],
                y=df3_piv[col_puesto_3],
                mode="markers+text",
                name=str(reg),
                text=[f"{v:.2f}" if pd.notna(v) else "" for v in df3_piv[reg]],
                textposition="top center",
                textfont=dict(color="black", size=11, weight="bold"),
                marker=dict(
                    size=13,
                    color=colores_puntos[idx % len(colores_puntos)],
                    line=dict(color="white", width=1.5),
                ),
            )
        )

      fig3_3.update_layout(
          title=dict(
              text=(
                  "<b>3. Brecha Regional en el Puntaje Promedio por Categoría de"
                  " Puesto</b>"
              ),
              font=dict(color="black", size=15),
          ),
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="sans-serif", color="black", size=12),
          xaxis=dict(
              title=dict(text="Puntaje Promedio", font=dict(color="black")),
              tickfont=dict(color="black"),
              showgrid=True,
              gridcolor="rgba(123, 44, 191, 0.12)",
          ),
          yaxis=dict(
              title=dict(text="Categoría de Puesto", font=dict(color="black")),
              tickfont=dict(color="black"),
              showgrid=False,
          ),
          legend=dict(
              font=dict(color="black"),
              title=dict(text="Región", font=dict(color="black")),
          ),
          height=420,
      )
      st.plotly_chart(fig3_3, use_container_width=True, key="g_obj3_3")

  st.markdown(
      f"""
        <div class="tarjeta-kpi">
            <div class="titulo-kpi">💡 Conclusión Específica</div>
            <p class="texto-kpi">{concl_obj3}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

#  OBJETIVO 4 

fig4 = px.bar(
    df4, x='Calificacion_Apoyo', y='Porcentaje_Concentracion', color='Region_Agrupada',
    barmode='group', text='Porcentaje_Concentracion',
    color_discrete_sequence=['#3C096C', '#7B2CBF'],
    labels={'Calificacion_Apoyo': 'Calificación de Apoyo', 'Porcentaje_Concentracion': 'Frecuencia Relativa (%)', 'Region_Agrupada': 'Región'}
)

estilizar_grafico(
    fig4,
    titulo="Distribución de Frecuencias de la Calificación del Apoyo Tecnológico",
    formato_texto='.1f',
    es_porcentaje=True
)

renderizar_bloque(
    4, "Distribución de frecuencias de la calificación del apoyo general",
    "Evaluar la percepción de los empleados sobre el respaldo de la industria tecnológica, comparando las tendencias y concentraciones de respuestas según su zona geográfica.",
    "El análisis de la distribución de frecuencias revela una concentración de respuestas en los niveles intermedios y favorables de la escala de respaldo. Al contrastar las regiones, se observa que tanto en Estados Unidos como en Europa y Oceanía las modas tienden hacia valoraciones similares, reflejando una percepción compartida sobre el compromiso general de la industria, aunque con sutiles variaciones en la densidad de las calificaciones extremas.",
    fig4, "g_obj4"
)

# OBJETIVO 5
titulo_obj5 = "Promedio y dispersión de prioridad por región"
desc_obj5 = (
    "Comparar el puntaje promedio de prioridad, su dispersión y el total de"
    " respuestas entre <b>Europa y Oceanía</b> y <b>USA</b>."
)
concl_obj5 = (
    "El promedio de prioridad es muy cercano entre regiones: <b>5.04</b> en"
    " <b>Europa y Oceanía</b> y <b>4.99</b> en <b>USA</b>. La dispersión"
    " también es similar (<b>2.22</b> en <b>Europa y Oceanía</b> frente a"
    " <b>2.34</b> en <b>USA</b>), con un volumen de <b>346</b> respuestas en"
    " <b>Europa y Oceanía</b> y <b>1,021</b> respuestas en <b>USA</b>."
)

with st.expander(f"📌 Objetivo 5: {titulo_obj5}", expanded=False):
  st.markdown(
      f"""
        <div class="tarjeta-objetivo">
            <h3 class="titulo-obj">Descripción del Objetivo</h3>
            <p class="texto-obj">{desc_obj5}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  tab5_1, tab5_2, tab5_3 = st.tabs([
      "📊 1. Promedio de Prioridad",
      "📉 2. Dispersión",
      "👥 3. Total de Respuestas",
  ])

  with tab5_1:
    with st.container(border=True):
      fig5_prom = px.bar(
          df5,
          x="Region_Agrupada",
          y="Promedio_Prioridad",
          color="Region_Agrupada",
          text="Promedio_Prioridad",
          color_discrete_sequence=["#3C096C", "#7B2CBF"],
          labels={
              "Region_Agrupada": "Región",
              "Promedio_Prioridad": "Promedio de Prioridad",
          },
      )
      fig5_prom.update_traces(
          texttemplate="%{text:.2f}",
          textposition="outside",
          textfont=dict(color="black", size=11, weight="bold"),
      )
      fig5_prom.update_layout(
          title=dict(
              text="<b>1. Promedio de Prioridad por Región</b>",
              font=dict(color="black", size=15),
          ),
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="sans-serif", color="black", size=12),
          xaxis=dict(
              showgrid=False,
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          yaxis=dict(
              showgrid=True,
              gridcolor="rgba(123, 44, 191, 0.12)",
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          legend=dict(
              font=dict(color="black"),
              title=dict(font=dict(color="black")),
          ),
      )
      st.plotly_chart(fig5_prom, use_container_width=True, key="g_obj5_1")

  with tab5_2:
    with st.container(border=True):
      fig5_disp = px.bar(
          df5,
          x="Region_Agrupada",
          y="Dispersion_Prioridad",
          color="Region_Agrupada",
          text="Dispersion_Prioridad",
          color_discrete_sequence=["#7B2CBF", "#C77DFF"],
          labels={
              "Region_Agrupada": "Región",
              "Dispersion_Prioridad": "Dispersión de Prioridad",
          },
      )
      fig5_disp.update_traces(
          texttemplate="%{text:.2f}",
          textposition="outside",
          textfont=dict(color="black", size=11, weight="bold"),
      )
      fig5_disp.update_layout(
          title=dict(
              text="<b>2. Dispersión de Prioridad por Región</b>",
              font=dict(color="black", size=15),
          ),
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="sans-serif", color="black", size=12),
          xaxis=dict(
              showgrid=False,
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          yaxis=dict(
              showgrid=True,
              gridcolor="rgba(123, 44, 191, 0.12)",
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          legend=dict(
              font=dict(color="black"),
              title=dict(font=dict(color="black")),
          ),
      )
      st.plotly_chart(fig5_disp, use_container_width=True, key="g_obj5_2")

  with tab5_3:
    with st.container(border=True):
      fig5_resp = px.bar(
          df5,
          x="Region_Agrupada",
          y="Total_Respuestas",
          color="Region_Agrupada",
          text="Total_Respuestas",
          color_discrete_sequence=["#5A189A", "#E0AAFF"],
          labels={
              "Region_Agrupada": "Región",
              "Total_Respuestas": "Total de Respuestas",
          },
      )
      fig5_resp.update_traces(
          texttemplate="%{text:,}",
          textposition="outside",
          textfont=dict(color="black", size=11, weight="bold"),
      )
      fig5_resp.update_layout(
          title=dict(
              text="<b>3. Total de Respuestas por Región</b>",
              font=dict(color="black", size=15),
          ),
          plot_bgcolor="rgba(0,0,0,0)",
          paper_bgcolor="rgba(0,0,0,0)",
          font=dict(family="sans-serif", color="black", size=12),
          xaxis=dict(
              showgrid=False,
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          yaxis=dict(
              showgrid=True,
              gridcolor="rgba(123, 44, 191, 0.12)",
              title_font=dict(color="black"),
              tickfont=dict(color="black"),
          ),
          legend=dict(
              font=dict(color="black"),
              title=dict(font=dict(color="black")),
          ),
      )
      st.plotly_chart(fig5_resp, use_container_width=True, key="g_obj5_3")

  st.markdown(
      f"""
        <div class="tarjeta-kpi">
            <div class="titulo-kpi">💡 Conclusión Específica</div>
            <p class="texto-kpi">{concl_obj5}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # OBJETIVO 6
titulo_obj6 = (
    "Necesidades y beneficios de salud mental en la industria tecnológica"
)
desc_obj6 = (
    "Identificar y comparar las categorías de sugerencias, su detalle, total"
    " de menciones y porcentaje por región entre <b>Europa y Oceanía</b> y"
    " <b>USA</b>."
)
concl_obj6 = (
    "Las categorías y el detalle de cada sugerencia permiten contrastar las"
    " demandas registradas en <b>Europa y Oceanía</b> y <b>USA</b> según su"
    " peso porcentual y número de menciones (por ejemplo,"
    " <b>Desestigmatización y Cultura Abierta</b>, <b>Jornada, Carga Laboral"
    " y Burnout</b>, <b>Educación, Difusión y Espacio Físico</b>,"
    " <b>Capacitación a Líderes y RRHH</b>, <b>Días de Salud Mental y"
    " Licencias</b> y <b>Seguros, Beneficios y Cobertura</b>), apoyándose en"
    " la tabla de detalle para revisar cada propuesta."
)

df6_plot = df6.copy()

if "Porcentaje_Region" in df6_plot.columns and "Region" in df6_plot.columns:
  df6_plot = df6_plot.sort_values(
      ["Region", "Porcentaje_Region"], ascending=[True, False]
  )

hover_cols_6 = [
    c for c in ["Detalle_Categoria", "Total_Menciones"] if c in df6_plot.columns
]

fig6 = px.bar(
    df6_plot,
    x="Categoria_Sugerencia",
    y="Porcentaje_Region",
    color="Region",
    barmode="group",
    text="Porcentaje_Region",
    hover_data=hover_cols_6,
    color_discrete_sequence=["#3C096C", "#7B2CBF"],
    labels={
        "Categoria_Sugerencia": "Categoría de Demanda / Sugerencia",
        "Porcentaje_Region": "Peso en la Región (%)",
        "Region": "Región",
        "Detalle_Categoria": "Detalle de la Propuesta",
        "Total_Menciones": "Total de Menciones",
    },
)

estilizar_grafico(
    fig6,
    titulo="Priorización de Demandas y Propuestas de Mejora por Región (%)",
    formato_texto=".1f",
    es_porcentaje=True,
)

fig6.update_layout(
    xaxis=dict(tickangle=-20),
    height=470,
)

with st.expander(f"📌 Objetivo 6: {titulo_obj6}", expanded=False):
  st.markdown(
      f"""
        <div class="tarjeta-objetivo">
            <h3 class="titulo-obj">Descripción del Objetivo</h3>
            <p class="texto-obj">{desc_obj6}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  with st.container(border=True):
    st.plotly_chart(fig6, use_container_width=True, key="g_obj6")

  cols_tabla_6 = [
      c
      for c in [
          "Region",
          "Categoria_Sugerencia",
          "Detalle_Categoria",
          "Total_Menciones",
          "Porcentaje_Region",
      ]
      if c in df6_plot.columns
  ]
  if cols_tabla_6:
    st.dataframe(
        df6_plot[cols_tabla_6],
        use_container_width=True,
        hide_index=True,
    )
  st.markdown(
      f"""
        <div class="tarjeta-kpi">
            <div class="titulo-kpi">💡 Conclusión Específica</div>
            <p class="texto-kpi">{concl_obj6}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )