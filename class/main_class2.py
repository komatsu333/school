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
		keyword = input("検索ワード > ")
		p_list = da.getKeyPref(cn,keyword)
		for p in p_list:
			print(f"{p._kenmei},{p._kenchou},{p._chihou}")

	except KeyboardInterrupt:
		print("\n終了")
		sys.exit()
