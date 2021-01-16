import math
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
import turtle
import os.path
import sys

class Painter:
    def __init__(self,_matrix):
        self.window = Tk()
        self.window.title("Sudoku Matrix")
        self.labelText = [[],[],[],[],[],[],[],[],[]]

        # 行列标
        for i in range(1,10):
            Label(self.window,text = i,
            font=('microsoft yahei', 14),
            width = 5,heigh = 2,
            bg = "#C4CAFF").grid(column = i,row = 0)

            tex = chr(ord('A') + i - 1)
            Label(self.window,text = tex,
            font=('microsoft yahei', 14),
            width = 5,heigh = 2,
            bg = "#C4CAFF").grid(column = 0,row = i)

        for i in range(9):
            for j in range(9):
                tex = StringVar()
                tex.set("1111")
                color = "white"

                if _matrix.matrix[i][j] == 0:
                    tex = ""
                    color = "#DEDEDE"

                lab2 = Label(self.window,textvariable = tex,
                text = _matrix.matrix[i][j],
                bg = color,width = 5,heigh = 2,
                font=('microsoft yahei', 14),
                ).grid(row = i + 1,column = j + 1)

                #lab2.config(text='HELLO')

        self.window.mainloop()
        