from django.shortcuts import render
from django.http import HttpResponseBadRequest
import joblib
import os
import numpy as np
import traceback

# Paths to your saved model and scaler
MODEL_PATH = 'taha_regression/ml_models/gradient_boosting_model.pkl'
MODEL_PATH = 'taha_regression/ml_models/gradient_boosting_model.pkl'
TEMPERATURE_SCALER_PATH = 'taha_regression/ml_models/temperature_scaler.pkl'
PRESSURE_SCALER_PATH = 'taha_regression/ml_models/pressure_scaler.pkl'
WIND_DIRECTION_SCALER_PATH = 'taha_regression/ml_models/wind_direction_scaler.pkl'

# Check if model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Taha Regression - Model file not found at {MODEL_PATH}")
if not (os.path.exists(TEMPERATURE_SCALER_PATH) and os.path.exists(PRESSURE_SCALER_PATH) and os.path.exists(WIND_DIRECTION_SCALER_PATH)) :
    raise FileNotFoundError(f"Taha Regression - Scaler file not found")

# Load the model using joblib
model = joblib.load(MODEL_PATH)
print(f"Taha Regression - Model loaded: {model}")

# Load the scaler
temperature_scaler = joblib.load(TEMPERATURE_SCALER_PATH)
pressure_scaler = joblib.load(PRESSURE_SCALER_PATH)
wind_direction_scaler = joblib.load(WIND_DIRECTION_SCALER_PATH)
print(f"Taha Regression - Scaler loaded")

def predict(request):
    if request.method == 'POST':
        try:
            print("POST request received.")

            # Collect input data from the form
            temperature = request.POST.get('temperature', '').strip()
            pressure = request.POST.get('pressure', '').strip()
            wind_direction = request.POST.get('wind_direction', '').strip()
            print(f"Received inputs: Temperature={temperature}, Pressure={pressure}, Wind Direction={wind_direction}")

            # Validate that all fields are filled
            if not all([temperature, pressure, wind_direction]):
                print("Validation failed: Missing fields.")
                return HttpResponseBadRequest("All fields are required.")

            # Convert inputs to float and validate
            try:
                temperature = float(temperature)
                pressure = float(pressure)
                wind_direction = float(wind_direction)
                print(f"Converted inputs: Temperature={temperature}, Pressure={pressure}, Wind Direction={wind_direction}")
            except ValueError as e:
                print(f"Input conversion error: {e}")
                return HttpResponseBadRequest("Inputs must be valid numbers.")

            # Scale each feature independently
            temperature_scaled = temperature_scaler.transform([[temperature]])
            pressure_scaled = pressure_scaler.transform([[pressure]])
            wind_direction_scaled = wind_direction_scaler.transform([[wind_direction]])

            # Combine scaled features
            scaled_features = np.hstack((temperature_scaled, pressure_scaled, wind_direction_scaled))
            print(f"Scaled features: {scaled_features}")

            # Predict using the model
            predicted_solar_radiation = model.predict(scaled_features)[0]
            print(f"Prediction: {predicted_solar_radiation}")
            predicted_solar_radiation = round(abs(predicted_solar_radiation), 2)

            # Render the result
            print("Rendering result to the template.")
            return render(request, 'taha_regression.html', {
                'prediction': predicted_solar_radiation,
                'temperature': temperature,
                'pressure': pressure,
                'wind_direction': wind_direction
            })

        except Exception as e:
            print(f"Error during prediction: {e}")
            traceback.print_exc()  # Log the full stack trace
            return HttpResponseBadRequest("An unexpected error occurred. Please try again.")

    # Render the input form
    print("Rendering input form.")
    return render(request, 'taha_regression.html')

