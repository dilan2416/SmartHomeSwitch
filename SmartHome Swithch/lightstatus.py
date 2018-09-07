#encoding=utf-8
import pymysql
import sys

# 连接MySQL数据库
connection = pymysql.connect("localhost","root","12345678","smarthome",charset='utf8' )

# 通过cursor创建游标
cursor = connection.cursor()

# 创建sql 语句，并执行
sql = """INSERT INTO equipmentstatus(name,status,kind)
         VALUES ('客厅电灯2',0, 1)"""
    #"UPDATE equipmentstatus SET name = '客厅电灯1' WHERE id = 2"
#"""INSERT INTO equipmentstatus(name,status,kind)
 #        VALUES ('客厅电灯',0, 1)"""

cursor.execute(sql)

# 提交SQL
connection.commit()
