from utils import scale_value, to_sequences
import numpy as np
import flask
from flask_cors import CORS
import joblib
import pandas as pd
import requests

app = flask.Flask(__name__)
CORS(app)
model = None
scaler = None
url = 'https://btc-predictor-mibdbzxdia-uc.a.run.app/v1/models/model:predict'

def load_scaler():
    global scaler
    scaler = joblib.load('scaler.gz')

def preprocess_input(data):
    features = ['Close', 'Adj Close', 'Volume', 'Open', 'High', 'Low', 'Close Future']
    data_df = pd.DataFrame(data)
    data_df = data_df[features].dropna()
    scaled_data = scaler.transform(data_df)
    
    return scaled_data

@app.route('/predict', methods=['POST'])
def predict():
    data = {"success": False}

    if flask.request.method == "POST":
        json_data = flask.request.get_json()
        if json_data:
            try:
                input_data = json_data.get('data')
                scaled_input = preprocess_input(input_data)
                
                sequences = np.array([scaled_input])

                res = requests.post(url, json={"instances": sequences.tolist()})
                res.raise_for_status()  # Check for unsuccessful responses
                
                predictions = res.json().get('predictions')
                inverse_transformed_predictions = scaler.inverse_transform(predictions)
                
                response["success"] = True
                response["predictions"] = inverse_transformed_predictions.tolist()

                data['prediction'] = predictions
                data["success"] = True
                data['sig'] = 'BTC'
            except Exception as e:
                data['error'] = str(e)
        else:
            data['error'] = "No JSON data received"
    else:
        data['error'] = "Invalid HTTP method"

    return flask.jsonify(data)

if __name__ == "__main__":
    print("* Loading Keras model and starting Flask server. Please wait...")
    load_scaler()
    app.run()
