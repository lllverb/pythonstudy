import os
import glob

path = "./cutted_myphotos"
files = glob.glob(path + "/*")

for i, f in enumerate(files, 1):
    os.rename(f, os.path.join(path, "daiki_" + str(i) + ".jpg"))
