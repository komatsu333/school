import mariadb
import sys
from pref import Pref #prefをインポート

class ClassDao:
        def getConnection(self) -> mariadb.Connection:
                try:
                        con = mariadb.connect(
                                user = "user",
                                password = "shikoku-pc",
                                host = "192.168.76.207",
                                port = 3306,
                                database = "todoufukenbase"
                        )
                except mariadb.Error as e:
                        print(f"DB 接続エラー:{e}")
                        return None

                return con

        def getAllPref(self,con):
                sql = 'SELECT * FROM todoufuken order by id'
                cur = con.cursor()
                try:
                        cur.execute(sql)
                        pref_list = []
                        for record in cur:
                                p = Pref(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                                pref_list.append(p)

                        return pref_list

                except mariadb.Error as e:
                        print(f"D エラー:{e}")
                        return None

                finally:
                        cur.close()

        def getWordPref(self,con):
                pref_inp = input('検索ワード > ')
                sql = "SELECT * FROM todoufuken where kenmei like '%" +pref_inp+ "%' "
                sql += " OR kenchou like '%" +pref_inp+ "%' order by id"
                cur = con.cursor()
                try:
                        cur.execute(sql)
                        pref_list = []
                        for record in cur:
                                p = Pref(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                                pref_list.append(p)

                        return pref_list

                except mariadb.Error as e:
                        print(f"D エラー:{e}")
                        return None

                finally:
                        cur.close()

        def getKeyPref(self,con,key):
                sql = "SELECT * FROM todoufuken where kenmei like '%" +key+ "%'"
                sql += " or kenchou like '%" + key+ "%' order by id"
                cur = con.cursor()
                try:
                        cur.execute(sql)
                        pref_list = []
                        for record in cur:
                                p = Pref(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                                pref_list.append(p)

                        return pref_list

                except mariadb.Error as e:
                        print(f"D エラー:{e}")
                        return None

                finally:
                        cur.close()


        def deletePref(self,con,key):
                sql = "delete from todoufuken where id = ?"
                param = (key,)
                cur = con.cursor()
                try:
                        cur.execute(sql,param)
                        con.commit()
                        return True

                except mariadb.Error as e:
                        print(f"deleteの処理に失敗:{e}")
                        return False

                finally:
                        cur.close()

        def insertPref(self,con,pr):
                sql = "INSERT INTO todoufuken (id, kenmei, kenchou, jinkou, menseki, chihou, jinkoumitudo) VALUES(?, ?, ?, ?, ?, ?, ?)"
                cur = con.cursor()

                pram = (pr._id, pr._kenmei, pr._kenchou, pr._jinkou, pr._menseki, pr._chihou, pr._jinkoumitudo)
                try:
#                        cur.execute(sql, (pr._id, pr._kenmei, pr._kenchou, pr._jinkou, pr._menseki, pr._chihou, pr._jinkoumitudo))
                        cur.execute(sql, pram)
                        con.commit()
                        return True

                except mariadb.Error as e:
                        print(f"insertの処理に失敗:{e}")
                        return False

                finally:
                        cur.close()

        def updatePref(self,con,c_id,pr):
                sql = "update todoufuken set id = ?, kenmei = ?, kenchou = ?, jinkou = ?, menseki = ?, chihou = ?, jinkoumitudo = ? where id = ?"
                cur = con.cursor()
                pram = (pr._id, pr._kenmei, pr._kenchou, pr._jinkou, pr._menseki, pr._chihou, pr._jinkoumitudo, c_id)

                try:
                        cur.execute(sql, pram)
                        con.commit()
                        return True
                except mariadb.Error as e:
                        print(f"insertの処理に失敗:{e}")
                        return False

                finally:
                        cur.close()

##########################################################################
if __name__ == '__main__':
        da = ClassDao()
        cn = da.getConnection()

        p_list = da.getAllPref(cn)
        print(p_list)

        for p in p_list:
                print(p)
