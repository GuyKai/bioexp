import tkinter as tk
from tkinter.constants import *



#===========================event 設定===========================
def decide():
    while (True):
        #從外部呼叫函數  決定手勢
        break
        

#===========================視窗建立===========================
window = tk.Tk()
window.title('剪刀石頭布')
window.geometry('380x400')
window.resizable(False, False)
#===========================標題畫面===========================

title = tk.Label(window, text='剪刀石頭布小遊戲', font=('Times 20'))
title.place( x=190,y=100,anchor = CENTER)

label1 = tk.Label(window, text='開始遊戲(手向上)', font=('Times 10'))
label1.place( x=190,y=180,anchor = CENTER)
label2 = tk.Label(window, text='退出遊戲(手向下)', font=('Times 10'))
label2.place( x=190,y=250,anchor = CENTER)

window.after(100, decide)

window.mainloop()

