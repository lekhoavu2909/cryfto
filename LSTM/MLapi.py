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

def prepare_predict(close_price):
    return close_price

@app.route('/predict', methods=['POST'])
def predict():
    data = {"success": False}

    if flask.request.method == "POST":
        json_data = flask.request.get_json()
        if json_data:
            try:
                df = pd.DataFrame.from_dict(json_data)
                close_prices = df['data'].values
                scaled_close = scale_value(scaler, close_prices)
                sequences = to_sequences(scaled_close, len(df) // 2)

                # Batch prediction requests
                res = requests.post(url, json={"instances": sequences.tolist()})
                res.raise_for_status()  # Raise HTTPError for unsuccessful responses
                predictions = scaler.inverse_transform(res.json()['predictions']).tolist()

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
