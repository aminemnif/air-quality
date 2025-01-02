from django.shortcuts import render
import joblib

model = joblib.load("C:/Users/ASUS/air-quality/wafa_emissions_trend/MLModels/xgboost_model.pkl")

def predict(request):
    return render(request, 'predictionForm.html')
