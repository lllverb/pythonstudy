# -*- coding: utf-8 -*-
# import sys
import os

# import numpy as np
# import pandas as pd
# from PIL import Image
from model import MyModel

images_dir = "./train"
inputs_dir = "./test/daiki"
categories = [name for name in os.listdir(images_dir) if name != ".DS_Store"]
inputs = [name for name in os.listdir(inputs_dir) if name != ".DS_Store"]

# 入力画像の予測値
predictions = MyModel().predict_from_dir(inputs_dir)

# 結果出力
strcat = ""
for cat in categories:
    strcat += cat.ljust(10, " ")
print("             ", strcat)

for i, input in enumerate(inputs):
    strpre = input.ljust(14, " ")
    for pre in predictions[i]:
        strpre += str(round(pre, 3)).ljust(10, " ")
    print(strpre)