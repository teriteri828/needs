from dataclasses import dataclass
import numpy as np
import glob
from const import  USE_URL, NUM_CLASSES

import tensorflow_hub as hub
import tensorflow_text
from sklearn.model_selection import train_test_split
import keras

embed = hub.load(USE_URL)

@dataclass
class LearnDataSplit:
    def execute(self, df_learn):
        num_classes = NUM_CLASSES

        tweets = df_learn["text"].values
        X = embed(tweets).numpy()
        y = df_learn["needs"].values
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=123, test_size=0.2
        )

        # ラベルデータを学習用に整形
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        return X_train, X_test, y_train, y_test

