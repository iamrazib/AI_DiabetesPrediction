import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

import os  # To handle directories

# Get the absolute path to the root of the project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create the 'model' directory if it doesn't exist
model_dir = os.path.join(base_dir, 'model')
dataset_path = os.path.join(base_dir, 'diabetes.csv')

os.makedirs(model_dir, exist_ok=True)

# Load the dataset
data = pd.read_csv(dataset_path)  

# Features (X) and Labels (y)
X = data.drop('Outcome', axis=1)  # 'Outcome' is the target column (whether the person has diabetes or not)
y = data['Outcome']  # 'Outcome' is the label (0 or 1, where 1 means diabetic and 0 means not diabetic)

# Split data into training and test sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features (important for models like Logistic Regression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train) 
X_test = scaler.transform(X_test) 

# Train a Logistic Regression model 
model = LogisticRegression()
model.fit(X_train, y_train) 

# Save the model to a file using joblib
#joblib.dump(model, 'diabetes_model.pkl')  # This will save the model as 'diabetes_model.pkl'

# Save the model using joblib
model_path = os.path.join(model_dir, 'diabetes_model.joblib')

# Save the model using joblib
joblib.dump(model, model_path)

print("Diabetes Model trained and saved successfully.")
