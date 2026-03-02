import os
import joblib
import numpy as np

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(MODEL_PATH)

def predict_pass_percentage(avg_marks, attendance_percent):
    """
    Returns predicted pass probability (0–100)
    """
    features = np.array([[avg_marks, attendance_percent]])
    prediction = model.predict_proba(features)[0][1]  # probability of passing
    return round(prediction * 100, 2)