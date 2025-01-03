import os
import pickle

# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'trained_model.pkl')

def load_model():
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    return model
