import pymysql

conn = pymysql.connect("localhost","root","12345678","smarthome" )

cursor = conn.cursor()

# 执行数据查询

sql = "SELECT `status` FROM `equipmentstatus` "
cursor.execute(sql)
#查询数据库单条数据
result = cursor.fetchone()
print(result)

# 关闭数据连接
conn.close()
print(int(result[0]))
