import tkinter as tk
from tkinter.constants import *
from PIL import Image, ImageTk

counter = 0

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #--------------Title Window--------------
        #if counter == 0:
        self.title('剪刀石頭布')
        self.geometry('380x400')
        self.resizable(False, False)

        #-------------- widgets --------------
        title = tk.Label(self, text='剪刀石頭布小遊戲', font=('Times 20'))
        title.place( x=190,y=100,anchor = CENTER)
        label1 = tk.Label(self, text='開始遊戲(手向上)', font=('Times 10'))
        label1.place( x=190,y=180,anchor = CENTER)
        label2 = tk.Label(self, text='退出遊戲(手向下)', font=('Times 10'))
        label2.place( x=190,y=250,anchor = CENTER)
        #-------------- Only For Testing--------------
        button1 = tk.Button(self, text='測試開始')
        button1['command'] = self.button_clicked
        button1.place(x=190,y=300,anchor = CENTER)
    
        
    #-------------- Other Functions --------------
    def button_clicked(self):
        self.destroy()    

#-------------- Program Start --------------
if __name__ == "__main__":
    app1 = MainApp()
    app1.mainloop()

    #-------------- Game Window --------------
    root = tk.Tk()
    root.title('剪刀石頭布')
    root.geometry('700x600')
    root.resizable(False, False)

    #-------------- Widgets --------------
     
    img1 = Image.open('rock.png')
    tk_img1 = ImageTk.PhotoImage(img1)
    canvas1 = tk.Canvas(root, width=tk_img1.width(), height=tk_img1.height())
    canvas1.create_image(0, 0, anchor='nw', image=tk_img1)   # 在 Canvas 中放入圖片
    canvas1.place(x=150,y=500,anchor = CENTER)
    
    img2 = Image.open('paper.png')
    tk_img2 = ImageTk.PhotoImage(img2)
    canvas2 = tk.Canvas(root, width=tk_img2.width(), height=tk_img2.height())
    canvas2.create_image(0, 0, anchor='nw', image=tk_img2)   # 在 Canvas 中放入圖片
    canvas2.place(x=350,y=500,anchor = CENTER)

    img3 = Image.open('scissors.png')
    tk_img3 = ImageTk.PhotoImage(img3)
    canvas3 = tk.Canvas(root, width=tk_img3.width(), height=tk_img3.height())
    canvas3.create_image(0, 0, anchor='nw', image=tk_img3)   # 在 Canvas 中放入圖片
    canvas3.place(x=550,y=500,anchor = CENTER)

    img4 = Image.open('opponent.png')
    tk_img4 = ImageTk.PhotoImage(img4)
    canvas4 = tk.Canvas(root, width=tk_img4.width(), height=230)
    canvas4.create_image(0, 0, anchor='nw', image=tk_img4)   # 在 Canvas 中放入圖片
    canvas4.place(x=350,y=200,anchor = CENTER)

    root.mainloop()