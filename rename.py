import os
import glob

path = "./myphotos"
files = glob.glob(path + "/*")

for i, f in enumerate(files, 1):
    os.rename(f, os.path.join(path, "{0:03d}".format(i) + "_" + "daiki.jpg"))
