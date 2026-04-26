import streamlit as st
import plotly.express as px
from utils import load_all_data, filter_data

st.set_page_config(page_title="Africa Climate Dashboard", layout="wide")
st.title("East & West Africa Climate Trends (2015–March 2026)")

df = load_all_data()

if df.empty:
    st.error("No data found. Run Task 2 first.")
    st.stop()

st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect("Select Countries", 
                    options=df['Country'].unique(), 
                    default=df['Country'].unique())

min_year = int(df['Date'].dt.year.min())
max_year = int(df['Date'].dt.year.max())
year_range = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))

var_options = ['T2M', 'PRECTOTCORR', 'RH2M', 'T2M_MAX']
selected_var = st.sidebar.selectbox("Main Variable", var_options)

filtered = filter_data(df, selected_countries, year_range[0], year_range[1])

col1, col2 = st.columns(2)

with col1:
    fig = px.line(filtered.groupby(['Country', 'Date'])[selected_var].mean().reset_index(),
                  x='Date', y=selected_var, color='Country')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.box(filtered, x='Country', y='PRECTOTCORR', color='Country')
    st.plotly_chart(fig, use_container_width=True)

numeric_df = filtered.select_dtypes(include='number').corr()
fig = px.imshow(numeric_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu')
st.plotly_chart(fig, use_container_width=True)