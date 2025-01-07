from django.shortcuts import render
import joblib
import os
from django.http import HttpResponseBadRequest
import numpy as np
import pandas as pd


# Load the trained model
MODEL_PATH = 'bassem_regression_aqi_prediction/ml_models/random_forest_model.pkl'
CITY_MEANS_PATH = 'bassem_regression_aqi_prediction/ml_models/city_means.csv'
SCALER_PATH = 'bassem_regression_aqi_prediction/ml_models/robust_scaler.pkl'

# Check if model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Bassem Regression AQI Pred - Model file not found at {MODEL_PATH}")
if not os.path.exists(CITY_MEANS_PATH):
    raise FileNotFoundError(f"Bassem Regression AQI Pred - City means file not found at {CITY_MEANS_PATH}")
if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Bassem Regression AQI Pred - Scaler file not found at {SCALER_PATH}")


# Load the model using joblib
model = joblib.load(MODEL_PATH)
print(f"Bassem Regression AQI Pred - Model loaded: {model}")

# Load the scaler
scaler = joblib.load(SCALER_PATH)
print(f"Bassem Regression AQI Pred - Scaler loaded: {scaler}")


# Load city means
city_means_df = pd.read_csv(CITY_MEANS_PATH)
print(f"Bassem Regression AQI Pred - City means loaded: {city_means_df}")

# Convert city means into a dictionary for encoding
CITY_MEANS = city_means_df.set_index('City')['AQI'].to_dict()
CITIES = list(CITY_MEANS.keys())


# Create your views here.
def predict(request):
    if request.method == 'POST':
        try:
            # Collect input data from the form
            pm25 = request.POST.get('pm25', '').strip()
            pm10 = request.POST.get('pm10', '').strip()
            no = request.POST.get('no', '').strip()
            no2 = request.POST.get('no2', '').strip()
            nox = request.POST.get('nox', '').strip()
            co = request.POST.get('co', '').strip()
            so2 = request.POST.get('so2', '').strip()
            o3 = request.POST.get('o3', '').strip()
            toluene = request.POST.get('toluene', '').strip()
            benzene = request.POST.get('benzene', '').strip()
            nh3 = request.POST.get('nh3', '').strip()  
            city = request.POST.get('city', '').strip()

            # Validate that all fields are filled
            if not all([pm25, pm10, no, no2, nox, co, so2, o3, toluene, benzene, nh3, city]):
                return HttpResponseBadRequest("All fields are required.")

            # Convert numeric fields to float and validate
            try:
                pm25 = float(pm25)
                pm10 = float(pm10)
                no = float(no)
                no2 = float(no2)
                nox = float(nox)
                co = float(co)
                so2 = float(so2)
                o3 = float(o3)
                toluene = float(toluene)
                benzene = float(benzene)
                nh3 = float(nh3)
            except ValueError:
                return HttpResponseBadRequest("Numeric fields must contain valid numbers.")

            # Validate that the city is in the predefined list
            if city not in CITIES:
                return HttpResponseBadRequest("Invalid city selected.")

            # Get city mean AQI from the dictionary
            city_encoded = CITY_MEANS[city]

            # Combine features (including benzene and nh3 for scaling)
            raw_features = np.array([[pm25, pm10, no, no2, nox, co, so2, o3, toluene, benzene, nh3, city_encoded]])

            # Scale the input features using the loaded scaler
            scaled_features = scaler.transform(raw_features)

            # Select only the relevant features (exclude 'benzene' and 'nh3')
            selected_features = scaled_features[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 11]]  # Exclude benzene (index 9) and nh3 (index 10)

            # Predict AQI using the model
            predicted_aqi = model.predict(selected_features)[0]

            # Render the template with the prediction result
            return render(request, 'predict.html', {
                'cities': CITIES,
                'prediction': predicted_aqi,
                'pm25': pm25, 'pm10': pm10, 'no': no, 'no2': no2, 'nox': nox, 
                'co': co, 'so2': so2, 'o3': o3, 'toluene': toluene, 'benzene': benzene, 'nh3': nh3, 'city': city
            })
        except Exception as e:
            # Handle unexpected errors gracefully
            print(f"Error during prediction: {e}")
            return HttpResponseBadRequest("An unexpected error occurred. Please try again.")

    # Render the form with the list of cities
    return render(request, 'predict.html', {'cities': CITIES})
