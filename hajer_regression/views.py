from django.shortcuts import render
import joblib
import numpy as np

# Load the trained model and scaler
model = joblib.load("D:/ESPRIT/3eme Ai/semestre 1/Projet datawarehouse/DATA Science/hajer ayadi/supervised/random_forest_model_regression.pkl")  # Replace with your model path
scaler_features = joblib.load("D:/ESPRIT/3eme Ai/semestre 1/Projet datawarehouse/DATA Science/hajer ayadi/supervised/scaler.pkl")  # Replace with your scaler path
# Define mappings for encoding
station_mapping = {
    'Background': 0, 'Industrial': 1, 'Residential and Commercial': 2, 'Rural': 3,
    'Suburban': 4, 'Traffic': 5, 'Traffic, Fond Urbain': 6, 'Urban': 7,
    'Urban Traffic, Residential And Commercial Area': 8, 'Urban Traffic/Residential': 9,
    'Urban, Industrial': 10, 'Urban, Industrial, Rural': 11, 'Urban, Rural': 12,
    'Urban, Suburban': 13, 'Urban, Suburban, Rural': 14
}
pollutant_mapping = {
    'NO2': 0, 'PM10': 1, 'PM2.5': 2
}

def regression_concentration(request):
    predictions = None
    if request.method == 'POST':
        try:
            # Retrieve user inputs
            type_of_station = request.POST.get('type_of_station')
            type_of_pollutant = request.POST.get('type_of_pollutant')
            longitude = float(request.POST.get('longitude', 0.0))
            latitude = float(request.POST.get('latitude', 0.0))
            population = float(request.POST.get('population', 0.0))
            year = int(request.POST.get('year', 2022))  # Default to 2022 if not provided

            # Encode categorical variables
            type_of_station_encoded = station_mapping.get(type_of_station, -1)
            type_of_pollutant_encoded = pollutant_mapping.get(type_of_pollutant, -1)

            # Ensure valid encoding
            if type_of_station_encoded == -1 or type_of_pollutant_encoded == -1:
                raise ValueError("Invalid station or pollutant type selected.")

            # Prepare the feature list for prediction
            features = [type_of_station_encoded, longitude, latitude, type_of_pollutant_encoded, population, year]
            features_scaled = scaler_features.transform(np.array(features).reshape(1, -1))

            # Generate predictions
            prediction = model.predict(features_scaled)[0]
            predictions = {'pollutants_concentration': prediction}

        except Exception as e:
            print(f"Error during prediction: {e}")

    context = {
        'predictions': predictions,
        'stations': list(station_mapping.keys()),
        'pollutants': list(pollutant_mapping.keys()),
    }
    print(request.POST)
    print(f"Predictions: {predictions}")
    return render(request, 'regression_concentration.html', context)
