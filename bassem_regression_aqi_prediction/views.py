from django.shortcuts import render
import joblib
import os

# Load the trained model
MODEL_PATH = 'bassem_regression_aqi_prediction/ml_models/random_forest_model.pkl'

# Check if model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Load the model using joblib
model = joblib.load(MODEL_PATH)

# Log the model to confirm it loaded correctly
print(f"Model loaded: {model}")

# Create your views here.
def predict(request):
    return render(request, 'predict.html')