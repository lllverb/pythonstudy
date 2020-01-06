import cv2
import os


def cutting(name, image_format, limit):
    # 先ほど集めてきた画像データのあるディレクトリ
    input_data_path = name + "/"
    # 切り抜いた画像の保存先ディレクトリ(予めディレクトリを作っておいてください)
    save_path = name + "_cutted/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # OpenCVのデフォルトの分類器のpath。(https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xmlのファイルを使う)
    cascade_path = "/usr/local/Cellar/opencv/4.1.2/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascade_path)

    # 収集した画像の枚数(任意で変更)
    image_count = limit
    # 顔検知に成功した数(デフォルトで0を指定)
    face_detect_count = 1

    # 集めた画像データから顔が検知されたら、切り取り、保存する。
    for i in range(1, image_count):
        img = cv2.imread(input_data_path + name + "_" + str(i) + image_format)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(
            gray, scaleFactor=1.11, minNeighbors=3, minSize=(60, 60)
        )
        label = "a"
        # print(img)
        if len(face) > 0:
            for rect in face:
                # ///////////////////////////////
                # 顔認識部分を赤線で囲み保存(今はこの部分は必要ない)
                # cv2.rectangle(
                #     img,
                #     tuple(rect[0:2]),
                #     tuple(rect[0:2] + rect[2:4]),
                #     (0, 0, 255),
                #     thickness=1,
                # )
                # cv2.imwrite("detected.jpg", img)
                # ////////////////////////////////
                x = rect[0]
                y = rect[1]
                w = rect[2]
                h = rect[3]
                cv2.imwrite(
                    save_path + str(i) + "_" + name + "_cutted_" + label + image_format,
                    img[y : y + h, x : x + w],
                )
                face_detect_count += 1
                label = getNewLabel(label)
        else:
            print(name + str(i) + ":NoFace")


def getNewLabel(label):
    newlabel = ""
    for s in label:
        # アスキーコードに変換
        s = ord(s)
        if 65 <= s and s <= 90:
            s = s + 1
        elif 97 <= s and s <= 122:
            s = s + 1
        # アスキーコードから文字を取得
        s = chr(s)
        newlabel += s
    return newlabel


if __name__ == "__main__":
    # name = "d"
    image_format = ".jpg"
    limit = 1000
    cutting(name, image_format, limit)

