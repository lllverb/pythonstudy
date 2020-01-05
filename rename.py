import glob
import os
import shutil


def rename(name, image_format):
    path = name + "/*"
    i = 1
    files = glob.glob(path)

    for file in files:
        os.rename(file, name + "/" + name + "_" + str(i) + image_format)
        i += 1


def movedir(name):
    shutil.move(name, "keras/train_all")


if __name__ == "__main__":
    name = "daiki"
    image_format = ".jpg"
    rename(name, image_format)
    # movedir(name)
