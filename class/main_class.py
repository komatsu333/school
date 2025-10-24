from class_dao import ClassDao as Dao
import sys

da = Dao()

cn = da.getConnection()
#p_list = da.getAllPref(cn)
#p_list = da.getWordPref(cn)
p_list = da.deletePref(cn)

if p_list is not None:
	for p in p_list:
#		print(p)
		print(f"{p._kenmei},{p._kenchou},{p._chihou}")
else:
	print("DB接続エラー")
	sys.exit()

