import os.path
import sys
import tkinter.messagebox
import time

class SodokuMatrix:

    def __init__(self,_path):
        self.matrix = []
        self.blankBlock = 0
        self.candidates = []
        self.countOfCandiates = 0
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
                self.countOfCandiates += 10

                # 消除行上重复数
                for k in range(9):
                    if k == j:
                        continue
                    if self.matrix[i][k] in self.candidates[i][j]:
                        self.candidates[i][j].remove(self.matrix[i][k])
                        self.countOfCandiates -= 1
                # 消除列上重复数
                for k in range(9):
                    if k == i:
                        continue
                    if self.matrix[k][j] in self.candidates[i][j]:
                        self.candidates[i][j].remove(self.matrix[k][j])
                        self.countOfCandiates -= 1
                # 消除宫重复数
                block = self.GetBlocKIndex(i,j)

                for m in self.GetRangeByBlock_Row(block):
                    for n in self.GetRangeByBlock_Column(block):
                        if m == i and n == j:
                            continue

                        if self.matrix[m][n] in self.candidates[i][j]:
                            self.candidates[i][j].remove(self.matrix[m][n])
                            self.countOfCandiates -= 1

        os.system("cls")
        print("The amount of blank unit : [ ",self.blankBlock," ]")
        print("The count of candiates : [ ",self.countOfCandiates," ]")
        # for i in self.matrix:
        #     print(i)

        # for i in self.candidates:
        #     print(i)

        self.Optimize()
        print("********************** After optimizing ************************")
        print("The amount of blank unit : [ ",self.blankBlock," ]")
        print("The count of candiates : [ ",self.countOfCandiates," ]")
        input()

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
        print("Count of blank units : [",self.blankBlock,"]")
        print("Count of candiates : [",self.countOfCandiates,"]")
        for i in self.matrix:
            print(i)
        exit()

    # 候选数组优化
    def Optimize(self):
        self.BlockFirstExclusion()
        self.RcFirstExclusion()

    # [ 宫区块对行列排除法 ] 
    # 在某一宫中同一个候选数出现在同一行或同一列 
    # 则该候选数在同行同列的其他宫中的候选数组中删除
    # 潜在候选数 A 的侯选位置必然小于等于 3
    # 当 A 侯选位置 = 1 该数必然符合条件
    # 当 A 侯选位置 = 2 or = 3 判断侯选位置是否为同一行(列) 是则符合条件
    def BlockFirstExclusion(self):

        # 宫循环
        for block in range(9):
            # 记录候选数分布 总为增序 (下标为 0 的数组不用)
            distribution = [[],[],[],[],[],[],[],[],[],[]]
            index = -1
            
            for i in self.GetRangeByBlock_Row(block):
                for j in self.GetRangeByBlock_Column(block):
                    index += 1

                    if len(self.candidates[i][j]) == 0:
                        continue
                    
                    # print("Block : ",block," Index : ",index,"(x,y) = (",i,",",j,") Candiates : ",self.candidates[i][j])
                    # input()

                    for k in self.candidates[i][j]:
                        distribution[k].append(index)

            # print("Block Index : ",block)
            # d = 0
            # for i in distribution:
            #     print("Candiate : ",d," ",i)
            #     d += 1
            # print()
            # input()
        
            # 遍历候选数分布数组
            for i in range(1,10):
                if len(distribution[i]) > 3 or len(distribution[i]) == 0:
                    continue
                # 宫号和宫内分布下标转换成矩阵坐标(第一个候选数出现位置的坐标)

                x = int(block / 3) * 3
                y = block % 3 * 3

                x += int(distribution[i][0] / 3)
                y += distribution[i][0] % 3

                if len(distribution[i]) == 1:
                    #print("(1)Valid candiate was detected : [",i,"] Coodination : [",x,",",y,"] len : ")
                    # 行列排除
                    for c in range(9):
                        if c == y:
                            continue
                        if i in self.candidates[x][c]:
                            self.candidates[x][c].remove(i)
                            #print("Block : ",block," Remove : (",i,") in [",x,",",c,"]")
                            self.countOfCandiates -= 1
                    for r in range(9):
                        if r == x:
                            continue
                        if i in self.candidates[r][y]:
                            self.candidates[r][y].remove(i)
                            #print("Block : ",block," Remove : (",i,") in [",r,",",y,"]")
                            self.countOfCandiates -= 1
                else:
                    # 判断是否为同一行 通过判断最大最小值是否在同一个宫内行域
                    tmp = int(int(distribution[i][0] / 3) * 3)
                    valid = True

                    #print("Verify candiate : ",i,"  Index : ",distribution[i]," Range : ",range(tmp,tmp+3))
                    for j in distribution[i]:
                        if j not in range(tmp,tmp + 3):
                            valid = False
                            break
                    
                    if valid:
                        #print("(2/3)Valid candiate was detected : [",i,"] Coodination : [",x,",",y,"]")
                        # 行排除(保留宫)
                        for c in range(9):
                            if c == y or self.GetBlocKIndex(x,c) == block:
                                continue
                            if i in self.candidates[x][c]:
                                self.candidates[x][c].remove(i)
                                self.countOfCandiates -= 1
                                #print("Block : ",block," Remove : (",i,") in [",x,",",c,"]")
                    
                    # 判断是否为同一列 通过宫内下标取余
                    # 判断余数是否一致
                    # 一致则表示在同一行
                    valid = True
                    tmp = distribution[i][0] % 3

                    for j in distribution[i]:
                        if j % 3 != tmp:
                            valid = False
                            break
                    
                    if valid:
                        # 列排除(保留宫)
                        for r in range(9):
                            if r == x or self.GetBlocKIndex(r,y) == block:
                                continue
                            if i in self.candidates[r][y]:
                                self.candidates[r][y].  remove(i)
                                self.countOfCandiates -= 1
                                #print("Block : ",block," Remove : (",i,") in [",r,",",y,"]")
    
    # [ 行列对宫排除法 ]
    # 一行或一列中的某一侯选数的侯选位置
    # 都在一个宫内 则该候选数所在宫的其他侯选位置删除该候选数
    # 有效候选数 A 的宫内分布数量必然属于 [1,3]
    def RcFirstExclusion(self):
        # 行搜寻
        for i in range(9):
            # 数组 [0] 不使用
            # 记录行中候选数分布 分布从 0 到 9
            distribution = [[],[],[],[],[],[],[],[],[],[]]

            # 记录候选分布 存放列号
            for j in range(9):
                if len(self.candidates[i][j]) == 0:
                    continue

                for k in self.candidates[i][j]:
                    distribution[k].append(j)

            for j in range(1,10):
                if len(distribution[j]) == 0 or len(distribution[j]) > 3:
                    continue

                block = self.GetBlocKIndex(i,distribution[j][0])

                if len(distribution[j]) == 1:
                    # 消除宫内异行候选数
                    for n in self.GetRangeByBlock_Row(block):
                        for m in self.GetRangeByBlock_Column(block):
                            if n == i:
                                continue
                            
                            if j in self.candidates[n][m]:
                                self.candidates[n][m].remove(j)
                                self.countOfCandiates -= 1
                else:
                    valid = True

                    # 检查候选数所处侯选位置是否全部属于一个宫之中
                    for k in distribution[j]:
                        if self.GetBlocKIndex(i,k) != block:
                            valid = False
                            break

                    if valid:
                        for n in self.GetRangeByBlock_Row(block):
                            for m in self.GetRangeByBlock_Column(block):
                                if n == i:
                                    continue

                                if j in self.candidates[n][m]:
                                    self.candidates[n][m].remove(j)
                                    self.countOfCandiates -= 1

        # 列搜寻
        for c in range(9):
            # 数组 [0] 不使用
            # 记录列中候选数分布 分布从 0 到 9
            distribution = [[],[],[],[],[],[],[],[],[],[]]

            # 记录候选分布 存放行号
            for r in range(9):
                if len(self.candidates[r][c]) == 0:
                    continue

                for k in self.candidates[r][c]:
                    distribution[k].append(r)

            for j in range(1,10):
                if len(distribution[j]) == 0 or len(distribution[j]) > 3:
                    continue

                block = self.GetBlocKIndex(distribution[j][0],c)

                if len(distribution[j]) == 1:
                    # 消除宫内异列候选数
                    for n in self.GetRangeByBlock_Row(block):
                        for m in self.GetRangeByBlock_Column(block):
                            if m == c:
                                continue
                            
                            if j in self.candidates[n][m]:
                                self.candidates[n][m].remove(j)
                                self.countOfCandiates -= 1
                else:
                    valid = True

                    # 检查候选数所处侯选位置是否全部属于一个宫之中
                    for k in distribution[j]:
                        if self.GetBlocKIndex(k,c) != block:
                            valid = False
                            break

                    if valid:
                        for n in self.GetRangeByBlock_Row(block):
                            for m in self.GetRangeByBlock_Column(block):
                                if m == c:
                                    continue

                                if j in self.candidates[n][m]:
                                    self.candidates[n][m].remove(j)
                                    self.countOfCandiates -= 1