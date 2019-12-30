import os
import glob

path = "./cutted/daiki_cutted"
files = glob.glob(path + "/*")

for i, f in enumerate(files, 1):
    os.rename(f, os.path.join(path, "daiki_cutted_" + str(i) + ".jpg"))
