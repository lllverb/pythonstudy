import os
import glob

path = "./imada_img"
files = glob.glob(path + "/*")

for i, f in enumerate(files, 1):
    os.rename(f, os.path.join(path, "imada_" + str(i) + ".jpg"))
