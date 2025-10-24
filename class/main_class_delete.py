from class_dao import ClassDao as Dao
import sys

da = Dao()
cn = da.getConnection()

if cn is None:
	print('接続エラー')
	sys.exit()

p_list = da.getAllPref(cn)

for p in p_list:
	print(p)

while True:
	try:
		keyword = input("削除id > ")
		anser = da.deletePref(cn,keyword)

		p_list = da.getAllPref(cn)
		if anser is True:
			print('成功')
			for p in p_list:
				print(p)

	except KeyboardInterrupt:
		print("\n終了")
		sys.exit()
