import os
import joblib
import numpy as np
from django.shortcuts import render
from django.http import HttpResponseBadRequest

# Paths to your model and scaler files
CLASSIFIER_PATH = 'bassem_classification/ml_models/rf_classification_model.pkl'
SCALER_PATH = 'bassem_classification/ml_models/robust_scaler.pkl'

# Check if files exist
if not os.path.exists(CLASSIFIER_PATH):
    raise FileNotFoundError(f"Classification model not found at {CLASSIFIER_PATH}")
if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler file not found at {SCALER_PATH}")

# Load the model and scaler
classifier_model = joblib.load(CLASSIFIER_PATH)
scaler = joblib.load(SCALER_PATH)
print(f"bassem classification - Classification model loaded: {classifier_model}")
print(f"bassem classification - Scaler loaded: {scaler}")

# Features used by the classification model
CLASSIFICATION_FEATURES = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'CO', 'SO2', 'O3', 'Toluene'
]

# All features expected by the scaler
ALL_FEATURES = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'CO', 'SO2', 'O3', 'Toluene', 'Benzene', 'NH3', 'city_encoded'
]

CLASS_LABELS = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']

# Color mapping for each class
COLOR_MAPPING = {
    'Good': 'green',
    'Satisfactory': 'lightgreen',
    'Moderate': 'yellow',
    'Poor': 'orange',
    'Very Poor': 'red',
    'Severe': 'darkred'
}


# Classification prediction view
def predict(request):
    if request.method == 'POST':
        try:
            print(f"bassem classification - Form data: {request.POST}")

            # Retrieve each input separately
            pm25 = request.POST.get('pm25', '').strip()
            pm10 = request.POST.get('pm10', '').strip()
            no = request.POST.get('no', '').strip()
            no2 = request.POST.get('no2', '').strip()
            nox = request.POST.get('nox', '').strip()
            co = request.POST.get('co', '').strip()
            so2 = request.POST.get('so2', '').strip()
            o3 = request.POST.get('o3', '').strip()
            toluene = request.POST.get('toluene', '').strip()

            # Validate and convert inputs to floats
            try:
                input_features = [
                    float(pm25), float(pm10), float(no), float(no2), float(nox),
                    float(co), float(so2), float(o3), float(toluene)
                ]
                print(f"bassem classification - Input features from form: {input_features}")
            except ValueError:
                return HttpResponseBadRequest("All fields must contain valid numeric values.")

            # Fill missing features (Benzene, NH3, city_encoded) with 0
            all_features = input_features + [0, 0, 0]  # Add Benzene, NH3, and city_encoded
            print(f"bassem classification - All features (with zeros): {all_features}")

            # Prepare input for scaling
            input_array = np.array([all_features])
            print(f"bassem classification - Input array before scaling: {input_array}")

            # Scale the input features
            try:
                scaled_features = scaler.transform(input_array)
                print(f"bassem classification - Scaled features: {scaled_features}")
            except Exception as e:
                print(f"bassem classification - Scaler error: {e}")
                return HttpResponseBadRequest("An error occurred during feature scaling. Please try again.")

            # Remove extra features (Benzene, NH3, city_encoded) before prediction
            filtered_scaled_features = scaled_features[:, :len(CLASSIFICATION_FEATURES)]
            print(f"bassem classification - Filtered scaled features: {filtered_scaled_features}")

            # Make the prediction
            try:
                prediction_encoded = classifier_model.predict(filtered_scaled_features)[0]
                print(f"bassem classification - Classification encoded result: {prediction_encoded}")
                
                # Map the encoded class to the actual class name
                predicted_class_name = CLASS_LABELS[int(prediction_encoded)]
                print(f"bassem classification - Classification Class Name: {predicted_class_name}")

                # Get the color associated with the predicted class
                prediction_color = COLOR_MAPPING.get(predicted_class_name, 'black')  # Default color is black if not found

            except Exception as e:
                print(f"bassem classification - Classification error: {e}")
                return HttpResponseBadRequest("An error occurred during classification. Please try again.")

            # Render the result in the template
            return render(request, 'predict_classification.html', {
                'prediction': predicted_class_name,
                'prediction_color': prediction_color,
                'input_data': {
                    'PM2.5': pm25, 'PM10': pm10, 'NO': no, 'NO2': no2,
                    'NOx': nox, 'CO': co, 'SO2': so2, 'O3': o3, 'Toluene': toluene
                }
            })

        except Exception as e:
            print(f"bassem classification - Unexpected error: {e}")
            return HttpResponseBadRequest("An unexpected error occurred. Please try again later.")

    # Render the blank form for GET requests
    return render(request, 'predict_classification.html', {
        'features': CLASSIFICATION_FEATURES
    })
