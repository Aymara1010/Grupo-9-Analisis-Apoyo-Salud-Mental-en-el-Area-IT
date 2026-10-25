import streamlit as st
import plotly.express as px
# Aquí va página de los resultados (Analisis y Conclusiones)

# función para los querys
def run_query(query, ttl="1h"):
    conn = st.connection("motherduck", type="sql")
    return conn.query(query, ttl=ttl)

df=run_query(""" WITH Conteos AS (
    
    SELECT 
        CASE 
            WHEN dp.Pais IN ('Estados Unidos', 'United States', 'USA') THEN 'Estados Unidos'
            WHEN dp.Region IN ('Europa', 'Europe') THEN 'Europa'
            WHEN dp.Region IN ('Oceanía', 'Oceania') THEN 'Oceanía'
        END AS Region_Geografica,
        CASE 
            WHEN db.Beneficio IN ('Sí', 'Si', 'Yes') THEN 'Sí'
            WHEN db.Beneficio = 'No' THEN 'No'
        END AS Respuesta_Beneficio,
        COUNT(f.RespuestaID) AS Cantidad
    FROM Fact_Respuesta_Encuestado f
    JOIN Dim_Trabajo_Encuestado dt ON f.TrabajoID = dt.TrabajoID
    JOIN Dim_Beneficio_Trabajo db ON f.BeneficiosID = db.BeneficiosID
    JOIN Dim_Pais dp ON f.Pais_Empleo = dp.PaisID 
    WHERE dt.Empresa_Tec IN ('Sí', 'Si', 'Yes', '1') 
      AND db.Beneficio IN ('Sí', 'Si', 'Yes', 'No')
      AND (dp.Pais IN ('Estados Unidos', 'United States', 'USA') OR dp.Region IN ('Europa', 'Europe', 'Oceanía', 'Oceania'))
    GROUP BY 1, 2
),
Totales AS (
    
    SELECT Region_Geografica, SUM(Cantidad) AS Total_Region
    FROM Conteos
    GROUP BY Region_Geografica
)

SELECT 
    c.Region_Geografica,
    c.Respuesta_Beneficio,
    c.Cantidad AS Cantidad_Respuestas,
    t.Total_Region AS Total_Encuestados,
    ROUND((c.Cantidad * 100.0) / t.Total_Region, 2) AS Frecuencia_Relativa_Porcentaje
FROM Conteos c
JOIN Totales t ON c.Region_Geografica = t.Region_Geografica;""")


# titulo del objetivo
st.markdown("""
<style>
.tarjeta-objetivo {
    background-color: #F8F4FF;
    border-left: 8px solid #3C096C; 
    border-radius: 10px;
    padding: 15px 20px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    margin-bottom: 25px;
}
.titulo-obj {
    color: black;
    font-size: 22px;
    font-weight: bold;
    margin: 0;
    font-family: sans-serif;
}
.texto-obj {
    color: black;
    font-size: 16px;
    margin: 8px 0 0 0;
    font-family: sans-serif;
}
</style>

<div class="tarjeta-objetivo">
    <h2 class="titulo-obj">Objetivo 1</h2>
    <p class="texto-obj">Comparar la frecuencia relativa de empresas tecnológicas que ofrecen beneficios de salud mental entre Estados Unidos, Europa y Oceanía.</p>
</div>
""", unsafe_allow_html=True)


df['Region_con_N'] = df['Region_Geografica'] + "<br>(n=" + df['Total_Encuestados'].astype(str) + ")"


st.markdown("""
<style>
.tarjeta-kpi {
    background-color: #F8F4FF; 
    border-left: 6px solid #7B2CBF; 
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0px 8px 20px rgba(123, 44, 191, 0.15); 
    margin-bottom: 25px;
    font-family: sans-serif;
    color: black;
}
.titulo-kpi {
    font-size: 14px;
    font-weight: bold;
    color: #3C096C;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.texto-kpi {
    font-size: 16px;
    margin: 0;
    line-height: 1.5;
}
</style>

<div class="tarjeta-kpi">
    <div class="titulo-kpi">💡 Conclusiones</div>
    <p class="texto-kpi">Al analizar la frecuencia relativa, se observa que las empresas en <b>Estados Unidos</b> presentan una mayor proporción de respuestas afirmativas respecto a los beneficios de salud mental en comparación con Europa y Oceanía.</p>
</div>
""", unsafe_allow_html=True)


fig = px.bar(
    df,
    x='Region_con_N',
    y='Frecuencia_Relativa_Porcentaje',
    color='Respuesta_Beneficio',
    barmode='group',
    text='Frecuencia_Relativa_Porcentaje',
    category_orders={"Respuesta_Beneficio": ["Sí", "No"]}, 
    labels={
        'Region_con_N': 'Región Geográfica',
        'Frecuencia_Relativa_Porcentaje': 'Frecuencia Relativa (%)',
        'Respuesta_Beneficio': 'Ofrece Beneficios'
    },
    title='<b>Frecuencia Relativa de Beneficios de Salud Mental</b>',
    hover_data=['Cantidad_Respuestas', 'Total_Encuestados']
)

# condiciones del los colores
for trace in fig.data:
    if trace.name == 'Sí':
        trace.marker.color = ['#7B2CBF' if 'Estados Unidos' in str(x) else '#c77dff' for x in trace.x]
    elif trace.name == 'No':
        trace.marker.color = ['#9d4edd' if 'Estados Unidos' in str(x) else '#E0AAFF' for x in trace.x]

# modificacion del texto
fig.update_traces(
    texttemplate='%{text:.1f}%',          
    textposition='outside',               
    textfont=dict(color='black', weight='bold'), 
    marker=dict(line=dict(color='#3C096C', width=1.5)) 
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',   
    paper_bgcolor='rgba(0,0,0,0)',  
    font=dict(family="sans-serif", color="black", size=12), 
    title=dict(
        font=dict(size=18, color="black"), 
        x=0.5,                  
        xanchor='center'
    ),
    xaxis=dict(
        showgrid=False,         
        title_font=dict(size=14, color="black")
    ),
    yaxis=dict(
        showgrid=True,          
        gridcolor='rgba(123, 44, 191, 0.1)', 
        title_font=dict(size=14, color="black"),
        range=[0, df['Frecuencia_Relativa_Porcentaje'].max() * 1.25]
    ),
    margin=dict(t=80, b=60, l=40, r=40),
    legend=dict(
        title=None, 
        orientation="h", 
        yanchor="bottom", 
        y=1.02, 
        xanchor="right", 
        x=1,
        font=dict(color="black") 
    )
)

with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True, key="grafico_techwell_final", theme=None)


#OBJETIVO NUMERO 2

df1=run_query("""WITH Conteos_Conocimiento AS (
    SELECT 
        CASE 
            WHEN dp.Pais IN ('Estados Unidos', 'United States', 'USA') THEN 'Estados Unidos'
            WHEN dp.Region IN ('Europa', 'Europe') THEN 'Europa'
            WHEN dp.Region IN ('Oceanía', 'Oceania') THEN 'Oceanía'
        END AS Region_Geografica,
        
        db.Conocimiento_Cobertura AS Nivel_Conocimiento, 
        
        COUNT(f.RespuestaID) AS Cantidad
    FROM Fact_Respuesta_Encuestado f
    JOIN Dim_Beneficio_Trabajo db ON f.BeneficiosID = db.BeneficiosID
    JOIN Dim_Pais dp ON f.Pais_Empleo = dp.PaisID 
    
    WHERE (dp.Pais IN ('Estados Unidos', 'United States', 'USA') 
       OR dp.Region IN ('Europa', 'Europe', 'Oceanía', 'Oceania'))
      AND db.Conocimiento_Cobertura IS NOT NULL 
    
    GROUP BY 1, 2
),
Totales_Region AS (
    SELECT Region_Geografica, SUM(Cantidad) AS Total_Region
    FROM Conteos_Conocimiento
    GROUP BY Region_Geografica
)
SELECT 
    c.Region_Geografica,
    c.Nivel_Conocimiento,
    c.Cantidad AS Cantidad_Respuestas,
    t.Total_Region AS Total_Encuestados,
    ROUND((c.Cantidad * 100.0) / t.Total_Region, 2) AS Proporcion_Porcentaje
FROM Conteos_Conocimiento c
JOIN Totales_Region t ON c.Region_Geografica = t.Region_Geografica
ORDER BY c.Region_Geografica, c.Cantidad DESC;""")
             
df1 = run_query("""
SELECT 
    CASE 
        WHEN dp.Pais IN ('Estados Unidos', 'United States', 'USA') THEN 'Estados Unidos'
        WHEN dp.Region IN ('Europa', 'Oceanía', 'Europe', 'Oceania') THEN 'Europa y Oceanía'
        ELSE 'Otros' 
    END AS Region_Geografica,
    db.Conocimiento_Cobertura AS Nivel_Conocimiento, 
    COUNT(f.RespuestaID) AS Cantidad_Respuestas,
    SUM(COUNT(f.RespuestaID)) OVER (
        PARTITION BY CASE 
            WHEN dp.Pais IN ('Estados Unidos', 'United States', 'USA') THEN 'Estados Unidos'
            WHEN dp.Region IN ('Europa', 'Oceanía', 'Europe', 'Oceania') THEN 'Europa y Oceanía'
            ELSE 'Otros' 
        END
    ) AS Total_Encuestados,
    ROUND(
        (COUNT(f.RespuestaID) * 100.0) / 
        SUM(COUNT(f.RespuestaID)) OVER (
            PARTITION BY CASE 
                WHEN dp.Pais IN ('Estados Unidos', 'United States', 'USA') THEN 'Estados Unidos'
                WHEN dp.Region IN ('Europa', 'Oceanía', 'Europe', 'Oceania') THEN 'Europa y Oceanía'
                ELSE 'Otros' 
            END
        ), 2
    ) AS Proporcion_Porcentaje
FROM Fact_Respuesta_Encuestado f
JOIN Dim_Beneficio_Trabajo db ON f.BeneficiosID = db.BeneficiosID
JOIN Dim_Pais dp ON f.Pais_Empleo = dp.PaisID 
WHERE db.Conocimiento_Cobertura IS NOT NULL 
GROUP BY 
    CASE 
        WHEN dp.Pais IN ('Estados Unidos', 'United States', 'USA') THEN 'Estados Unidos'
        WHEN dp.Region IN ('Europa', 'Oceanía', 'Europe', 'Oceania') THEN 'Europa y Oceanía'
        ELSE 'Otros' 
    END, 
    db.Conocimiento_Cobertura
ORDER BY Region_Geografica, Cantidad_Respuestas DESC;
""")
 ########################
st.markdown("""
<style>
.tarjeta-objetivo { background-color: #F8F4FF; border-left: 8px solid #3C096C; border-radius: 10px; padding: 15px 20px; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); margin-bottom: 25px; }
.titulo-obj { color: black; font-size: 22px; font-weight: bold; margin: 0; font-family: sans-serif; }
.texto-obj { color: black; font-size: 16px; margin: 8px 0 0 0; font-family: sans-serif; }
</style>
<div class="tarjeta-objetivo">
    <h2 class="titulo-obj">Objetivo 2</h2>
    <p class="texto-obj">Determinar la proporción de empleados que conocen sus opciones de atención de salud mental laboral según su región geográfica.</p>
</div>
""", unsafe_allow_html=True)

df1['Region_con_N'] = df1['Region_Geografica'] + "<br>(n=" + df1['Total_Encuestados'].astype(str) + ")"

st.markdown("""
<style>
.tarjeta-kpi { background-color: #F8F4FF; border-left: 6px solid #7B2CBF; border-radius: 10px; padding: 20px; box-shadow: 0px 8px 20px rgba(123, 44, 191, 0.15); margin-bottom: 25px; font-family: sans-serif; color: black; }
.titulo-kpi { font-size: 14px; font-weight: bold; color: #3C096C; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.texto-kpi { font-size: 16px; margin: 0; line-height: 1.5; }
</style>
<div class="tarjeta-kpi">
    <div class="titulo-kpi">💡 Conclusiones</div>
    <p class="texto-kpi">Al comparar la distribución de respuestas, se observan contrastes descriptivos en el nivel de conocimiento sobre las opciones de cobertura entre <b>Estados Unidos</b>, el bloque de <b>Europa y Oceanía</b></p>
</div>
""", unsafe_allow_html=True)

fig2 = px.bar(
    df1,
    x='Region_con_N',
    y='Proporcion_Porcentaje',
    color='Nivel_Conocimiento',
    barmode='group',
    text='Proporcion_Porcentaje',
    color_discrete_map={
        'Yes': '#7B2CBF',
        'No': '#c77dff',
        "I don't know": '#E0AAFF'
    },
    category_orders={"Nivel_Conocimiento": ["Yes", "No", "I don't know"]},
    labels={'Region_con_N': 'Región', 'Proporcion_Porcentaje': 'Proporción (%)', 'Nivel_Conocimiento': 'Conoce su cobertura'},
    title='<b>Conocimiento sobre Cobertura de Salud Mental</b>',
    hover_data=['Cantidad_Respuestas', 'Total_Encuestados']
)

fig2.update_traces(
    texttemplate='%{text:.1f}%',          
    textposition='outside',               
    textfont=dict(color='black', weight='bold'), 
    marker=dict(line=dict(color='#3C096C', width=1.5)) 
)

fig2.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',   
    paper_bgcolor='rgba(0,0,0,0)',  
    font=dict(family="sans-serif", color="black", size=12), 
    title=dict(font=dict(size=18, color="black"), x=0.5, xanchor='center'),
    xaxis=dict(showgrid=False, title_font=dict(size=14, color="black")),
    yaxis=dict(showgrid=True, gridcolor='rgba(123, 44, 191, 0.1)', title_font=dict(size=14, color="black"), range=[0, df1['Proporcion_Porcentaje'].max() * 1.25]),
    margin=dict(t=80, b=60, l=40, r=40),
    legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="black"))
)

with st.container(border=True):
    st.plotly_chart(fig2, use_container_width=True, key="graf_obj2", theme=None)


st.markdown("⚠️🔨 En Construcción...")