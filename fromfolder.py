import rename
import cutting
import judge

if __name__ == "__main__":
    name = "daiki"
    image_format = ".jpg"
    limit = 1500
    # rename.rename(name, image_format)
    cutting.cutting(name, image_format, limit)
    judge.judge(name)
