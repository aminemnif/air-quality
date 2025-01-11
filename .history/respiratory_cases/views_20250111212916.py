from django.shortcuts import render
from .utils import load_model

# Load the model once when the server starts
model = load_model()

def predict_view(request):
    if request.method == 'POST':
        try:
            # Get input values from the form
            aqi = float(request.POST.get('aqi'))
            pm10 = float(request.POST.get('pm10'))
            o3 = float(request.POST.get('o3'))
            temperature = float(request.POST.get('temperature'))
            humidity = float(request.POST.get('humidity'))

            # Input data for the model
            input_data = [[aqi, pm10, o3, temperature, humidity]]

            # Make prediction
            prediction = model.predict(input_data)[0]

            # Render the template with the prediction
            return render(request, 'predict_form.html', {
                'prediction': prediction
            })
        except Exception as e:
            # Handle errors gracefully
            return render(request, 'predict_form.html', {
                'error': 'An error occurred while making the prediction. Please check your inputs.',
                'aqi': request.POST.get('aqi'),
                'pm10': request.POST.get('pm10'),
                'o3': request.POST.get('o3'),
                'temperature': request.POST.get('temperature'),
                'humidity': request.POST.get('humidity')
            })

    # Render the form for GET requests
    return render(request, 'predict_form.html')

def clustering_RS(request):
    return render(request, 'clustering.html')

def associationR(request):
    return render(request, 'clustering.html')
