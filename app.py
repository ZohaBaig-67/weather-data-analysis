import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Historical Weather Explorer", page_icon="🌦️", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv("weather_data.csv")
    data["Formatted Date"] = pd.to_datetime(data["Formatted Date"], errors="coerce")
    data = data.dropna(subset=["Formatted Date"]).drop_duplicates().copy()
    data["Precip Type"] = data["Precip Type"].fillna("Unknown")
    return data

df = load_data()

st.title("🌦️ Historical Weather Data Explorer")
st.write(
    "Explore historical weather observations through interactive charts. "
    "The dataset has no country or place column, so filters are based on date."
)

st.sidebar.header("Filters")
min_date = df["Formatted Date"].min().date()
max_date = df["Formatted Date"].max().date()
date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

filtered = df[
    (df["Formatted Date"].dt.date >= start_date) &
    (df["Formatted Date"].dt.date <= end_date)
].copy()

if filtered.empty:
    st.warning("No observations found for this date range. Please select another range.")
    st.stop()

st.caption(f"Showing {len(filtered):,} observations from {start_date} to {end_date}.")
avg_temp = filtered["Temperature (C)"].mean()
max_temp = filtered["Temperature (C)"].max()
avg_humidity = filtered["Humidity"].mean()
avg_wind = filtered["Wind Speed (km/h)"].mean()
days_count = filtered["Formatted Date"].dt.date.nunique()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Average temperature", f"{avg_temp:.1f} °C")
m2.metric("Highest temperature", f"{max_temp:.1f} °C")
m3.metric("Average humidity", f"{avg_humidity:.0%}")
m4.metric("Average wind speed", f"{avg_wind:.1f} km/h")
m5.metric("Days covered", f"{days_count:,}")

st.subheader("Weather visualizations")
left, right = st.columns(2)

with left:
    fig = px.histogram(filtered, x="Temperature (C)", nbins=40, marginal="box",
                       title="Temperature distribution",
                       labels={"Temperature (C)": "Temperature (°C)", "count": "Observations"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.histogram(filtered, x="Humidity", nbins=35, title="Humidity distribution",
                       labels={"Humidity": "Humidity (0–1)", "count": "Observations"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    sample = filtered.sample(min(6000, len(filtered)), random_state=42)
    fig = px.scatter(sample, x="Temperature (C)", y="Humidity",
                     opacity=0.35, title="Temperature vs humidity",
                     labels={"Temperature (C)": "Temperature (°C)", "Humidity": "Humidity"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    daily = filtered.set_index("Formatted Date").resample("D")["Temperature (C)"].mean().dropna().reset_index()
    fig = px.line(daily, x="Formatted Date", y="Temperature (C)",
                  title="Daily average temperature over time",
                  labels={"Formatted Date": "Date", "Temperature (C)": "Average temperature (°C)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Wind speed and apparent temperature")
left, right = st.columns(2)
with left:
    fig = px.box(filtered, y="Wind Speed (km/h)", title="Wind speed spread",
                 labels={"Wind Speed (km/h)": "Wind speed (km/h)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    sample = filtered.sample(min(6000, len(filtered)), random_state=42)
    fig = px.scatter(sample, x="Temperature (C)", y="Apparent Temperature (C)",
                     opacity=0.35, title="Actual vs apparent temperature",
                     labels={"Temperature (C)": "Temperature (°C)",
                             "Apparent Temperature (C)": "Apparent temperature (°C)"})
    low = min(sample["Temperature (C)"].min(), sample["Apparent Temperature (C)"].min())
    high = max(sample["Temperature (C)"].max(), sample["Apparent Temperature (C)"].max())
    fig.add_trace(go.Scatter(x=[low, high], y=[low, high], mode="lines",
                             name="Equal temperature", line={"dash": "dash"}))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Correlation heatmap")
corr_cols = ["Temperature (C)", "Apparent Temperature (C)", "Humidity",
             "Wind Speed (km/h)", "Visibility (km)", "Pressure (millibars)"]
corr = filtered[corr_cols].corr()
fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1, aspect="auto", title="Correlation between weather variables")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Main findings")
temp_humidity_corr = filtered["Temperature (C)"].corr(filtered["Humidity"])
apparent_gap = (filtered["Apparent Temperature (C)"] - filtered["Temperature (C)"]).mean()
st.markdown(
    f"""
    - Average temperature in the selected period is **{avg_temp:.2f} °C**.
    - The highest recorded temperature in the selected period is **{max_temp:.2f} °C**.
    - Average humidity is **{avg_humidity:.1%}** and average wind speed is **{avg_wind:.2f} km/h**.
    - The temperature–humidity Pearson correlation is **{temp_humidity_corr:.2f}**.
    - Apparent temperature is on average **{apparent_gap:.2f} °C** relative to actual temperature.
    """
)
st.info("Dataset limitation: no country/place field is available, so geographic filters and country comparisons cannot be shown.")

if st.checkbox("Show raw data table"):
    st.dataframe(filtered, use_container_width=True, height=350)
