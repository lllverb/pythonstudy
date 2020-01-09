# 背景

僕はよさこいを踊っている。よさこいのお祭りがあると LINE のアルバムや FACEBOOK に僕のチームの写真が 1000 枚以上アップロードされる。多いときには 5000 枚にも及ぶことがある。
とてもありがたいのだがその中から自分の写っている画像を探すのが少々めんどくさい。
そこで、大量の画像の中から自分の写っているものだけを検出して保存してくれる機能があったらなと考え製作に至った。

## 機能

### fromfolder.py(フォルダ内の画像の判定)

###### 機械学習は完了していることが前提。学習方法は後述。

1. 予め自分を検出したい大量の画像を「"自分の名前"」のディレクトリに入れておく。
2. 画像を 1 からナンバリングしてリネームする。
3. 顔を検出し切り取る。その際に、先ほどつけたナンバーを用いて切り取った画像を命名し新たなディレクトリで保存する。
4. 大量の切り取った顔画像の中から自分と一致するものがあればそのナンバーがついた元画像を別のディレクトリに移動する。

#### これで自分の写る画像だけが保存できる。

### scrape.py を実行（google 画像検索から画像を保存）

1. 「検索キーワード」「拡張子」「保存したい枚数」「保存したいディレクトリ」を入力
2. 上記の情報を持って Google 画像検索から画像を保存。
3. 保存した画像に数字を付けてリネーム。
4. そのまま顔検出から別ディレクトリで保存することも可能。

###### この他にも search.rb を実行することで Bing 画像検索から画像をスクレイピングすることもできる。

## 学習方法

1. scrape.py, search.rb などを利用して学習用画像を大量に集める。
2. 顔を切り出す。本人以外の画像は手動で取り除く。
3. 人物ごとにディレクトリに分けて保存し、model.py を実行。これで機械学習モデルが生成される。

##### また、テスト用画像で判定の際に違う人物と判定されてしまった画像は訓練用画像としてあらたに追加し、精度を高めていく。

###### 学習モデルのパラメータを変化させることでどのように精度に影響が出るかを確認するため、1 回 1 回学習結果を graph に出力。

- グラフの例

#### 過学習が起きている例。（20 回以降は val_loss が上昇傾向にある。）

![6layers_64_100](https://user-images.githubusercontent.com/54735495/71853546-1b4d0100-311f-11ea-86ee-68c73c660aa4.png)

#### 適切な学習回数の例。

![4layers_64_15-3](https://user-images.githubusercontent.com/54735495/71853297-3cf9b880-311e-11ea-88bd-c46ff0b5cfe3.png)

#### val_loss や loss の変化率を考え過学習のない適切なパラメータを考え設定していく。

最終的には「四階層, batch_size=64, epoch=15」 の model を使用して検証している。

# results

このような検証結果になりました。

## firsttake 試行錯誤中

| batch_size | epoch | loss               | accuracy           |
| :--------: | :---: | :----------------- | :----------------- |
|     32     |  10   | 1.2694765302625368 | 0.7467018365859985 |
|     32     |  15   | 1.5873039860209563 | 0.7427440881729126 |
|     32     |  20   | 1.4444659338148413 | 0.7744063138961792 |
|     32     |  100  |                    |                    |
|     64     |  10   | 1.0200651943840893 | 0.7559366822242737 |
|     64     |  15   | 1.2905355374228042 | 0.767810046672821  |
|     64     |  20   | 1.2161630937795211 | 0.7651715278625488 |
|     64     |  50   | 1.3925397633488792 | 0.7638691067695618 |

- (adam)

| batch_size | epoch | loss             | accuracy           |
| :--------: | :---: | :--------------- | :----------------- |
|     64     |  15   | 1.40646814324925 | 0.7427440881729126 |

## 層を六層目までふやした!!!epoch 増やせば精度上がりそう！！

| batch_size | epoch | loss               | accuracy           | drop           |
| :--------: | :---: | :----------------- | :----------------- | :------------- |
|     32     |  25   | 0.8929301673315446 | 0.7467018365859985 | 0.25, 0.5, 0.5 |
|     32     |  50   | 1.1711467218273233 | 0.7691292762756348 | 0.25, 0.5, 0.5 |
|     32     |  15   | 1.4784660285884283 | 0.7664907574653625 | 0.2, 0.2, 0.2  |
|     32     |  50   | 1.8228084006221439 | 0.751978874206543  | 0.2, 0.2, 0.2  |
|     32     |  100  | 1.3596595347438765 | 0.7704485654830933 | 0.25, 0.5, 0.5 |
|     64     |  15   | 0.9667450796645676 | 0.6978892087936401 | 0.25, 0.5, 0.5 |
|     64     |  20   | 0.9130814150958703 | 0.7361477613449097 | 0.25, 0.5, 0.5 |
|     64     |  50   | 0.9125874250104999 | 0.7981530427932739 | 0.25, 0.5, 0.5 |
|     64     |  100  | 1.5175847849933957 | 0.748021125793457  | 0.25, 0.5, 0.5 |

そうでもなかった。

- (dense100)

| batch_size | epoch | loss               | accuracy           | drop          |
| :--------: | :---: | :----------------- | :----------------- | :------------ |
|     32     |  50   | 0.8827118996265381 | 0.7757256031036377 | 0.2, 0.2, 0.2 |

- 学習する画像数を増やすことで精度の向上が見られる。
  一人ずつ画像増やしていく

#### imada

| name  | batch_size | epoch | loss               | accuracy           | drop          |
| :---: | :--------: | :---: | :----------------- | :----------------- | :------------ |
| imada |     32     |  15   | 1.4784660285884283 | 0.7664907574653625 | 0.2, 0.2, 0.2 |
| suda  |     32     |  15   | 1.1954077915396801 | 0.7545219659805298 | 0.2, 0.2, 0.2 |

### 一度に増やすことにする

検出に成功した数。分母はおおよそ 500

|   name    | 最初 | 変化後 |
| :-------: | :--: | :----: |
|   imada   |      |  345   |
|   suda    | 135  |  292   |
| hashimoto | 180  |  298   |
|  sakurai  | 189  |  267   |
|  kubota   | 141  |  280   |
| ishihara  | 276  |  376   |
|  nakajo   | 171  |  132   |

（nakajo 画像増やさなかった）

四層に変更

| batch_size | epoch | loss               | accuracy           | drop           |
| :--------: | :---: | :----------------- | :----------------- | :------------- |
|     64     |   8   | 0.9749638413389524 | 0.7112597823143005 | 0.25, 0.5, 0.5 |
|     64     |  10   | 0.9170258415887836 | 0.7380155920982361 | 0.25, 0.5, 0.5 |
|     64     |  12   | 0.9142108786863626 | 0.739130437374115  | 0.25, 0.5, 0.5 |
|     64     |  15   | 0.934751871736552  | 0.7580825090408325 | 0.25, 0.5, 0.5 |
|     64     |  15   | 0.964419063026383  | 0.7573964595794678 | 0.25, 0.5, 0.5 |
|     64     |  15   | 1.0660587813730698 | 0.7732160091400146 | 0.25, 0.5, 0.5 |
|     64     |  30   | 1.082860721667674  | 0.7881828546524048 | 0.25, 0.5, 0.5 |
|     64     |  30   | 1.5747375994663242 | 0.7212932109832764 | 0.25, 0.5, 0.5 |

# 最終結果

#### 自分の画像を LINE のアルバムから検出します。いくつかのパラメータで実験

|    アルバム名    | 本人の枚数（目視, opencv) | 保存した枚数 | 本人以外の枚数 | 切り出し size | minNeighbors |
| :--------------: | :-----------------------: | :----------: | :------------: | :-----------: | :----------: |
|   ディズニー 1   |          32, 28           |      24      |       4        |     60x60     |      2       |
|   ディズニー 1   |          32, 28           |      28      |       3        |     60x60     |      3       |
|   ディズニー 1   |          32, 24           |      20      |       2        |    120x120    |      3       |
|       日光       |          33, 29           |      37      |       6        |     60x60     |      2       |
|       日光       |          33, 29           |      29      |       3        |     60x60     |      3       |
|       日光       |          33, 22           |      19      |       0        |    120x120    |      3       |
|   ディズニー 2   |          30, 24           |      23      |       1        |     60x60     |      2       |
|   ディズニー 2   |          30, 24           |      22      |       1        |     60x60     |      3       |
|   ディズニー 2   |          30, 18           |      17      |       1        |    120x120    |      3       |
| ドリームよさこい |          38, 31           |      27      |       4        |     60x60     |      2       |
| ドリームよさこい |          38, 31           |      27      |       4        |     60x60     |      3       |
| ドリームよさこい |          38, 27           |      19      |       3        |    120x120    |      3       |

~~以下省略~~

## 結果からの考察

- opencv で顔を認証するところで大く loss が出てしまっている。
- 切り出しサイズ「60x60」では 20%前後、, 「120x120」25%~33%ほどの顔の見逃しがある。
- 学習結果モデルとの判別は 90%以上の精度が出ている。
- cutting.py の設定は「minNeighbors=3, minSize=(60, 60)」のときに精度が上がる。

## 結構やりたいことが実現できた！

#### opencv の顔検出の精度、機械学習の精度を高めていくことが今後の課題。
