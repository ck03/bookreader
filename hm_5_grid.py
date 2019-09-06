import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from pymongo.collation import Collation


# from PIL import Image, ImageTk
#  https://blog.csdn.net/liuxu0703/article/details/54428405
# https://www.itread01.com/content/1550303110.html


class GUIGrid:
    def __init__(self, master=None):
        self.client = MongoClient(host="127.0.0.1", port=27017)
        self.collectionpath = self.client["ebook"]["path"]
        self.collectioninfo = self.client["ebook"]["bookinfo"]
        self.db_dict = {}
        mighty = tk.LabelFrame(master, text=' Mighty Python ')
        mighty.grid(column=0, row=0, padx=8, pady=4, ipadx=490)
        self.left = tk.Label(mighty, text="上次離開的章節")
        self.left.pack(padx=5, pady=10, side="left")
        center = tk.Label(mighty, text="書名:")
        center.pack(padx=35, pady=10, side="left")
        # 書名
        self.bookcom = ttk.Combobox(mighty, state='readonly')
        self.bookcom.pack(padx=30, pady=10, side="left")
        self.bookcom.bind("<<ComboboxSelected>>", self.chapterdetail)
        # 章節
        self.chapter = ttk.Combobox(mighty, state='readonly')
        self.chapter.pack(padx=45, pady=10, side="left")
        self.chapter.bind("<<ComboboxSelected>>", self.modified)

        self.btnprev = ttk.Button(mighty, text="上一頁",
                                  command=self.prevpage)
        self.btnprev.pack(padx=55, pady=10, side="left")

        self.btnnext = ttk.Button(mighty, text="下一頁",
                                  command=self.nextpage)
        self.btnnext.pack(padx=55, pady=10, side="left")

        self.lblcontent = tk.Label(root, bg='red', justify="left")
        self.lblcontent.grid(column=0, row=1, sticky="w")
        self.bookinfo()

        self.TextArea = tk.Text(root, font=("C:/Windows/Fonts/soukoumincho.ttf", 17), height=39)
        self.TextArea.grid(column=0, row=1, sticky="nsew")
        # 目前書名
        self.currentbook = ""
        # 目前書名id
        self.currentbookid = ""
        # 目前書名所有章節
        self.currentbookchapter = []

        # self.wifi_img = Image.open('a.jpg')
        # self.lblimg = ImageTk.PhotoImage(self.wifi_img)
        # self.lbl2 = tk.Label(root, image=self.lblimg, compound="top", text="Johnny提供,版權所有")
        # self.lbl2.grid(column=0, row=1, sticky="w")

    # 書名變換連動章節
    def chapterdetail(self, event):
        bookname = self.bookcom.get()
        self.currentbook = bookname
        bookid = ""
        for bname, bid in self.db_dict.items():
            if bname == bookname:
                bookid = bid
                self.currentbookid = bookid
                break
        if bookid is not None:
            binfo = self.collectioninfo.find({"book_id": "{}".format(bookid)}).collation(
                Collation(locale='zh', numericOrdering=True)).sort("sid")
            # 設定空元組
            x = ("請選擇",)
            for b in binfo:
                x = x + (b["title"],)
                self.currentbookchapter.append(b["title"])
            self.chapter["values"] = x
            self.chapter.current(0)
            # self.lblcontent.config(text="床前明月光，疑是地上霜，舉頭望明月，低頭思故鄉。")

    # 一開始先串書名
    def bookinfo(self):
        bookname = self.collectionpath.find({})
        if bookname.count() > 0:
            x = ("請選擇",)
            for b in bookname:
                self.db_dict[b["bookname"]] = b["bookid"]
                x = x + (b["bookname"],)
            self.bookcom["values"] = x
            self.bookcom.current(0)

    # 上一頁
    def prevpage(self):
        # self.left.config(text=self.chapter.current())
        dbprevindex = 0
        if self.chapter.current() != 1:
            previndex = self.chapter.current() - 1
            dbprevindex = self.chapter.current() - 2
            self.chapter.current(previndex)
        self.TextArea.delete(1.0, tk.END)
        chaptername = self.currentbookchapter[dbprevindex]

        self.left.config(text=chaptername+str(self.chapter.current()))

        x = self.collectioninfo.find({"title": "{}".format(chaptername)})
        if x.count() > 0:
            strc = ""
            for c in x:
                con = c["content"]
                for k in con:
                    strc += k + "\n\n"
            self.TextArea.insert(1.0, strc)

    # 下一頁
    def nextpage(self):
            # self.left.config(text=self.chapter.current())
            dbprevindex = 0
            if self.chapter.current() != len(self.currentbookchapter) - 1:
                previndex = self.chapter.current() + 1
                dbprevindex = self.chapter.current()
                self.chapter.current(previndex)
            self.TextArea.delete(1.0, tk.END)
            chaptername = self.currentbookchapter[dbprevindex]

            self.left.config(text=chaptername+str(self.chapter.current()))

            x = self.collectioninfo.find({"title": "{}".format(chaptername)})
            if x.count() > 0:
                strc = ""
                for c in x:
                    con = c["content"]
                    for k in con:
                        strc += k + "\n\n"
                self.TextArea.insert(1.0, strc)

    # 章節變換連動content
    def modified(self, event):
        self.left.config(text=self.chapter.current())
        # text要先刪除
        self.TextArea.delete(1.0, tk.END)
        chaptername = self.chapter.get()
        x = self.collectioninfo.find({"title": "{}".format(chaptername)})
        if x.count() > 0:
            strc = ""
            for c in x:
                con = c["content"]
                for k in con:
                    strc += k + "\n\n"
            self.TextArea.insert(1.0, strc)


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIGrid(master=root)
    root.title("tkinter_ebook")
    root.geometry("1200x1200")
    root.mainloop()
