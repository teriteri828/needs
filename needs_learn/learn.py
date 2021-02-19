from dataclasses import dataclass
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from const import NUM_CLASSES, SAVE_MODEL_PATH

class Learn:
    def _model_define(self,):

        # モデルの作成
        model = Sequential()
        model.add(Dense(1024, activation="relu", input_shape=(512,)))
        model.add(Dense(512, activation="relu"))
        model.add(Dense(NUM_CLASSES, activation="softmax"))

        model.compile(
            loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        return model

    def execute(self, X_train, X_test, y_train, y_test):
        print("X_train: {}".format(len(X_train))) 
        print("y_train: {}".format(len(y_train))) 
        print("X_test: {}".format(len(X_test))) 
        print("y_test: {}".format(len(y_test))) 

        model = self._model_define()
        # 学習
        early_stopping = EarlyStopping(monitor="val_loss", min_delta=0.0, patience=5,)

        history = model.fit(
            X_train,
            y_train,
            batch_size=1500,
            epochs=100,
            verbose=2,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping],
        )
        
        model.save(SAVE_MODEL_PATH)
        return True
