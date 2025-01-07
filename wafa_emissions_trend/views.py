from django.shortcuts import render
import joblib
import numpy as np

# Load the trained model and scalers
model = joblib.load("wafa_emissions_trend/MLModels/xgboost_model.pkl")
scaler_features = joblib.load("wafa_emissions_trend/MLModels/scaler_features.pkl")
scaler_target = joblib.load("wafa_emissions_trend/MLModels/scaler_target.pkl")

def predict(request):
    predictions = None
    if request.method == 'POST':
        try:
            # Define the expected features for the scaler (2002 to 2022)
            scaler_features_range = [f'emissions_{year}' for year in range(2002, 2023)]  # Includes 2002–2022
            user_input_range = [f'emissions_{year}' for year in range(2004, 2023)]  # User inputs 2004–2022

            # Debug: Print the expected feature ranges
            print("Scaler feature range (2002–2022):", scaler_features_range)
            print("User input feature range (2004–2022):", user_input_range)

            # Prepare emissions list with padding for 2002 and 2003
            emissions = [0.0, 0.0]  # Padding for 2002 and 2003
            for feature in user_input_range:
                value = request.POST.get(feature, None)
                if value is None or value.strip() == "":
                    emissions.append(0.0)  # Use default value for missing fields
                else:
                    emissions.append(float(value.replace(',', '.')))  # Normalize input (replace ',' with '.')

            # Debug: Print the raw input data and its length
            print("Raw input data from user (with padding for 2002–2003):", emissions)
            print("Input length before scaling:", len(emissions))

            # Ensure input size matches the scaler's expectation
            if len(emissions) != len(scaler_features_range):
                raise ValueError("Input size mismatch. Please ensure all required fields are provided.")

            # Scale the features using RobustScaler
            emissions_scaled = scaler_features.transform(np.array(emissions).reshape(1, -1))

            # Debug: Print the scaled input
            print("Scaled input for RobustScaler:", emissions_scaled)

            # Extract only model features (2004–2022) from scaled input
            model_input = emissions_scaled[:, 2:]  # Skip 2002 and 2003

            # Debug: Print trimmed input for the model
            print("Trimmed input for model (2004–2022):", model_input)

            # Number of years to predict
            num_years = int(request.POST.get('num_years', 1))

            # Debug: Print the number of years to predict
            print("Number of future years to predict:", num_years)

            # Generate predictions
            predictions = {}
            for i in range(num_years):
                # Predict the scaled value for the next year
                prediction_scaled = model.predict(model_input)[0]

                # Debug: Print scaled prediction for the year
                print(f"Scaled prediction for year {2023 + i}:", prediction_scaled)

                # Inverse transform the scaled prediction using scaler_target
                prediction = scaler_target.inverse_transform([[prediction_scaled]])[0][0]

                # Debug: Print the inverse-transformed prediction
                print(f"Inverse-transformed prediction for year {2023 + i}:", prediction)

                predictions[2023 + i] = prediction

                # Update the input for the next prediction
                # Append the scaled prediction directly (already scaled)
                model_input = np.append(model_input, [[prediction_scaled]], axis=1)
                model_input = model_input[:, 1:]  # Slide window to keep the size consistent

                # Debug: Print updated input for the model after sliding
                print(f"Updated model input after sliding for year {2023 + i}:", model_input)

        except Exception as e:
            # Debug: Log the error message
            print(f"Error during prediction: {e}")
    
    # Pass context to template
    context = {
        'predictions': predictions,
        'years': range(2004, 2023),  # Adjust range for input fields
    }

    # Debug: Print final predictions before rendering the template
    print("Final predictions:", predictions)

    return render(request, 'predictionForm.html', context)



def clustering_detail(request):
    return render(request, 'clusteringDetail.html')

def association_detail(request):
    return render(request, 'associationDetail.html')