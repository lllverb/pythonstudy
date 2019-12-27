import os
import glob

path = "./myphotos"
files = glob.glob(path + "/*")

for i, f in enumerate(files, 1):
    os.rename(f, os.path.join(path, str(i) + "_" + "daiki.jpg"))
