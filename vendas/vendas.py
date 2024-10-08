import altair as alt
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(layout='wide')

# Load the data from the CSV file
df = pd.read_csv('vendas/vendas.csv', delimiter=';', parse_dates=['Date'])

# Convert 'Total' and 'Rating' columns to numeric, replacing ',' with '.'
df['Total'] = df['Total'].str.replace(',', '.').astype(float)
df['Rating'] = pd.to_numeric(df['Rating'].str.replace(',', '.'))

# Extract year and month from 'Date' column
df['YearMonth'] = df['Date'].dt.to_period('M')

# Get unique year-months
yearmonths = sorted(df['YearMonth'].unique().astype(str))

# Sidebar selectbox
selected_yearmonth = st.sidebar.selectbox('Select a year and month', yearmonths)

# Filter data based on selected year and month
df_filtered = df[df['YearMonth'].astype(str) == selected_yearmonth]

# Create two columns for the first row
col1, col2 = st.columns(2)

# Display the data as an Altair chart using `st.altair_chart`.
chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Total:Q", title="Total"),
        color='City:N'
    )
    .properties(height=320, title="Faturamento por dia")
)
col1.altair_chart(chart, use_container_width=True)

# Group by 'Product line', 'City' and sum 'Total'
df_grouped = df_filtered.groupby(['Product line', 'City'])['Total'].sum().reset_index()

# Display the data as an Altair chart using `st.altair_chart`.
chart = (
    alt.Chart(df_grouped)
    .mark_bar()
    .encode(
        y=alt.Y("Product line:N", title="Product Line"),
        x=alt.X("Total:Q", title="Total"),
        color='City:N'
    )
    .properties(height=320, title="Faturamento por tipo de produto")
)
col2.altair_chart(chart, use_container_width=True)

# Create three columns for the second row
col3, col4, col5 = st.columns(3)

# Group by 'City' and sum 'Total'
df_city = df_filtered.groupby('City')['Total'].sum().reset_index()

# Display the data as an Altair chart using `st.altair_chart`.
chart = (
    alt.Chart(df_city)
    .mark_bar()
    .encode(
        x=alt.X("City:N", title="City"),
        y=alt.Y("Total:Q", title="Total"),
    )
    .properties(height=320, title="Faturamento por cidade")
)
col3.altair_chart(chart, use_container_width=True)

# Group by 'Payment' and sum 'Total'
df_payment = df_filtered.groupby('Payment')['Total'].sum().reset_index()

# Calculate percentage
total = df_payment['Total'].sum()
df_payment['Percentage'] = ((df_payment['Total'] / total) * 100).round(2)

# Display the data as an Altair chart using `st.altair_chart`.
chart = (
    alt.Chart(df_payment)
    .mark_arc(outerRadius=100)
    .encode(
        theta=alt.Theta("Total:Q", title="Total"),
        color=alt.Color('Payment:N', legend=alt.Legend(title="Payment Type")),
        tooltip=['Payment', 'Total'],
    )
    .properties(width=400, height=400, title="Faturamento por tipo de pagamento")
)

col4.altair_chart(chart, use_container_width=True)
# Group by 'City' and calculate average 'Rating'
df_rating = df_filtered.groupby('City')['Rating'].mean().reset_index()

# Display the data as an Altair chart using `st.altair_chart`.
chart = (
    alt.Chart(df_rating)
    .mark_bar()
    .encode(
        x=alt.X("City:N", title="City"),
        y=alt.Y("Rating:Q", title="Average Rating"),
    )
    .properties(height=320, title="Avaliação média")
)
col5.altair_chart(chart, use_container_width=True)