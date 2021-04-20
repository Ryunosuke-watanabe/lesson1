from var import Var
import psycopg2
import numpy as np

conn = psycopg2.connect(database=Var.dbname, user=Var.username, password=Var.password, host=Var.hostname, port=Var.port)
cur = conn.cursor()

# 画像データのrgbを取り出して配列に格納
cur.execute("SELECT blue, green, red FROM img_rgb;")
rows_img = cur.fetchall()

# キーワードのrgbも配列に格納
cur.execute("SELECT blue, green, red FROM keyword;")
rows_key = cur.fetchall()
# print(rows_key)

# キーワードに何が入ってるかを格納
cur.execute("SELECT word FROM keyword;")
keyword = cur.fetchall()

# 内積を計算して結果を配列に格納
ans = np.zeros((len(rows_img), len(rows_key[0])))
n = 0
for item_img in rows_img:
    item_img = np.array(item_img)
    ans_2 = np.array([])
    for item_key in rows_key:
        item_key = np.array(item_key)
        # print(np.array([item_img*item_key]))
        ans_2 = np.append(ans_2, sum(item_img*item_key))
    ans[n] = np.array(ans_2)
    n += 1

# ユーザーに入力させる
search_num = int(input('番号を入力してください'+ str([i[0]+'なら'+str(keyword.index(i)) for i in keyword])))

# 計算結果が一番高いインデックスを取得
final = np.array([])
for item in ans:
    final = np.append(final, [item[search_num]])

final_num = final.max()

re = np.where(final==final_num)[0][0]
# print(re)

# sqlからインデックスを元に検索
cur.execute("SELECT path FROM img_rgb WHERE id = %s", (str(re),))
final_result = cur.fetchall()

print(final_result[0][0])