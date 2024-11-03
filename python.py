import pandas as pd
import streamlit as st
import os
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title='SISEE', page_icon=':wind_blowing_face:', layout="wide")
st.title(':wind_blowing_face: Wind Section')
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)

# File upload section
fl = st.file_uploader(":file_folder: Upload a file", type=["CSV", "TXT", "xlsx", "XLS"])
if fl is not None:
    df = pd.read_csv(fl, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\TRAVAIL\PycharmProjects\try")
    df = pd.read_csv("file_projet.csv", encoding="ISO-8859-1")

# Assurez-vous que la colonne "Date Enrg" est bien au format datetime
df["Date Enrg"] = pd.to_datetime(df["Date Enrg"], errors='coerce')

# Supprimez les dates non valides, le cas échéant
df = df.dropna(subset=["Date Enrg"])

# Définir la plage minimale et maximale pour les dates
startDate = df["Date Enrg"].min()
endDate = df["Date Enrg"].max()

# Choisir les dates en fixant les valeurs minimales et maximales
col1, col2 = st.columns(2)
with col1:
    date1 = st.date_input("Start Date", startDate, min_value=startDate, max_value=endDate)
with col2:
    date2 = st.date_input("End Date", endDate, min_value=startDate, max_value=endDate)

# Convertir les dates en format datetime
date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)

# Filtrer les données en fonction de la plage de dates sélectionnée
df = df[(df["Date Enrg"] >= date1) & (df["Date Enrg"] <= date2)].copy()


# Filter by date range
df = df[(df["Date Enrg"] >= date1) & (df["Date Enrg"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("GPS Coordinates")
GPS_Data = st.sidebar.multiselect("Input Longitude and Latitude", df["GPS"].unique())
df1 = df[df["GPS"].isin(GPS_Data)] if GPS_Data else df.copy()

st.sidebar.header("Choose your Country")
country = st.sidebar.multiselect("Pick your Country", df1["Country"].unique())
df2 = df1[df1["Country"].isin(country)] if country else df1.copy()

st.sidebar.header("Choose your Region")
region = st.sidebar.multiselect("Pick your Region", df2["Region"].unique())
df3 = df2[df2["Region"].isin(region)] if region else df2.copy()

st.sidebar.header("Choose your District")
district = st.sidebar.multiselect("Pick your District", df3["District"].unique())
filtered_df = df3[df3["District"].isin(district)] if district else df3.copy()

# Data Aggregation for Wind Speed
classified_df = filtered_df.groupby("Wind speed(m/s)", as_index=False)["Probability"].sum()

# Displaying Weibull Wind Speed chart
col1, col2 = st.columns(2)
with col1:
    st.subheader("Weibull Wind speed(m/s)")
    fig = px.bar(
        classified_df,
        x="Wind speed(m/s)",
        y="Probability",
        text=[f'{x:,.5f}' for x in classified_df["Probability"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Wind speed(m/s) by District")

    # Calculate average wind speed by district
    avg_wind_speed_by_district = filtered_df.groupby("District", as_index=False)["Wind speed(m/s)"].mean()

    # Create a pie chart
    fig = px.pie(
        avg_wind_speed_by_district,
        values="Wind speed(m/s)",
        names="District",
        hole=0.1,
        title="Wind speed (m/s) by District"
    )

    # Customize hover information to show average wind speed
    fig.update_traces(hovertemplate="District: %{label}<br>Average Wind Speed: %{value:.2f} m/s")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
# Wind Frequency and Wind Time Series Analysis side by side
classified_df_1 = filtered_df.groupby("Wind speed(m/s)", as_index=False)["Time"].sum()

col1, col2 = st.columns(2)  # Creating two side-by-side columns

with col1:
    st.subheader("Wind Frequency")
    fig = px.bar(
        classified_df_1,
        x="Wind speed(m/s)",
        y="Time",
        text=[f'{x:,.5f}' for x in classified_df_1["Time"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Wind Time Series Analysis
    filtered_df["month_year"] = filtered_df["Date Enrg"].dt.to_period("M").astype(str)
    st.subheader("Wind Time Series Analysis")
    linechart = filtered_df.groupby("month_year")["Wind speed(m/s)"].sum().reset_index()
    fig2 = px.line(linechart, x="month_year", y="Wind speed(m/s)", labels={"Wind speed(m/s)": "Wind speed(m/s)"})
    st.plotly_chart(fig2, use_container_width=True)

# Downloadable Data Section
col1, col2 = st.columns(2)
with col1:
    with st.expander("Weibull Parameter Data"):
        st.write(classified_df)
        CSV = classified_df.to_csv(index=False).encode('UTF-8')
        st.download_button("Download Data", data=CSV, file_name="Weibull_Wind_speed.csv", mime="text/csv")

with col2:
    with st.expander("Wind Speed Data by Region"):
        region_data = classified_df.groupby("Wind speed(m/s)", as_index=False)["Wind speed(m/s)"].sum()
        st.write(region_data)
        CSV = region_data.to_csv(index=False).encode('UTF-8')
        st.download_button("Download Data", data=CSV, file_name="Wind_speed_region.csv", mime="text/csv")

st.title(':thermometer: Temperature Section')
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)

classified_df = filtered_df.groupby("Temperature (°C)", as_index=False)["Probability"].sum()

# Displaying Weibull Wind Speed chart
col1, col2 = st.columns(2)
with col1:
    st.subheader("Weibull Temperature (°C)")
    fig = px.bar(
        classified_df,
        x="Temperature (°C)",
        y="Probability",
        text=[f'{x:,.5f}' for x in classified_df["Probability"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Temperature (°C) by District")

    # Calculate average wind speed by district
    avg_wind_speed_by_district = filtered_df.groupby("District", as_index=False)["Temperature (°C)"].mean()

    # Create a pie chart
    fig = px.pie(
        avg_wind_speed_by_district,
        values="Temperature (°C)",
        names="District",
        hole=0.1,
        title="Temperature (°C) by District"
    )

    # Customize hover information to show average wind speed
    fig.update_traces(hovertemplate="District: %{label}<br>Average Temperature (°C): %{value:.2f} °C")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

classified_df_1 = filtered_df.groupby("Temperature (°C)", as_index=False)["Time"].sum()

col1, col2 = st.columns(2)  # Creating two side-by-side columns

with col1:
    st.subheader("Temperature Frequency")
    fig = px.bar(
        classified_df_1,
        x="Temperature (°C)",
        y="Time",
        text=[f'{x:,.5f}' for x in classified_df_1["Time"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Temperature (°C) Series Analysis
    filtered_df["month_year"] = filtered_df["Date Enrg"].dt.to_period("M").astype(str)
    st.subheader("Temperature Time Series Analysis")
    linechart = filtered_df.groupby("month_year")["Temperature (°C)"].sum().reset_index()
    fig2 = px.line(linechart, x="month_year", y="Temperature (°C)", labels={"Temperature (°C)": "Temperature (°C)"})
    st.plotly_chart(fig2, use_container_width=True)

st.title(':radioactive_sign: Solar Irradiation Section')
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)
classified_df = filtered_df.groupby("Irradiation (W/m²)", as_index=False)["Probability"].sum()

# Displaying Weibull Wind Speed chart
col1, col2 = st.columns(2)
with col1:
    st.subheader("Weibull Irradiation (W/m²) ")
    fig = px.bar(
        classified_df,
        x="Irradiation (W/m²)",
        y="Probability",
        text=[f'{x:,.5f}' for x in classified_df["Probability"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Irradiation (W/m²)  by District")

    # Calculate average wind speed by district
    avg_wind_speed_by_district = filtered_df.groupby("District", as_index=False)["Irradiation (W/m²)"].mean()

    # Create a pie chart
    fig = px.pie(
        avg_wind_speed_by_district,
        values="Irradiation (W/m²)",
        names="District",
        hole=0.1,
        title="Irradiation (W/m²)  by District"
    )

    # Customize hover information to show average wind speed
    fig.update_traces(hovertemplate="District: %{label}<br>Average Irradiation (W/m²) : %{value:.2f} W/m²")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

classified_df_1 = filtered_df.groupby("Irradiation (W/m²)", as_index=False)["Time"].sum()

col1, col2 = st.columns(2)  # Creating two side-by-side columns

with col1:
    st.subheader("Irradiation Frequency")
    fig = px.bar(
        classified_df_1,
        x="Irradiation (W/m²)",
        y="Time",
        text=[f'{x:,.5f}' for x in classified_df_1["Time"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Temperature (°C) Series Analysis
    filtered_df["month_year"] = filtered_df["Date Enrg"].dt.to_period("M").astype(str)
    st.subheader("Irradiation Time Series Analysis")
    linechart = filtered_df.groupby("month_year")["Irradiation (W/m²)"].sum().reset_index()
    fig2 = px.line(linechart, x="month_year", y="Irradiation (W/m²)", labels={"Irradiation (W/m²)": "Irradiation (W/m²)"})
    st.plotly_chart(fig2, use_container_width=True)

st.title(':sweat_drops: Relative Humidity Section')
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)
classified_df = filtered_df.groupby("Relative Humidity (%)", as_index=False)["Probability"].sum()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Weibull Relative Humidity (%)")
    fig = px.bar(
        classified_df,
        x="Relative Humidity (%)",
        y="Probability",
        text=[f'{x:,.5f}' for x in classified_df["Probability"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Relative Humidity (%)  by District")

    # Calculate average wind speed by district
    avg_wind_speed_by_district = filtered_df.groupby("District", as_index=False)["Relative Humidity (%)"].mean()

    # Create a pie chart
    fig = px.pie(
        avg_wind_speed_by_district,
        values="Relative Humidity (%)",
        names="District",
        hole=0.1,
        title="Relative Humidity (%)  by District"
    )

    # Customize hover information to show average wind speed
    fig.update_traces(hovertemplate="District: %{label}<br>Average Relative Humidity (%) : %{value:.2f} %")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
classified_df_1 = filtered_df.groupby("Relative Humidity (%)", as_index=False)["Time"].sum()

col1, col2 = st.columns(2)  # Creating two side-by-side columns

with col1:
    st.subheader("Relative Humidity Frequency")
    fig = px.bar(
        classified_df_1,
        x="Relative Humidity (%)",
        y="Time",
        text=[f'{x:,.5f}' for x in classified_df_1["Time"]],
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Temperature (°C) Series Analysis
    filtered_df["month_year"] = filtered_df["Date Enrg"].dt.to_period("M").astype(str)
    st.subheader("Relative Humidity Time Series Analysis")
    linechart = filtered_df.groupby("month_year")["Relative Humidity (%)"].sum().reset_index()
    fig2 = px.line(linechart, x="month_year", y="Relative Humidity (%)", labels={"Relative Humidity (%)": "Relative Humidity (%)"})
    st.plotly_chart(fig2, use_container_width=True)

st.title(':droplet: Rain Section')
st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>', unsafe_allow_html=True)
# classified_df = filtered_df.groupby("Relative Humidity (%)", as_index=False)["Probability"].sum()
#
# col1, col2 = st.columns(2)
# with col1:
#     st.subheader("Weibull Relative Humidity (%)")
#     fig = px.bar(
#         classified_df,
#         x="Relative Humidity (%)",
#         y="Probability",
#         text=[f'{x:,.5f}' for x in classified_df["Probability"]],
#         template="seaborn"
#     )
#     st.plotly_chart(fig, use_container_width=True)
#
# with col2:
#     st.subheader("Relative Humidity (%)  by District")
#
#     # Calculate average wind speed by district
#     avg_wind_speed_by_district = filtered_df.groupby("District", as_index=False)["Relative Humidity (%)"].mean()
#
#     # Create a pie chart
#     fig = px.pie(
#         avg_wind_speed_by_district,
#         values="Relative Humidity (%)",
#         names="District",
#         hole=0.1,
#         title="Relative Humidity (%)  by District"
#     )
#
#     # Customize hover information to show average wind speed
#     fig.update_traces(hovertemplate="District: %{label}<br>Average Relative Humidity (%) : %{value:.2f} %")
#
#     # Display the chart
#     st.plotly_chart(fig, use_container_width=True)
# classified_df_1 = filtered_df.groupby("Relative Humidity (%)", as_index=False)["Time"].sum()
#
# col1, col2 = st.columns(2)  # Creating two side-by-side columns
#
# with col1:
#     st.subheader("Relative Humidity Frequency")
#     fig = px.bar(
#         classified_df_1,
#         x="Relative Humidity (%)",
#         y="Time",
#         text=[f'{x:,.5f}' for x in classified_df_1["Time"]],
#         template="seaborn"
#     )
#     st.plotly_chart(fig, use_container_width=True)
#
# with col2:
#     # Temperature (°C) Series Analysis
#     filtered_df["month_year"] = filtered_df["Date Enrg"].dt.to_period("M").astype(str)
#     st.subheader("Relative Humidity Time Series Analysis")
#     linechart = filtered_df.groupby("month_year")["Relative Humidity (%)"].sum().reset_index()
#     fig2 = px.line(linechart, x="month_year", y="Relative Humidity (%)", labels={"Relative Humidity (%)": "Relative Humidity (%)"})
#     st.plotly_chart(fig2, use_container_width=True)
