import numpy as np
import flask
from flask_cors import CORS
import joblib
import pandas as pd
import requests
from tensorflow.keras.models import load_model

# Flask application initialization
app = flask.Flask(__name__)
CORS(app)
model = None
scaler = None
PREDICTION_SERVICE_URL = 'https://btc-predictor-mibdbzxdia-uc.a.run.app/v1/models/model:predict'

def load_model_and_scaler():
    global scaler
    scaler = joblib.load('scaler.gz')

def preprocess_input(data):
    """Preprocess the input data and return scaled features."""
    features = ['Close', 'Adj Close', 'Volume', 'Open', 'High', 'Low', 'Close Future']
    data_df = pd.DataFrame(data)
    data_df = data_df[features].dropna()
    
    # Scale the input data using the loaded scaler
    scaled_data = scaler.transform(data_df)
    
    return scaled_data

@app.route('/predict', methods=['POST'])
def predict():
    response = {"success": False}
    
    try:
        json_data = flask.request.get_json()
        if not json_data:
            response['error'] = "No JSON data received"
            return flask.jsonify(response)
        
        input_data = json_data.get('data')
        scaled_input = preprocess_input(input_data)
        
        sequences = np.array([scaled_input])

        res = requests.post(PREDICTION_SERVICE_URL, json={"instances": sequences.tolist()})
        res.raise_for_status()  # Check for unsuccessful responses
        
        predictions = res.json().get('predictions')
        inverse_transformed_predictions = scaler.inverse_transform(predictions)
        
        response["success"] = True
        response["predictions"] = inverse_transformed_predictions.tolist()
        
    except Exception as e:
        # Handle any exceptions that occur and provide useful error information
        response["error"] = str(e)
    
    return flask.jsonify(response)

if __name__ == "__main__":
    # Load the model and scaler at startup
    print("* Loading Keras model and starting Flask server. Please wait...")
    load_model_and_scaler()
    
    # Start the Flask server on a specific host and port (e.g.,
