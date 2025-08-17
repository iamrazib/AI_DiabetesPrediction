import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any

st.set_page_config(
    page_title="Diabetes Predictor · Streamlit",
    page_icon="🩺",
    layout="centered",
)

# -----------------------------
# Sidebar: API Settings
# -----------------------------
st.sidebar.header("⚙️ API Settings")
api_base = st.sidebar.text_input(
    "FastAPI base URL",
    value="https://ai-diabetesprediction.onrender.com/predict",
    help="Your FastAPI server root. Example: https://your-app.onrender.com",
)

colA, colB = st.sidebar.columns(2)
if colA.button("Check API Health"):
    try:
        r = requests.get(f"{api_base}/health", timeout=8)
        if r.ok:
            st.sidebar.success(f"Health OK: {r.json()}")
        else:
            st.sidebar.error(f"Health check failed: {r.status_code}")
    except Exception as e:
        st.sidebar.error(f"Health check error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Tip: If deploying Streamlit separately from FastAPI, ensure CORS is enabled in your API."
)

# -----------------------------
# Main: App Title
# -----------------------------
st.title(" Diabetes Prediction (API Client)")
st.write(
    "This app collects patient metrics and sends them to your **FastAPI** endpoint to get a prediction."
)

# -----------------------------
# Input Form
# -----------------------------
with st.form("patient_form", clear_on_submit=False):
    st.subheader("Patient Input")
    c1, c2, c3 = st.columns(3)

    Pregnancies = c1.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1,
                                  help="Number of times pregnant")
    Glucose = c2.number_input("Glucose", min_value=0, max_value=300, value=120, step=1,
                              help="Plasma glucose concentration (mg/dL)")
    BloodPressure = c3.number_input("Blood Pressure", min_value=0, max_value=200, value=70, step=1,
                                    help="Diastolic blood pressure (mm Hg)")

    SkinThickness = c1.number_input("Skin Thickness", min_value=0, max_value=99, value=20, step=1,
                                    help="Triceps skin fold thickness (mm)")
    Insulin = c2.number_input("Insulin", min_value=0, max_value=900, value=79, step=1,
                              help="2-Hour serum insulin (mu U/ml)")
    BMI = c3.number_input("BMI", min_value=0.0, max_value=70.0, value=32.0, step=0.1,
                          help="Body mass index (weight/height^2)")

    DiabetesPedigreeFunction = c1.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.47,
                                               step=0.01, help="Diabetes heredity metric")
    Age = c2.number_input("Age", min_value=1, max_value=120, value=33, step=1)

    submitted = st.form_submit_button("🔮 Predict")

# -----------------------------
# Call API on submit
# -----------------------------

def call_predict(api_root: str, payload: Dict[str, Any]):
    url = f"{api_root}/predict"
    r = requests.post(url, json=payload, timeout=12)
    r.raise_for_status()
    return r.json()

if submitted:
    payload = {
        "Pregnancies": int(Pregnancies),
        "Glucose": float(Glucose),
        "BloodPressure": float(BloodPressure),
        "SkinThickness": float(SkinThickness),
        "Insulin": float(Insulin),
        "BMI": float(BMI),
        "DiabetesPedigreeFunction": float(DiabetesPedigreeFunction),
        "Age": int(Age),
    }

    with st.spinner("Contacting API and generating prediction…"):
        try:
            data = call_predict(api_base, payload)
            # Expected keys: prediction (0/1), result (str), confidence (0..1)
            result = data.get("result", "Unknown")
            conf = float(data.get("confidence", 0.0))
            conf_pct = round(conf * 100, 2) if conf <= 1 else round(conf, 2)

            if result.lower().startswith("diabetic") or data.get("prediction") == 1:
                st.error(f" Prediction: **{result}**")
            else:
                st.success(f" Prediction: **{result}**")

            st.metric(label="Confidence", value=f"{conf_pct}%")

            st.markdown("### Raw Response")
            st.json(data)

            # Show payload for reference
            st.markdown("### Submitted Features")
            df = pd.DataFrame([payload])
            st.dataframe(df, use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
---
**Notes**
- Make sure your FastAPI service exposes `/health` and `/predict` endpoints as implemented in your backend.
- If Streamlit is hosted on a different domain than FastAPI, enable CORS in your API.
""")
