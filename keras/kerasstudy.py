from keras.datasets import mnist
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense

# x_trainには手書き画像、 y_trainには正解の数値が入ってる
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# print(x_train[0])別ファイルに保存した
# 画像を一次元化 60000_28_28だったものを60000_784の配列に
# reshapeについて https://note.nkmk.me/python-numpy-reshape-usage/
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)

# 画素を0~1の範囲になるように255で割る
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# 正解ラベルをone-hot-encoding
# 参考 https://analytics-note.xyz/machine-learning/keras-to-categorical/
y_train = to_categorical(y_train, 10)

y_test = to_categorical(y_test, 10)

# モデルを構築
model = Sequential()
model.add(Dense(64, activation="relu", input_dim=784))
model.add(Dense(10, activation="softmax"))
model.compile(
    optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"]
)

model.fit(x_train, y_train, batch_size=100, epochs=12, verbose=1)
score = model.evaluate(x_test, y_test)
print(score[0])
print(score[1])
