from utils import scale_value, to_sequences
import numpy as np
import flask
from flask_cors import CORS
import joblib
import pandas as pd
import requests
import codecs, json 
from json import JSONEncoder

app = flask.Flask(__name__)
app.debug = True
CORS(app)
model = None
scaler = None
url = 'https://btc-predictor-mibdbzxdia-uc.a.run.app/v1/models/model:predict'

def load_scaler():
    global scaler
    global scaler_y
    scaler = joblib.load('scaler.gz')
    scaler_y = joblib.load('scaler_y.gz')

def preprocess_input(data):
    features = ['Close', 'Adj Close', 'Volume', 'Open', 'High', 'Low']
    data_df = pd.DataFrame(data)
    data_df = data_df[features].dropna()
    scaled_data = scaler.transform(data_df)

    return scaled_data

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

@app.route('/predict', methods=['POST'])
def predict():
    data = {"success": False}

    if flask.request.method == "POST":
        json_data = flask.request.get_json()
        if json_data:
            try:
                input_data = json_data.get('data')
                scaled_input = preprocess_input(input_data)
                rescaled_data = scaled_input.reshape(scaled_input.shape[0], scaled_input.shape[1], 1)
                res = requests.post(url, json={
                    "instances":rescaled_data.tolist()
                })
                # res.raise_for_status()  # Check for unsuccessful responses
                
                predictions = res.json().get('predictions')
                inverse_transformed_predictions = scaler_y.inverse_transform(predictions)
                
                print(predictions)

                data["success"] = True
                data["predictions"] = inverse_transformed_predictions.tolist()

                # data['prediction'] = predictions
                # data["success"] = True
                data['sig'] = 'BTC'

                print(data["predictions"])
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
