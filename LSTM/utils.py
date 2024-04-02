import numpy as np
from sklearn.preprocessing import MinMaxScaler

def to_sequences(data, seq_len):
    d = []

    for index in range(len(data) - seq_len):
        d.append(data[index: index + seq_len])

    return np.array(d)

def preprocess(data_raw, seq_len, train_split):

    data = to_sequences(data_raw, seq_len)

    num_train = int(train_split * data.shape[0])

    X_train = data[:num_train, :-1, :]
    y_train = data[:num_train, -1, :]

    X_test = data[num_train:, :-1, :]
    y_test = data[num_train:, -1, :]

    return X_train, y_train, X_test, y_test


def scale_value(scaler, close_price):

    close_price = close_price.reshape(-1, 1)

    scaled_close = scaler.fit_transform(close_price)

    scaled_close = scaled_close[~np.isnan(scaled_close)]

    scaled_close = scaled_close.reshape(-1, 1)

    return scaled_close