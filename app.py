import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar el archivo CSV
df = pd.read_csv("vehicles_us.csv")

# Crear columna 'manufacturer' a partir de la primera palabra de 'model'
df['manufacturer'] = df['model'].str.split().str[0]

st.title("Dashboard de Vehículos 🚗")

# --- Filtros en la barra lateral ---
st.sidebar.header("Filtros")

# Filtro por fabricante
fabricantes = df['manufacturer'].dropna().unique()
fabricantes_seleccionados = st.sidebar.multiselect(
    "Selecciona fabricantes:",
    options=sorted(fabricantes),
    default=sorted(fabricantes)[:5]
)

# Filtro por rango de precio
min_price, max_price = int(df['price'].min()), int(df['price'].max())
rango_precio = st.sidebar.slider(
    "Rango de precio ($):",
    min_price, max_price, (min_price, max_price)
)

# Filtro por rango de kilometraje
min_km, max_km = int(df['odometer'].min()), int(df['odometer'].max())
rango_km = st.sidebar.slider(
    "Rango de kilometraje (mi):",
    min_km, max_km, (min_km, max_km)
)

# --- Aplicar filtros ---
df_filtrado = df.copy()

if fabricantes_seleccionados:
    df_filtrado = df_filtrado[df_filtrado['manufacturer'].isin(fabricantes_seleccionados)]

df_filtrado = df_filtrado[
    (df_filtrado['price'].between(rango_precio[0], rango_precio[1])) &
    (df_filtrado['odometer'].between(rango_km[0], rango_km[1]))
]

# --- Tabs (pestañas) ---
tab1, tab2, tab3 = st.tabs(["📊 Gráficos", "📈 Estadísticas", "📑 Datos"])

# ================== TAB 1 - GRÁFICOS ==================
with tab1:
    st.subheader("Visualización de variables")
    opcion = st.selectbox(
        "Elige una variable para visualizar:",
        ["price", "odometer", "condition", "fuel", "transmission", "type", "manufacturer"]
    )

    if opcion in ["price", "odometer"]:  # numéricas
        fig = px.histogram(df_filtrado, x=opcion, nbins=30, color="manufacturer")
        st.plotly_chart(fig, use_container_width=True)
    else:  # categóricas
        fig = px.histogram(df_filtrado, x=opcion, color="manufacturer")
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico de dispersión
    st.subheader("Relación entre precio y kilometraje")
    fig_scatter = px.scatter(
        df_filtrado,
        x="odometer",
        y="price",
        color="manufacturer",
        hover_data=["model", "condition", "fuel", "transmission"],
        opacity=0.7
    )
    fig_scatter.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_scatter, use_container_width=True)

# ================== TAB 2 - ESTADÍSTICAS ==================
with tab2:
    st.subheader("Estadísticas de precio y kilometraje")
    stats = (
        df_filtrado.groupby("manufacturer")[["price", "odometer"]]
        .agg(["mean", "median", "std", "min", "max"])
        .round(2)
    )
    st.write(stats)

# ================== TAB 3 - DATOS ==================
with tab3:
    st.subheader("Vista previa de los datos filtrados")
    st.write(df_filtrado.head(20))
    st.download_button(
        label="📥 Descargar datos filtrados (CSV)",
        data=df_filtrado.to_csv(index=False),
        file_name="vehiculos_filtrados.csv",
        mime="text/csv"
    )

