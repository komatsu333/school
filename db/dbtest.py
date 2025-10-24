#!/usr/bin/env python
import mariadb
import sys
try:
	config = {
	"user": "user",
	"password": "shikoku-pc",
	"host": "192.168.76.207",
	"port": 3306,
	"database": "todoufukenbase"
	}
	con = mariadb.connect(**config)

	#con = mariadb.connect(
	# user="user", # MariaDBのユーザーID
	# password="shikoku-pc", # MariaDBのrootユーザーのパスワード
	# host="192.168.76.207 ", # MariaDBのサーバーアドレス
	# port=3306, # MariaDBのポート番号
	# database=" todoufukenbase " # デフォルトで使用するDB
	#)

except mariadb.Error as e:
	print(f"DB接続エラー:{e}")

#############################

sql = 'SELECT * FROM todoufuken'
cur = con.cursor()

try:
	cur.execute(sql)
	# SQLを実行する
	# SELECT結果を取得する
	for record in cur:
		print(record)

except mariadb.Error as e:
	print(f"DBエラー:{e}")

#############################

nin = input('人口 = ')
sql ='SELECT * FROM todoufuken '
sql += " WHERE jinkou >= ? "
cur = con.cursor()
param = (nin,)
try:
	# SQLを実行する
	cur.execute(sql,param)
	# SELECT結果を取得する
	for record in cur:
		print(record)

except mariadb.Error as e:
	print(f"DBエラー:{e}")

finally:
	cur.close()
