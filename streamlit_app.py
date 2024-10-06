import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Function to get real-time data from Raspberry Pi (replace with actual data retrieval)
def get_data():
    df = pd.read_csv("Edited_Generated_Energy_Data.csv")  # Replace with actual path
    
    # Convert the 'Timestamp' column to datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    
    return df

# Load real-time data from Raspberry Pi
df = get_data()

# Title of the dashboard
st.title("Real-time Energy Consumption Dashboard")

# Real-time table display
st.subheader("Energy Data Table (Live Update)")
st.dataframe(df)  # Display the data as a table

# Select graph type for energy consumption
chart_type = st.radio("Select Chart Type for Energy Consumption:", ["Line Chart", "Bar Chart"])

# Plot energy consumption per hour
st.subheader("Energy Consumed Per Hour")
if chart_type == "Line Chart":
    st.line_chart(df[['Timestamp', 'Power (W)']].set_index('Timestamp'))
elif chart_type == "Bar Chart":
    st.bar_chart(df[['Timestamp', 'Power (W)']].set_index('Timestamp'))

# Predicted time to energy exhaustion (gauge or line chart option)
st.subheader("Predicted Time to Energy Exhaustion (h)")

# Select chart type for energy exhaustion prediction
exhaust_chart_type = st.radio("Select Chart Type for Energy Exhaustion Prediction:", ["Gauge Chart", "Line Chart"])

# Mock-up predicted time to exhaustion data (replace this with your actual model's output)
predicted_time = df['Predicted Time to Exhaustion (h)'].iloc[-1]  # Replace with actual prediction logic

# Gauge Chart Implementation
if exhaust_chart_type == "Gauge Chart":
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=predicted_time,
        title={'text': "Time Left Until Energy Exhaustion (hours)"},
        gauge={
            'axis': {'range': [0, 100]},  # Adjust this range according to your model's max prediction
            'bar': {'color': "orange"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': predicted_time
            }
        }
    ))

    st.plotly_chart(fig)

# Line Chart Implementation
elif exhaust_chart_type == "Line Chart":
    # Assuming df['Predicted_Time_to_Exhaustion'] exists in your data
    st.line_chart(df[['Timestamp', 'Predicted_Time_to_Exhaustion (h)']].set_index('Timestamp'))

