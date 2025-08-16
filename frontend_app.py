import streamlit as st
import requests
import json

# Streamlit App: frontend_app.py

# Set the title of the app
st.title("Heart Disease Prediction")

# Add some instructions
st.write("Enter the details below and get your heart disease prediction.")

# Input fields for the user to fill in
age = st.number_input('Age', min_value=0, max_value=120, value=25)
sex = st.selectbox('Sex', ['Male', 'Female'])
cp = st.selectbox('Chest Pain Type', [0, 1, 2, 3])  # Example values, customize as needed
trestbps = st.number_input('Resting Blood Pressure', min_value=90, max_value=200, value=120)
chol = st.number_input('Serum Cholesterol', min_value=100, max_value=500, value=200)
fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['True', 'False'])
restecg = st.selectbox('Resting Electrocardiographic Results', [0, 1, 2])
thalach = st.number_input('Maximum Heart Rate Achieved', min_value=50, max_value=220, value=150)
exang = st.selectbox('Exercise Induced Angina', ['Yes', 'No'])
oldpeak = st.number_input('Depression Induced by Exercise', min_value=0.0, max_value=6.0, value=1.0)
slope = st.selectbox('Slope of the Peak Exercise ST Segment', [1, 2, 3])
ca = st.selectbox('Number of Major Vessels Colored by Fluoroscopy', [0, 1, 2, 3])
thal = st.selectbox('Thalassemia', [3, 6, 7])

# Convert the string inputs to integers or floats where necessary
sex = 1 if sex == 'Male' else 0
fbs = 1 if fbs == 'True' else 0
exang = 1 if exang == 'Yes' else 0

# Collect the input data
input_data = {
    "age": age,
    "sex": sex,
    "cp": cp,
    "trestbps": trestbps,
    "chol": chol,
    "fbs": fbs,
    "restecg": restecg,
    "thalach": thalach,
    "exang": exang,
    "oldpeak": oldpeak,
    "slope": slope,
    "ca": ca,
    "thal": thal
}

# URL of the deployed FastAPI backend on Render
backend_url = 'https://ai-diabetesprediction.onrender.com/predict'

# Send a POST request with the input data
response = requests.post(backend_url, json=input_data)

# Check if the request was successful
if response.status_code == 200:
    prediction = response.json()['heart_disease']
    st.write(f"Prediction: {'Heart Disease Detected' if prediction else 'No Heart Disease Detected'}")
else:
    st.write("Error in fetching the prediction.")
