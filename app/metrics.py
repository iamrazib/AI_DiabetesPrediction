
from sklearn.metrics import classification_report
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import os  # To handle directories

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_dir = os.path.join(base_dir, 'model')
dataset_path = os.path.join(base_dir, 'diabetes.csv')

os.makedirs(model_dir, exist_ok=True)


# Load the dataset
def load_data():
    data = pd.read_csv(dataset_path)
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    return X, y

def calculate_metrics():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Load model
    #model = joblib.load('diabetes_model.pkl')
    model = joblib.load('model/diabetes_model.joblib')

    # Standardize features
    scaler = StandardScaler()
    X_test = scaler.fit_transform(X_test)

    # Predict
    y_pred = model.predict(X_test)

    # Return classification metrics
    return classification_report(y_test, y_pred, output_dict=True)
