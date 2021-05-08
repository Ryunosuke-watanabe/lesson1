import cv2
import numpy as np
import pandas as pd
import os
import pathlib
from var import List

feel = List.img_list

for item in feel:
    idir = 'img/ans/'
    odir = 'output/ans/'
    fname=item+""
    num_photo=10
    bgr = np.zeros((num_photo,4),dtype=object)
    # print(bgr)

    for k in range(num_photo):

        img = cv2.imread(idir + fname + '' + str(k+1) + '.jpg')  #1番からスタート
        print(idir + fname + '' + str(k+1) + '.jpg')
        h, w, c = img.shape #height, width, channnel

        #初期化
        l=0
        b_ave=0; g_ave=0; r_ave=0

        for i in range(h):
            for j in range(w):
                #画素値[0,0,0]（Black）を除外してピクセルの和とbgrの画素値の合計を計算する
                if(img[i,j,0] != 0 or img[i,j,1] != 0 or img[i,j,2] != 0 ):
                    l+=1    #対象となるピクセル数を計算する
                    #対象となるピクセルの画素値の和を計算する
                    b_ave=b_ave+img[i,j,0]
                    g_ave=g_ave+img[i,j,1]
                    r_ave=r_ave+img[i,j,2]

        #画素値合計をピクセル数で除することでRGBの画素値の平均値を求める
        b_ave=b_ave/l
        g_ave=g_ave/l
        r_ave=r_ave/l
        # print(b_ave)

        bgr[k]=np.array([idir + fname + str(k+1) + '.jpg', b_ave, g_ave, r_ave])
        # print(bgr[k])

    df = pd.DataFrame(bgr, columns=['path', 'blue', 'green', 'red'])    #opencvの並び準BGRに合わせる
    if not os.path.isdir(odir):
        os.makedirs(odir)
    df.to_csv(odir + item + '.csv')

# csv結合
def contcat_csv(f_path:str):
    # pathlibのitedir()で対象とするディレクトリのCSVファイル一覧をジェネレーターとして取得
    csvs = [pd.read_csv(str(path)) for path in pathlib.Path(f_path).glob('*.csv')]
    # そのファイル一覧をPandasで読み込んで、pd.concat()で連結してDataFrameとして返す
    return pd.concat(csvs, sort=False)

df = contcat_csv('output/ans/')
df = df.drop(df.columns[0], axis=1)
id_ = np.arange(len(df))
df.insert(0, 'id', id_)

# 連結されたDataFrameをCSVとして保存する
if not os.path.isdir("csv/ans/"):
        os.makedirs("csv/ans/")
df.to_csv('csv/ans/total-concat.csv', index=False, header=None)
