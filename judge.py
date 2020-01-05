import os
import re
import shutil
from model import MyModel


def judge(name):

    images_dir = "keras/train_all"
    inputs_dir = name + "_cutted"
    persons_dir = name
    categories = [name for name in os.listdir(images_dir) if name != ".DS_Store"]
    inputs = [name for name in os.listdir(inputs_dir) if name != ".DS_Store"]
    people = [name for name in os.listdir(persons_dir) if name != ".DS_Store"]

    # 入力画像の予測値
    predictions = MyModel().predict_from_dir(inputs_dir)

    # 結果出力
    strcategory = ""
    for category in categories:
        strcategory += category.ljust(11, " ")
    nameIndex = categories.index(name)
    print(strcategory)

    thePerson = []
    for i, input in enumerate(inputs):
        strprediction = input.ljust(28, " ")
        for prediction in predictions[i]:
            strprediction += str(round(prediction, 3)).ljust(10, " ")
        print(strprediction)
        if predictions[i][nameIndex] == 1.0:
            number = re.sub("\\D", "", input)
            if number not in thePerson:
                thePerson.append(number)

    print(len(thePerson))

    for person in people:
        person_number = re.sub("\\D", "", person)
        for p in thePerson:
            if p == person_number:
                save_path = "data/" + name
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                # shutil.move(persons_dir + "/" + person, "data/" + name + "/")
                break


if __name__ == "__main__":
    name = "suda"
    judge(name)
