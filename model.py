# -*- coding: utf-8 -*-
import os
import gc
import numpy as np
import random
import math
import traceback
from PIL import Image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils

import matplotlib.pyplot as plt


class Model:
    def __init__(self):
        print(os.getcwd())
        self.images_dir = "keras/train_all"
        self.hdf5_file = "keras/Model.hdf5"
        self.sub_dir = [
            name for name in os.listdir(self.images_dir) if name != ".DS_Store"
        ]

    # ------------------------------------
    # 学習モデルの作成と保存
    # ------------------------------------
    def save_model(self):
        try:
            # 画像読み込み
            train_data = []
            for i, sdir in enumerate(self.sub_dir):
                print("->", sdir)
                files = [
                    name
                    for name in os.listdir(self.images_dir + "/" + sdir)
                    if name != ".DS_Store"
                ]
                for f in files:
                    data = self.create_data_from_image(
                        self.images_dir + "/" + sdir + "/" + f
                    )
                    train_data.append([data, i])

            # シャッフル
            random.shuffle(train_data)
            X, Y = [], []
            for data in train_data:
                X.append(data[0])
                Y.append(data[1])

            test_idx = math.floor(len(X) * 0.8)
            xy = (
                np.array(X[0:test_idx]),
                np.array(X[test_idx:]),
                np.array(Y[0:test_idx]),
                np.array(Y[test_idx:]),
            )
            x_train, x_test, y_train, y_test = xy

            # 正規化
            self.x_train = x_train.astype("float") / 256
            self.x_test = x_test.astype("float") / 256
            self.y_train = np_utils.to_categorical(y_train, len(self.sub_dir))
            self.y_test = np_utils.to_categorical(y_test, len(self.sub_dir))

            # 学習モデルの保存
            model = self.create_model_from_shape(self.x_train.shape[1:])
            fit = model.fit(
                self.x_train,
                self.y_train,
                batch_size=64,
                epochs=15,
                validation_split=0.2,
            )
            model.save_weights(self.hdf5_file)

            # テスト
            score = model.evaluate(self.x_test, self.y_test)
            print("loss=", score[0])
            print("accuracy=", score[1])

            # グラフ描画
            loss = fit.history["loss"]
            val_loss = fit.history["val_loss"]
            nb_epoch = len(loss)
            plt.plot(range(nb_epoch), loss, marker=".", label="loss")
            plt.plot(range(nb_epoch), val_loss, marker=".", label="val_loss")
            plt.legend(loc="best", fontsize=10)
            plt.grid()
            plt.xlabel("epoch")
            plt.ylabel("loss")
            plt.show()

        except Exception as e:
            print("Exception:", traceback.format_exc(), e.args)

    # ------------------------------------
    # 入力画像の予測
    # ------------------------------------
    def predict_from_dir(self, dir):
        X = []
        files = [name for name in os.listdir(dir) if name != ".DS_Store"]
        for f in files:
            data = self.create_data_from_image(os.path.join(dir, f))
            X.append(data)
        X = np.array(X)
        model = self.create_model_from_shape(X.shape[1:])
        model.load_weights(self.hdf5_file)
        predictions = model.predict(X)
        return predictions

    # 画像ファイルからデータを作成
    def create_data_from_image(self, file):
        img = Image.open(file)
        img = img.convert("RGB")
        img = img.resize((50, 50))
        data = np.asarray(img)
        return data

    # Shape から Model の作成
    def create_model_from_shape(self, shape):
        model = Sequential()

        # 畳み込み層
        # 一層目
        model.add(Conv2D(32, 3, 3, border_mode="same", input_shape=shape))
        model.add(Activation("relu"))

        # 二層目
        model.add(Conv2D(32, 3, 3, border_mode="same"))
        model.add(Activation("relu"))

        # プーリング層の追加
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # ドロップアウト。サンプルと同数値
        model.add(Dropout(0.25))

        # 三層目
        model.add(Conv2D(64, 3, 3, border_mode="same"))
        model.add(Activation("relu"))

        # 四層目
        model.add(Conv2D(64, 3, 3, border_mode="same"))
        model.add(Activation("relu"))

        # プーリング層
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # ドロップアウト
        model.add(Dropout(0.5))

        # # 五層目
        # model.add(Conv2D(128, 3, 3, border_mode="same"))
        # model.add(Activation("relu"))

        # # 六層目
        # model.add(Conv2D(128, 3, 3, border_mode="same"))
        # model.add(Activation("relu"))

        # # プーリング層
        # model.add(MaxPooling2D(pool_size=(2, 2)))
        # # ドロップアウト
        # model.add(Dropout(0.5))

        # 平坦化する
        model.add(Flatten())

        # 全結合層
        model.add(Dense(512))
        model.add(Activation("relu"))
        # ドロップアウト
        model.add(Dropout(0.5))

        # 分類の数
        model.add(Dense(len(self.sub_dir)))
        model.add(Activation("softmax"))

        model.compile(
            loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        return model


if __name__ == "__main__":
    m = Model()
    m.save_model()
    gc.collect()
