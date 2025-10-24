from class_dao import ClassDao as Dao
import sys
from pref import Pref as pr

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
		print("\nupdate開始\n")

		c_id = input("変更したいフィールドのIDを入力 > ")
		id = input("id > ")
		kenmei = input("県名 > ")
		kenchou = input("県庁 > ")
		jinkou = input("人口 > ")
		menseki = input("面積 > ")
		chihou = input("地方 > ")
		jinkoumitudo = input("人口密度 > ")

		pr_object = pr(id, kenmei, kenchou, jinkou, menseki, chihou, jinkoumitudo)

		anser = da.updatePref(cn, c_id, pr_object)

		p_list = da.getAllPref(cn)
		if anser is True:
			print('\n成功しました\n')
			for p in p_list:
				print(p)
			sys.exit()

	except KeyboardInterrupt:
		print("\n終了")
		sys.exit()
