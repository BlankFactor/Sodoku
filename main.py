import math
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
import turtle
import os.path
import sys
import time

from SodokuMatrix import SodokuMatrix
from Painter import Painter

def main():
    matrix = SodokuMatrix(askopenfilename())
    #matix.Solve()
    #painter = Painter(matrix)
main()