from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
#from .model import load_model, make_prediction

# Load the trained model
model = joblib.load('model/diabetes_model.joblib')

app = FastAPI(
    title="Diabetes Prediction API by Razibul", 
    description="This API predicts whether a patient has diabetes or not based on various input features.",
    version="1.0.0",
)

# Load pre-trained model (Logistic Regression, Random Forest, etc.)
#model = load_model()

class PatientData(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

@app.get("/health")
async def health_check():
    return {"status": "ok, healthy and ready to serve."}

@app.post("/predict")
async def predict(patient: PatientData):
    input_data = np.array([
        [
            patient.Pregnancies,
            patient.Glucose,
            patient.BloodPressure,
            patient.SkinThickness,
            patient.Insulin,
            patient.BMI,
            patient.DiabetesPedigreeFunction,
            patient.Age
        ]
    ])
    prediction = model.predict(input_data)
    confidence = model.predict_proba(input_data)[0][prediction[0]]
    
    result = "Diabetic" if prediction[0] == 1 else "Not Diabetic"
    
    return {
        "prediction": int(prediction[0]),
        "result": result,
        "confidence": float(confidence)
    }


@app.get("/metrics")
async def metrics():
    from .metrics import calculate_metrics
    metrics = calculate_metrics()  # Load test set and calculate metrics
    return metrics
