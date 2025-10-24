import tkinter as tk
from tkinter import ttk
from dao import DAO
from student import Student

class ui:

    #コンストラクタ
    def __init__(self):
        # メインウィンドウの生成
        self._root = tk.Tk()
        self._root.title('学生 List')
        self._root.geometry('600x600')
        # ツリー
        column = ('ID', 'Name', 'Addr','Tel','HighSchool')
        self._tree = ttk.Treeview(self._root, height=20,columns=column)
        # 列の設定
        self._tree.column('#0',width=0, stretch='no')
        self._tree.column('ID', anchor='center', width=50)
        self._tree.column('Name',anchor='center', width=100)
        self._tree.column('Addr', anchor='center', width=100)
        self._tree.column('Tel', anchor='center', width=150)
        self._tree.column('HighSchool', anchor='center', width=100)
        # 列の見出し設定
        self._tree.heading('#0',text='')
        self._tree.heading('ID', text='ID',anchor='center')
        self._tree.heading('Name', text='名前', anchor='center')
        self._tree.heading('Addr',text='住所', anchor='center')
        self._tree.heading('Tel',text='電話番号', anchor='center')
        self._tree.heading('HighSchool',text='出身高校', anchor='center')
        # ウィジェットの配置
        self._tree.pack(pady=50)

        #####self._tree.bind("<<TreeviewSelect>>",self.SelectRecord)
        # 検索テキストボックス
        self._textbox1 = tk.Entry(width=20)
        self._textbox1.place(x=50,y=10)
        # 検索ボタン
        self._button1 = tk.Button(self._root,text="検索",command=self.ButtonSearch)
        self._button1.place(x=200,y=10)
        # 削除ボタン
        self._button2 = tk.Button(self._root,text="削除",command=self.ButtonDelete)
        self._button2.place(x=500,y=15)
        # 新規登録ボタン
        self._button3 = tk.Button(self._root,text="登録",command=self.ButtonInsert)
        self._button3.place(x=350,y=550)
        # 新規入力ラベル
        self._label1 = tk.Label(self._root,text="名前")
        self._label1.place(x=30,y=490)
        self._label2 = tk.Label(self._root,text="住所")
        self._label2.place(x=30,y=510)
        self._label3 = tk.Label(self._root,text="電話番号")
        self._label3.place(x=30,y=530)
        self._label4 = tk.Label(self._root,text="出身高校")
        self._label4.place(x=30,y=550)
        # 新規入力テキストボックス
        self._textbox2 = tk.Entry(width=30)
        self._textbox2.place(x=100,y=490)
        self._textbox3 = tk.Entry(width=30)
        self._textbox3.place(x=100,y=510)
        self._textbox4 = tk.Entry(width=30)
        self._textbox4.place(x=100,y=530)
        self._textbox5 = tk.Entry(width=30)
        self._textbox5.place(x=100,y=550)

    #検索ボタンクリック
    def ButtonSearch(self):
        keywd=self._textbox1.get()
        da = DAO()
        cn = da.getConnection()

        if keywd == "":
                students = da.getAllStudentList(cn)       #検索が空で全検索
        else:
                students = da.getStudentList(cn, keywd)   #検索にキーワードがある場合、検索

        self.TreeDataView(students)

    #削除ボタンクリック
    def ButtonDelete(self):
        # 選択行の判別
        try:
            select_record_id = self._tree.focus()
            # 選択行のレコードを取得
            select_values = self._tree.item(select_record_id, 'values')
            # 選択行のレコードを取得
            delete_id = select_values[0]

#            print(delete_id)
            da = DAO()
            cn = da.getConnection()
            anser = da.DeleteStudent(cn, delete_id)
            if anser is True:
               print("succes")
        except:
            print("選択されたデータがありません")

    #登録ボタンクリック
    def ButtonInsert(self):
        name=self._textbox2.get()
        addr=self._textbox3.get()
        tel=self._textbox4.get()
        high=self._textbox5.get()

        da = DAO()
        cn = da.getConnection()

        tk_object = Student(0,name, addr, tel, high)

        anser = da.InsertStudent(cn, tk_object)
        self.ButtonSearch()

    #ツリー内を選択したとき
    def SelectRecord(self,event):
        # 選択行の判別
        select_record_id = self._tree.focus()
        # 選択行のレコードを取得
        select_values = self._tree.item(select_record_id, 'values')
        delete_id = select_values[0]
        print(delete_id)

    #ツリー内にデータを表示
    def TreeDataView(self,students):
        self._tree.delete(*self._tree.get_children())
        i=0
        std: student
        for std in students:
            self._tree.insert(parent='',
                              index='end',
                              iid=i ,
                              values=(
                                  std._id,
                                  std._name,
                                  std._addr,
                                  std._tel,
                                  std._highschool)
                              )
            i+=1

    def main_loop(self):
        self._root.mainloop()



