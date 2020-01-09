import glob
import os
import shutil


def rename(name, image_format):
    path = name + "/*"
    i = 1
    files = glob.glob(path)

    for file in files:
        os.rename(file, name + "/" + name + "2_" + str(i) + image_format)
        i += 1


def movedir(name):
    shutil.move(name, "keras/train_all")


if __name__ == "__main__":
    name = "aiba_cutted"
    image_format = ".jpg"
    rename(name, image_format)
    # movedir(name)
