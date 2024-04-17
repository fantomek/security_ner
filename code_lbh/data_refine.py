# 从数据库中拿出数据，并按标题进行去重
import pymysql
import re

conn = pymysql.connect(
    user='root',
    password='snort',
    host='202.117.43.191',
    port=3306,
    database='CNVD_DB',
    use_unicode=True,
    charset="utf8"
)

# 获取游标
cursor = conn.cursor()

# 编写sql
# cursor.execute("select * from cnvd;")
cursor.execute("select vulnerability_name,vulnerability_introduce from cnvd;")
res = cursor.fetchall()
print(len(res))
reslist = []
namelist = []

# 去重，按标题
for item in res:
    # print(item)
    vulnerability_name = re.sub(r'（.*?）', '', item[0])
    vulnerability_introduce = item[1]
    if vulnerability_name in namelist:
        continue
    namelist.append(vulnerability_name)
    reslist.append(vulnerability_introduce)

# 写入文件
with open("data.txt", "w+", encoding = 'utf-8') as f:
    for item in reslist:
        if item:
            f.write(item+'\n')   # \n 实现换行
f.close()

cursor.close()
conn.commit()
conn.close()
print('sql执行成功')