import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Lectura de datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Configuración de la página
st.set_page_config(
    page_title = "Herramienta de Visualización de Datos - 13MBID",
    page_icon="📈",
    layout="wide",
)

# Titulo de la aplicacion
st.title("Herramienta de Visualización de Datos - 13MBID")
st.write(
    "Esta aplicación permite explorar y visualizar los datos del proyecto en curso de la AP2."
)
st.write("Desarrollado por: Lídia Martínez Dalmau")
st.markdown("-----")

# Gráficos
st.header("Gráficos")
st.subheader("Caracterización de los gráficos otorgados:")

# Cantidad de créditos por objetivo del mismo
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Visualización
st.plotly_chart(creditos_x_objetivo, use_container_width=True)


st.subheader("Histograma de los importes de créditos otorgados:")

# Histograma de los importes de créditos otorgados

histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')
# Visualización
st.plotly_chart(histograma_importes, use_container_width=True)



# Se agrega un selector para el tipo de credito y se aplica a continuación:
tipo_credito =st.selectbox(
    "Selecciona el tipo de crédito",
    df['objetivo_credito'].unique(),
)


# Filtrar el DataFrame segun el tipi de credito
df_filtrado = df[df['objetivo_credito']== tipo_credito]

col1, col2 = st.columns(2)
with col1:
    barras_apiladas = px.histogram(df, x='objetivo_credito', color='estado_credito_N',
                               title='Distribución de créditos por estado y objetivo',
                               barmode='stack')
    barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')
    st.plotly_chart(barras_apiladas, use_container_width=True)
with col2:


    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora')
    st.plotly_chart(fig, use_container_width=True)

##############################################################################################################

## Nuevo gráfico: Relación entre importe solicitado y duración del crédito, coloreado por estado del crédito
st.subheader("Relación entre importe solicitado y duración del crédito:")

fig_scatter_credito = px.scatter(df, x='duracion_credito', y='importe_solicitado', color='estado_credito_N',
                                 title='Relación entre importe solicitado y duración del crédito')
fig_scatter_credito.update_layout(xaxis_title='Duración del crédito (meses)', yaxis_title='Importe solicitado')

# Visualización
st.plotly_chart(fig_scatter_credito, use_container_width=True)

## Nuevo gráfico: Evolución de los importes solicitados por antigüedad del cliente
st.subheader("Evolución de los importes solicitados por antigüedad del cliente:")

# Definir el orden personalizado
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']

# Ordenar los datos según el orden personalizado
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

# Crear el gráfico de líneas
lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')

# Visualización
st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)

##

# Filtros dinámicos
st.sidebar.header("Filtros dinámicos (Gráfico de cajas y gráfico de dispersión)")

# Filtro por objetivo del crédito
objetivo_seleccionado = st.sidebar.multiselect(
    "Selecciona uno o más objetivos de crédito:",
    options=df['objetivo_credito'].unique(),
    default=df['objetivo_credito'].unique()
)

# Filtro por estado del crédito
estado_seleccionado = st.sidebar.multiselect(
    "Selecciona uno o más estados del crédito:",
    options=df['estado_credito_N'].unique(),
    default=df['estado_credito_N'].unique()
)

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df[(df['objetivo_credito'].isin(objetivo_seleccionado)) & 
                 (df['estado_credito_N'].isin(estado_seleccionado))]

# Sección de gráficos lado a lado
st.subheader("Distribución y relación de importes solicitados")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de cajas: Distribución de los importes solicitados por objetivo del crédito
    fig_box = px.box(df_filtrado, x='objetivo_credito', y='importe_solicitado',
                     title='Distribución de importes solicitados por objetivo del crédito')
    fig_box.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Importe solicitado')
    st.plotly_chart(fig_box, use_container_width=True, key="box_chart")

with col2:
    # Gráfico de dispersión: Relación entre importe solicitado y duración del crédito, coloreado por estado del crédito
    fig_scatter_credito = px.scatter(df_filtrado, x='duracion_credito', y='importe_solicitado', color='estado_credito_N',
                                     title='Relación entre importe solicitado y duración del crédito')
    fig_scatter_credito.update_layout(xaxis_title='Duración del crédito (meses)', yaxis_title='Importe solicitado')
    st.plotly_chart(fig_scatter_credito, use_container_width=True, key="scatter_chart")


# Filtros dinámicos para el mapa de calor
st.sidebar.header("Filtros dinámicos (Mapa de calor de correlación)")

# Filtro por número de personas a cargo
personas_a_cargo_seleccionadas = st.sidebar.multiselect(
    "Selecciona el número de personas a cargo:",
    options=df['personas_a_cargo'].unique(),
    default=df['personas_a_cargo'].unique()
)

# Filtrar el DataFrame según el filtro de personas a cargo
df_filtrado_heatmap = df[df['personas_a_cargo'].isin(personas_a_cargo_seleccionadas)]

# Mapa de calor de correlación
st.subheader("Mapa de calor de correlación entre variables")

corr_matrix = df_filtrado_heatmap[['importe_solicitado', 'duracion_credito', 'personas_a_cargo']].corr()

# Crear el mapa de calor con Seaborn y Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title('Mapa de calor de correlación entre variables')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

##
# Sección de gráficos lado a lado
st.subheader("Comparación de la distribución de tasas de interés")

col1, col2 = st.columns(2)

with col1:
    # Primer histograma: Distribución de tasas de interés
    fig_hist1 = px.histogram(df, x='tasa_interes', nbins=20, title='Distribución de tasas de interés (Histograma 1)')
    fig_hist1.update_layout(xaxis_title='Tasa de interés (%)', yaxis_title='Cantidad de créditos')
    st.plotly_chart(fig_hist1, use_container_width=True, key="hist_tasa_interes_1")

with col2:
    # Segundo histograma: Distribución de tasas de interés
    fig_hist2 = px.histogram(df, x='tasa_interes', nbins=20, title='Distribución de tasas de interés (Histograma 2)')
    fig_hist2.update_layout(xaxis_title='Tasa de interés (%)', yaxis_title='Cantidad de créditos')
    st.plotly_chart(fig_hist2, use_container_width=True, key="hist_tasa_interes_2")

