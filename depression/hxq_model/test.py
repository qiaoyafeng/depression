import os

from tensorflow.keras.callbacks import Callback
import pandas as pd
import random
import numpy as np
import math
import matplotlib
from matplotlib import pyplot as plt

import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras import backend as K
from tensorflow.keras.layers import LeakyReLU, Conv1D, Dense
from tcn import TCN, tcn_full_summary
from sklearn.metrics import mean_squared_error  # 均方误差
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import Input, Model, Sequential
from tensorflow.keras.callbacks import ModelCheckpoint

matplotlib.use("TkAgg")


def rmse(y_pred, y_true):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))


if __name__ == "__main__":
    checkpoint_filepath = r"E:\myworkspace\depression\depression\hxq_model\qiao_vidio_1.keras"
    tcn = tf.keras.models.load_model(
        checkpoint_filepath, custom_objects={"TCN": TCN, "rmse": rmse}
    )

    print("*" * 30)
    tcn.summary()
    print("*" * 30)

    path = (
        r"E:\myworkspace\depression\depression\hxq_model\daic_woz_dataset\hdr\303_0.csv"
    )
    df = pd.read_csv(path, index_col=0)
    print(f"df shape: {df.shape}")
    time_step = 30
    x_Test = []
    j = 0
    while j + time_step < df.shape[0]:
        x_Test.append(df.iloc[j : j + time_step, :])
        j = j + time_step

    X_TEST = [x.values for x in x_Test]
    x_test = np.array(X_TEST)
    print(f"x_test shape: {x_test.shape}")

    predict = tcn.predict(x_test)
    print(f"predict: {predict}, len: {len(predict)}")

    # default model

    default_tcn = tf.keras.models.load_model(
        "E:/myworkspace/depression/depression/back/vidio_1.h5",
        custom_objects={"TCN": TCN, "mse": "mse"},
    )
    print("*" * 50)
    default_tcn.summary()
    print("*" * 50)

    d_predict = default_tcn.predict(x_test)
    print(f"d_predict: {d_predict}, len: {len(d_predict)}")

