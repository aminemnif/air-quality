import numpy as np
import joblib
import os
from django.shortcuts import render
from django.http import HttpResponseBadRequest
import traceback
from sklearn.preprocessing import LabelEncoder

# Load the trained model
MODEL_PATH = 'predictor/models/random_forest_model.pkl'

# Check if model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Load the model using joblib
model = joblib.load(MODEL_PATH)

# Log the model to confirm it loaded correctly
print(f"Model loaded: {model}")

def predict_co2(request):
    if request.method == 'POST':
        try:
            # Collect input data from the form
            fuel_city = request.POST.get('fuel_city', '').strip()
            fuel_hwy = request.POST.get('fuel_hwy', '').strip()
            fuel_comb = request.POST.get('fuel_comb', '').strip()
            fuel_mpg = request.POST.get('fuel_mpg', '').strip()
            vehicle_model = request.POST.get('model', '').strip()

            # Log the received data
            print(f"Received data: fuel_city: '{fuel_city}', fuel_hwy: '{fuel_hwy}', fuel_comb: '{fuel_comb}', fuel_mpg: '{fuel_mpg}', vehicle_model: '{vehicle_model}'")

            # Ensure all fields are provided
            if not fuel_city or not fuel_hwy or not fuel_comb or not fuel_mpg or not vehicle_model:
                return HttpResponseBadRequest("All fields are required.")

            # Convert to float and check if it's valid for numeric fields
            try:
                fuel_city = float(fuel_city)
                fuel_hwy = float(fuel_hwy)
                fuel_comb = float(fuel_comb)
                fuel_mpg = float(fuel_mpg)
            except ValueError:
                return HttpResponseBadRequest("Fuel fields must contain valid numeric values.")

            # Encode vehicle_model (categorical string) to a numeric value using LabelEncoder
            encoder = LabelEncoder()
            vehicle_model_encoded = encoder.fit_transform([vehicle_model])[0]  # Encodes to a numeric value

            # Log the input features before prediction
            input_features = np.array([[fuel_city, fuel_hwy, fuel_comb, fuel_mpg, vehicle_model_encoded]])
            print(f"Input features for prediction: {input_features}")

            # Try making a test prediction with the model
            try:
                predicted_co2 = model.predict(input_features)[0]
                print(f"Prediction result: {predicted_co2}")
            except Exception as prediction_error:
                # Log detailed error message and traceback
                print(f"Prediction error details: {prediction_error}")
                print(f"Error type: {type(prediction_error)}")
                traceback.print_exc()  # This will print the full traceback to the logs
                return HttpResponseBadRequest(f"Prediction error: {prediction_error}. Please try again.")

            # Return the prediction result in the same page
            return render(request, 'predictor/predict.html', {
                'prediction': predicted_co2,
                'fuel_city': fuel_city,
                'fuel_hwy': fuel_hwy,
                'fuel_comb': fuel_comb,
                'fuel_mpg': fuel_mpg,
                'vehicle_model': vehicle_model
            })

        except Exception as e:
            # Log the complete exception traceback for debugging
            print(f"Unexpected error: {e}")
            traceback.print_exc()  # This will print the full traceback to the logs
            return HttpResponseBadRequest("An unexpected error occurred. Please try again later.")

    return render(request, 'predictor/predict.html')

def home(request):
    return render(request, 'home/home.html')  # Update the path to 'predictor/home.html'
