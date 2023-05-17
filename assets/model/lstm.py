import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def prediction(req, model):
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime(2021, 12, 31)
    data = yf.download(req, start, end)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    prediction_days = 60
    x_train, y_train = [], []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    if x_train.shape[0] == 0:
        return "NA"
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model.fit(x_train, y_train, batch_size=32, epochs=25)

    test_start = dt.datetime(2022, 1, 1)
    test_end = dt.datetime.now()
    test_data = yf.download(req, test_start, test_end)
    actual_prices = test_data['Close'].values

    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.fit_transform(model_inputs)

    x_test = [
        model_inputs[x - prediction_days:x, 0]
        for x in range(prediction_days, len(model_inputs))
    ]
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)

    req = req.split('-')[0]
    plt.figure(figsize=(12,5))
    plt.plot(actual_prices, color='black', label='actual prices')
    plt.plot(prediction_prices, color='green', label='predicted prices')
    plt.title(f'{req} price prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.savefig(f'./../../img/{req}.png')

    real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs) + 1, 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)

    return prediction[0][0]


# Create the model outside the prediction function
model = create_model((None, 1))
