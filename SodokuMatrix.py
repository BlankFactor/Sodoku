import os.path
import sys
import tkinter.messagebox
import time

class SodokuMatrix:

    def __init__(self,_path):
        self.matrix = []
        self.blankBlock = 0
        self.candidates = []
        self.step = 0
        self.time_s = time.time()

        # 路径检测
        if os.path.isfile(_path) == False:
            tkinter.messagebox.WARNING("Invalid path")
            exit()

        file = open(_path)

        # 读入数独样本/初始化矩阵 (默认样本正确)
        i = 0
        for line in file:
            line = line.replace(' ','')
            line = line.replace('\n','')
            self.matrix.append([])

            for j in range(9):
                self.matrix[i].append(eval(line[j]))
                if line[j] == '0':
                    self.blankBlock = self.blankBlock + 1
            
            i = i + 1

        # 初始化单元候选数列表
        for i in range(9):
            self.candidates.append([])

            for j in range(9):
                self.candidates[i].append([])
                
                if self.matrix[i][j] != 0:
                    continue
                
                for k in range(1,10):
                    self.candidates[i][j].append(k)

                # 消除行重复数
                for k in range(9):
                    if k == j:
                        continue
                    if self.matrix[i][k] in self.candidates[i][j]:
                        self.candidates[i][j].remove(self.matrix[i][k])
                # 消除列重复数
                for k in range(9):
                    if k == j:
                        continue
                    if self.matrix[k][j] in self.candidates[i][j]:
                        self.candidates[i][j].remove(self.matrix[k][j])
                # 消除宫重复数
                block = self.GetBlocKIndex(i,j)

                for m in self.GetRangeByBlock_Row(block):
                    for n in self.GetRangeByBlock_Column(block):
                        if m == i and n == j:
                            continue

                        if self.matrix[m][n] in self.candidates[i][j]:
                            self.candidates[i][j].remove(self.matrix[m][n])

        os.system("cls")
        print("Th amount of blank unit : [ ",self.blankBlock," ]")
        for i in self.matrix:
            print(i)

        for i in self.candidates:
            print(i)

    # 通过行列下标获得所在宫下标
    def GetBlocKIndex(self,_row,_column):
        if (_row < 0 or _row >= 9) or (_column < 0 or _column >= 9):
            return -1
        
        row = int(_row / 3)
        column = int(_column / 3)

        return row * 3 + column
    
    # 通过宫下标获取所在行列范围
    def GetRangeByBlock_Row(self,_block):
        row = int(_block / 3)
        return range(row * 3,row * 3 + 3)
    def GetRangeByBlock_Column(self,_block):
        column = int(_block % 3)
        return range(column * 3,column * 3 + 3)

    # 获取单元侯选数数组
    def GetCandiatews(self,_row,_column):
        return self.candidates(_row,_column)
    
    def GetBlankBlock(self):
        return self.blankBlock

    # 检查当前位置数字是否有效
    def CheckIfValid(self,_row,_column):
        if self.matrix[_row][_column] == 0:
            return "Blank unit"
        
        # 行列检查
        for i in range(9):
            if i == _column:
                continue

            if self.matrix[_row][i] == self.matrix[_row][_column]:
                return False
        for i in range(9):
            if i == _row:
                continue

            if self.matrix[i][_column] == self.matrix[_row][_column]:
                return False    
        
        # 宫检测
        block = self.GetBlocKIndex(_row,_column)

        for i in self.GetRangeByBlock_Row(block):
            for j in self.GetRangeByBlock_Column(block):
                if i == _row and j == _column:
                    continue

                if self.matrix[i][j] == self.matrix[_row][_column]:
                    return False

        return True

    # 递归算法求数独解
    def Solve(self,_row = 0,_column = 0):
        os.system("cls")
        print("Current coodination [",_row,",",_column,"] step : ",self.step)
        self.step += 1
        for i in self.matrix:
            print(i)

        # 候选数组 寻空单元
        if len(self.candidates[_row][_column]) == 0:
            if _column == 8 and _row == 8:
                self.SolvedSuccessfully()
            elif _column == 8:
                self.Solve(_row + 1,0)
            else:
                self.Solve(_row,_column + 1)

        else:
            #print("Unit [",_row,",",_column,"] Candiates : ",self.candidates[_row][_column])

            for k in self.candidates[_row][_column]:
                self.matrix[_row][_column] = k

                if self.CheckIfValid(_row,_column):
                    if _column == 8 and _row == 8:
                        self.SolvedSuccessfully()
                    elif _column == 8:
                        self.Solve(_row + 1,0)
                    else:
                        self.Solve(_row,_column + 1)
            
                else:
                    #print("Unit [",_row,",",_column,"] invalid candiate : ",k)
                    self.matrix[_row][_column] = 0

            # 若所有候选数均无效 则代表该位置之前的某一单元数出错 当前位置归零并退回上一级循环
            self.matrix[_row][_column] = 0
    
    def SolvedSuccessfully(self):
        os.system("cls")
        print("Solved successfully")
        print("Time cost : [",round(time.time() - self.time_s,2)," seconds ]")
        print("Count of recursion : [",self.step," times ]")
        for i in self.matrix:
            print(i)
        exit()