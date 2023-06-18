import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar los datos
crime = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

# Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard San Francisco Police",
    page_icon="🚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Título del Dashboard
st.title("👮🚓 Datos del Departamento de Policía de San Francisco")

# Descripción de los datos
st.markdown(
    """
    A continuación se muestran los informes de incidentes en la ciudad de San Francisco,
    desde 2018 hasta la fecha actual, con detalles como la fecha, día de la semana,
    distrito policial, vecindario, categoría y subcategoría del incidente, ubicación exacta y resolución.
    """
)

# Convertir columna de fecha a tipo datetime
crime["Incident Date"] = pd.to_datetime(crime["Incident Date"])

# Mapa de delitos
mapa = crime.dropna(subset=["Latitude", "Longitude"])
mapa = mapa[["Incident Date", "Incident Day of Week", "Police District", "Latitude", "Longitude", "Analysis Neighborhood", "Incident Category"]]

# Gráfico: Crímenes por distrito policial
crime_district = crime["Police District"].value_counts().reset_index().rename(columns={"index": "Police District", "Police District": "Número de Crímenes"})
fig1 = px.bar(crime_district, x="Police District", y="Número de Crímenes", color="Police District")
fig1.update_layout(xaxis_title="Distrito Policial", yaxis_title="Número de Crímenes")

# Gráfico: Crímenes por vecindario
crime_neighborhood = crime["Analysis Neighborhood"].value_counts().reset_index().rename(columns={"index": "Neighborhood", "Analysis Neighborhood": "Número de Crímenes"})
crime_neighborhood = crime_neighborhood[crime_neighborhood["Número de Crímenes"] > 10000]
fig2 = px.bar(crime_neighborhood, x="Neighborhood", y="Número de Crímenes", color="Neighborhood")

# Gráfico: Categoría de crímenes
crime_category = crime["Incident Category"].value_counts().reset_index().rename(columns={"index": "Category", "Incident Category": "Número de Crímenes"})
crime_category = crime_category[crime_category["Número de Crímenes"] > 6000]
fig3 = px.pie(crime_category, values="Número de Crímenes", names="Category")

# Gráfico: Ocurrencia de crímenes por hora del día
crime["Incident Hour"] = pd.to_datetime(crime["Incident Time"]).dt.hour
crime_per_hour = crime["Incident Hour"].value_counts().reset_index().rename(columns={"index": "Hour of the Day", "Incident Hour": "Número de Crímenes"})
fig4 = px.line(crime_per_hour, x="Hour of the Day", y="Número de Crímenes")
fig4.update_layout(xaxis_title="Hora del Día", yaxis_title="Número de Crímenes")

# Estructura del Dashboard
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 🗺️ Mapa de Delitos")
    st.map(mapa)
with col2:
    st.markdown("## 📊 Crímenes por Distrito Policial")
    st.plotly_chart(fig1)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown("## 📊 Crímenes por Vecindario")
    st.plotly_chart(fig2)

with col4:
    st.markdown("## 📊 Categoría de Crímenes")
    st.plotly_chart(fig3)

st.markdown("---")

st.markdown("## 📊 Ocurrencia de Crímenes por Hora del Día")
st.plotly_chart(fig4)

st.map(subset_data)

subset_data