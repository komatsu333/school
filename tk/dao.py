import mariadb
import sys
from student import Student

class DAO:
        def getConnection(self) -> mariadb.Connection:
                try:
                        con = mariadb.connect(
                                user = "user",
                                password = "shikoku-pc",
                                host = "192.168.76.207",
                                port = 3306,
                                database = "GakuseiDB"
                        )
                except mariadb.Error as e:
                        print(f"DB 接続エラー:{e}")
                        return None

                return con

        def getAllStudentList(self,con):
                sql = 'SELECT * FROM student_tbl order by id'
                cur = con.cursor()
                try:
                        cur.execute(sql)
                        Student_list = []
                        for record in cur:
                                s = Student(record[0], record[1], record[2], record[3], record[4])
                                Student_list.append(s)

                        return Student_list

                except mariadb.Error as e:
                        print(f"D エラー:{e}")
                        return None

                finally:
                        cur.close()

        def getStudentList(self,con,keywd):
                sql = "SELECT * FROM student_tbl where name like '%" +keywd+ "%' "
                sql += " OR addr like '%" +keywd+ "%'"
                sql += " OR tel like '%" +keywd+ "%'"
                sql += " OR id like '%" +keywd+ "%'"
                sql += " OR highschool like '%" +keywd+ "%' order by id"
                cur = con.cursor()
                try:
                        cur.execute(sql)
                        Student_list = []
                        for record in cur:
                                s = Student(record[0], record[1], record[2], record[3], record[4])
                                Student_list.append(s)

                        return Student_list

                except mariadb.Error as e:
                        print(f"D エラー:{e}")
                        return None

                finally:
                        cur.close()

        def DeleteStudent(self,con,delete_id):
                sql = "delete from student_tbl where id = ?"
                param = (delete_id,)
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

        def InsertStudent(self,con,st):
                sql = "INSERT INTO student_tbl (name, addr, tel, highschool) VALUES(?, ?, ?, ?)"
                cur = con.cursor()

                pram = (st._name, st._addr, st._tel, st._highschool)
                try:
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
