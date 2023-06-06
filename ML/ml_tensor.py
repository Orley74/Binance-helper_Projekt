from sklearn.model_selection import train_test_split

import tensorflow as tf
import pandas as pd
import tensorflow_io as tfio
from Binance.binance_api import *

model = tf.keras.models.Sequential([

    tf.keras.layers.Dense(24, activation="relu", input_shape=(2,)),
    tf.keras.layers.Dense(1, activation=None)

])
model.run_eagerly = True
model.compile(loss=tf.keras.losses.mae,
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              metrics=['accuracy'])

def Train_set(model: tf.keras.models.Sequential):

    cryptos = ["BTC","ETH", "NEO", 'GNO' ,  "XNO", "JOE", "NMR", "RPL", "SNT", "AUD","BAL", "YFI", "SOL", "MATIC", "GNO"]

    for x in cryptos:

        try:
            data = pd.read_csv(f"clines_data_{x}")
            data_VWAP = tf.convert_to_tensor(VWAP(x),dtype=tf.float32)

        except(FileNotFoundError):
            get_data(x)
            data = pd.read_csv(f"clines_data_{x}")
            data_VWAP = tf.convert_to_tensor(VWAP(x), dtype=tf.float32)
        except:
            continue
        data_close = tf.convert_to_tensor(data['close'].head(data_range), dtype=tf.float32)

        data_open = tf.convert_to_tensor(data['open'].head(data_range), dtype=tf.float32)

        first_index = data_close/data_VWAP
        second_index = data_open/data_close
        future = data_open[1:]/data_close[1:]
        last_ind = data_open[-1]/data_close[-1]
        pred = tf.concat([future, [last_ind]], axis=0)




        combined_input = tf.stack([first_index,second_index], axis=1)
        #print(pred)
        #print(combined_input)
        model.fit(combined_input,pred,epochs=1000)


def check_ml (model: tf.keras.models.Sequential):
    symbol = "BTC"
    data = pd.read_csv(f"clines_data_{symbol}")

    data_close = tf.convert_to_tensor(data['close'].head(data_range), dtype=tf.float32)

    data_open = tf.convert_to_tensor(data['open'].head(data_range), dtype=tf.float32)
    data_VWAP = tf.convert_to_tensor(VWAP(symbol), dtype=tf.float32)
    first_index = data_close / data_VWAP
    second_index = data_open / data_close
    future = data_open[1:] / data_close[1:]
    last_ind = data_open[-1] / data_close[-1]
    pred = tf.concat([future, [last_ind]], axis=0)

    combined_input = tf.stack([first_index, second_index], axis=1)
    # print(pred)
    # print(data_y)
    result = model.predict(combined_input)
    print(result)
    for i in range(data_range):

        print(result[i])
        temp_avg = result[i]
        #print(temp_avg)
        predicted = temp_avg*data_close[i]

        if predicted>data_close[i+1]:
            accuracy = data_close[i+1]/predicted * 100
        else:
            accuracy = predicted/data_close[i+1] * 100
        print(f"real:   {data_close[i]}, next real value:   {pred[i]}, predict: {predicted}, accuracy:   {accuracy}")
        # accuracy = result[i]

def predict_future(model: tf.keras.models.Sequential):
    symbol = "BTC"
    data_x = VWAP(symbol)
    data = pd.read_csv(f"clines_data_{symbol}")
    data_y = data['close'].head(data_range)
    last_price = data_y[0]
    data_x = data_x.astype('float32')
    data_y = data_y.astype('float32')
    new_data_table = []
    print(last_price)
    change_price = model.predict((last_price,))
    print(change_price)
    #for i in range(9):

#Train_set(model)


