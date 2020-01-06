import rename
import cutting
import judge

if __name__ == "__main__":
    # 学習の際に使用した名前を入力
    name = "daiki"
    # 画像のフォーマットを入力
    image_format = ".jpg"
    # 画像の枚数を入力。（オーバーしてよい）
    limit = 1500
    rename.rename(name, image_format)
    cutting.cutting(name, image_format, limit)
    judge.judge(name)
