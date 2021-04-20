import psycopg2
from var import Var

conn = psycopg2.connect(database=Var.dbname, user=Var.username, password=Var.password, host=Var.hostname, port=Var.port)
cur = conn.cursor()
# keywordのテーブルも作る
target_sql_file = open('keyword.sql')
sql_data = target_sql_file.read()
target_sql_file.close()

conn.commit()
cur.execute(sql_data)

cur.execute(
    "DROP TABLE IF EXISTS img_rgb;"+
    "CREATE TABLE img_rgb (" +
        "id bigint,"+
        "path text," +
        "blue real," +
        "green real," +
        "red real);"
    )
with open('csv/total-concat.csv') as fp:
    cur.copy_from(fp, table='img_rgb', sep=',', columns=['id','path', 'blue', 'green', 'red'])
conn.commit()