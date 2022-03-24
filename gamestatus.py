import random
import time
from queue import Queue

class gamestatus(object):
    def __init__(self,row,column,mines,options):
        self.row,self.column,self.mineNum=row,column,mines
        self.failed,self.timeStart,self.finish=False,False,False
        self.redmine=[0,0]
        self.tmplist=[i for i in range(self.column*self.row-1)]
        self.gamemode=options[0]
        self.gametype=options[1]
        self.leftHeld,self.rightHeld,self.leftAndRightHeld,self.rightfirst=False,False,False,False
        self.path,self.gamenum,self.ranks=0,0,[0,0,0]
        self.starttime,self.intervaltime,self.endtime,self.oldinttime=0,0,0,0
        self.num0seen,self.islandseen,self.isbv=[],[],[]
        self.num0get,self.bvget=0,0
        self.ops,self.solvedops,self.bbbv,self.solvedbbbv,self.islands,self.solvedislands=0,0,0,0,0,0
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0]
        self.oldCell=(0,0)
        self.thisislandsolved,self.thisopsolved=False,False
        self.num = [[0 for j in range(self.column)] for i in range(self.row)] # -1雷，0-8数字
        self.status = [[0 for j in range(self.column)] for i in range(self.row)] # 0未开 1打开 2标雷
        self.pressed = [[0 for j in range(self.column)] for i in range(self.row)] # 0未打开 1打开 2标雷 3以上是其他
        self.num0queue=Queue()
        self.counter=None

    def outOfBorder(self, i, j):
        return i < 0 or i >= self.row or j < 0 or j >= self.column

    def createMine(self,mode):    
        num = self.mineNum
        if len(self.tmplist)!=self.column*self.row-1:
            self.tmplist=[i for i in range(self.column*self.row-1)]
        if mode==1:
            random.shuffle(self.tmplist)
            for i in range(num):
                r= int(self.tmplist[i]/self.column)
                c= self.tmplist[i]-r*self.column
                self.num[r][c]=-1
                for i in range(r - 1, r + 2):
                    for j in range(c - 1, c + 2):
                        if not self.outOfBorder(i, j) and (
                            self.num[i][j] != -1):
                            self.num[i][j] += 1
                        
    def BFS(self, i, j ,start0):
        #print(self.num0queue.qsize())
        if self.status[i][j] == 0:
            self.status[i][j] = 1
        if self.num[i][j] >= 0:
            if self.num[i][j] == 0: #左键开op递归
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.status[r][c] == 0 and self.num[r][c] != -1:
                            self.status[r][c] = 1
                            self.num0queue.put([r,c,start0])
            elif self.num[i][j] > 0: #双键递归，此处为假条件，将来会替换为递归开关
                flagged=0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.status[r][c] == 2:
                            flagged+=1
                if flagged==self.num[i][j]:
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c) and self.status[r][c] == 0 and self.num[r][c] != -1:
                                self.status[r][c] = 1
                                self.num0queue.put([r,c,start0])
                            elif not self.outOfBorder(r, c) and self.num[r][c]==-1 and self.status[r][c] == 0:
                                self.failed=True
                                self.redmine=[r,c]

    def doleft(self,i,j):
        self.allclicks[0]+=1
        self.pressed[i][j]=0
        if self.status[i][j] == 0:
            self.eclicks[0]+=1
            if self.num[i][j] >= 0:
                self.num0queue=Queue()
                self.num0queue.put([i,j,self.num[i][j] == 0])
                while(self.num0queue.empty()==False):
                    getqueuehead=self.num0queue.get()
                    self.BFS(getqueuehead[0], getqueuehead[1],getqueuehead[2])
            else:
                if not self.timeStart and self.gametype==1 :#第一下不能为雷
                    self.exchange1tolast(i,j)
                    self.num0queue=Queue()
                    self.num0queue.put([i,j,self.num[i][j] == 0])
                    while(self.num0queue.empty()==False):
                        getqueuehead=self.num0queue.get()
                        self.BFS(getqueuehead[0], getqueuehead[1],getqueuehead[2])        
                else:
                    self.failed=True
                    self.redmine=[i,j]

    def doright(self,i,j):
        self.allclicks[1]+=1
        self.rightfirst=True
        if self.status[i][j] == 0:
            self.flagonmine(i,j)
        elif self.status[i][j] == 2:
            self.unflagonmine(i,j)
        elif self.status[i][j] == 1 and self.num[i][j] != 0:
            self.flagonnumber(i,j)

    def pressdouble(self,i,j):
        if self.status[i][j] == 1:
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.status[r][c] == 0:
                            self.pressed[r][c]=1

    def dodouble(self,i,j):
        if self.rightfirst==True:
            self.allclicks[1]-=1
            self.rightfirst=False
        self.allclicks[2]+=1
        if self.chordingFlag(i, j):
            edouble=False
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        self.pressed[r][c]=0
                        if self.status[r][c] == 0:
                            edouble=True
                            if self.num[r][c] >= 0:
                                self.num0queue=Queue()
                                self.num0queue.put([r,c,self.num[r][c] == 0])
                                while(self.num0queue.empty()==False):
                                    getqueuehead=self.num0queue.get()
                                    self.BFS(getqueuehead[0], getqueuehead[1],getqueuehead[2])
                            else:
                                self.failed=True
                                self.redmine=[r,c]
            if edouble==True:
                self.eclicks[2]+=1
        else:
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.status[r][c] == 0:
                            self.pressed[r][c]=0
                        
    def domove(self,i,j):
        if not self.outOfBorder(i, j):
            if (i, j) != self.oldCell and (self.leftAndRightHeld or self.leftHeld):
                ii, jj = self.oldCell
                self.oldCell = (i, j)
                if self.leftAndRightHeld:
                    for r in range(ii - 1, ii + 2):
                        for c in range(jj - 1, jj + 2):
                            if not self.outOfBorder(r, c):
                                if self.status[r][c] == 0:
                                    self.pressed[r][c]=0
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c):
                                if self.status[r][c] == 0:
                                    self.pressed[r][c]=1
                elif self.leftHeld:
                    if self.status[i][j] == 0:
                        self.pressed[i][j]=1
                    if self.status[ii][jj] == 0:
                        self.pressed[ii][jj]=0
        elif self.leftAndRightHeld or self.leftHeld:#拖到界外
            ii, jj = self.oldCell
            if self.leftAndRightHeld:
                for r in range(ii - 1, ii + 2):
                    for c in range(jj - 1, jj + 2):
                        if not self.outOfBorder(r, c):
                            if self.status[r][c] == 0:
                                self.pressed[r][c]=0
            elif self.leftHeld:
                if self.status[ii][jj] == 0:
                    self.pressed[ii][jj]=0

    def dofinish(self,result):
        for i in range(self.row):
            for j in range(self.column):
                if result==2:#输了
                    if self.num[i][j] == -1 or self.status[i][j] == 2:
                        if self.num[i][j] == -1 and self.status[i][j] == 2:
                            pass
                        elif self.num[i][j] == -1:
                            self.pressed[i][j]= 2
                        else:
                            self.pressed[i][j]= 3

                elif result==1:#赢了
                    if self.num[i][j]==-1 or self.status[i][j] == 2:
                        if self.num[i][j]==-1  and self.status[i][j] == 0:#游戏过程中未标上的雷
                            self.pressed[i][j]=5
                        elif self.num[i][j]==-1  and self.status[i][j] == 2:#游戏过程中标上的雷
                            pass
                        else:
                            self.pressed[i][j]=3
                #j.status = 1
        if result==2:
            self.pressed[self.redmine[0]][self.redmine[1]]=4
            

    def exchange1tolast(self,i,j):
        self.num[i][j]=0
        self.num[self.row-1][self.column-1]=-1
        for ii in range(i - 1, i + 2):
            for jj in range(j - 1, j + 2):
                if not self.outOfBorder(ii, jj) and self.num[ii][jj]!=-1:     
                    count=0
                    for rr in range(ii - 1, ii + 2):
                        for cc in range(jj - 1, jj + 2):
                            if not self.outOfBorder(rr, cc) and self.num[rr][cc]==-1:
                                count+=1
                    self.num[ii][jj]=count
        for ii in range(self.row-2, self.row):
            for jj in range(self.column-2, self.column):
                if not self.outOfBorder(ii, jj) and self.num[ii][jj]!=-1:     
                    count=0
                    for rr in range(ii - 1, ii + 2):
                        for cc in range(jj - 1, jj + 2):
                            if not self.outOfBorder(rr, cc) and self.num[rr][cc]==-1:
                                count+=1
                    self.num[ii][jj]=count

    def chordingFlag(self, i, j):
        # i, j 周围标雷数是否满足双击的要求
        if self.num[i][j] <= 8 and self.num[i][j] >= 0 and self.status[i][j]==1:
            count = 0
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.status[r][c] == 2:
                            count += 1
            if count == 0 and self.num[i][j] !=0:
                return False
            else:
                return count == self.num[i][j]
        else:
            return False

    def flagonmine(self,i,j):
        self.eclicks[1]+=1
        self.allclicks[3]+=1
        self.rightfirst=False
        self.status[i][j] = 2

    def unflagonmine(self,i,j):
        self.eclicks[1]+=1
        self.allclicks[3]-=1
        self.rightfirst=False
        self.status[i][j] = 0

    def flagonnumber(self,i,j):
        count=0
        for r in range(i - 1, i + 2):
            for c in range(j - 1, j + 2):
                if not self.outOfBorder(r, c):
                    if self.status[r][c] == 0 or self.status[r][c]==2:
                        count += 1
        if count== self.num[i][j]:
            eright=False
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.status[r][c] == 0:
                            self.status[r][c] =2
                            self.allclicks[3]+=1
                            self.rightfirst=False
                            eright=True
            if eright==True:
                self.eclicks[1]+=1
                
    def findopis_bfs(self,i,j,num):
        for ii in range(i-1,i+2):
            if ii<0 or ii>=self.row:
                continue
            for jj in range(j-1,j+2):
                if jj<0 or jj>=self.column:
                    continue
                if num==1:
                    if self.num[ii][jj]>=0 and self.status[ii][jj]==0:
                        self.thisopsolved=False
                    if self.num[ii][jj]==0 and self.num0seen[ii][jj]==False:
                        self.num0seen[ii][jj]=True
                        self.num0get+=1
                        self.num0queue.put([ii,jj])
                elif num==2:
                    if self.isbv[ii][jj]==True and self.islandseen[ii][jj]==False:
                        if self.status[ii][jj]==0:
                            self.thisislandsolved=False
                        self.islandseen[ii][jj]=True
                        self.bvget+=1
                        self.num0queue.put([ii,jj])

    def cal_3bv(self):
        self.islands,self.solvedislands,self.ops,self.solvedops,self.solvedbbbv=0,0,0,0,0
        solvedelse,num0,numelse=0,0,0
        self.bvget,self.num0get=0,0
        self.num0seen = [[False for j in range(self.column)] for i in range(self.row)]
        self.islandseen = [[False for j in range(self.column)] for i in range(self.row)]
        self.isbv = [[False for j in range(self.column)] for i in range(self.row)]
        for i in range(self.row):#对0格计数
            for j in range(self.column):
                if self.num[i][j]==0:
                    num0+=1
        for i in range(self.row):
            for j in range(self.column):
                if self.num0get==num0:#所有0被染色，标志op计算完全，终止
                    break
                if self.num[i][j]==0:
                    if self.num0seen[i][j]==True:
                        continue
                    else:
                        self.ops+=1#找到新的op
                        self.thisopsolved=True
                        self.num0seen[i][j]=True
                        self.num0get+=1
                        self.num0queue=Queue()
                        self.num0queue.put([i,j])
                        while(self.num0queue.empty()==False):
                            getqueuehead=self.num0queue.get()
                            self.findopis_bfs(getqueuehead[0], getqueuehead[1],1)
                        if self.thisopsolved==True:
                            self.solvedops+=1
                        
        for i in range(self.row):
            for j in range(self.column):
                if self.num[i][j]>0:
                    nearnum0=False
                    for ii in range(i-1,i+2):
                        if ii<0 or ii>=self.row:
                            continue
                        for jj in range(j-1,j+2):
                            if jj<0 or jj>=self.column:
                                continue
                            if self.num[ii][jj]==0:
                                nearnum0=True
                                break
                    if nearnum0==False:
                        self.isbv[i][j]=True
                        numelse+=1
                        if self.status[i][j]==1:
                            solvedelse+=1

        for i in range(self.row):#算islands
            for j in range(self.column):
                if self.bvget==numelse:
                    break
                if self.isbv[i][j]==True:
                    if self.islandseen[i][j]==True:
                        continue
                    else:
                        self.islands+=1
                        self.thisislandsolved=True
                        if self.status[i][j]==0:
                            self.thisislandsolved=False
                        self.islandseen[i][j]=True
                        self.bvget+=1
                        self.num0queue=Queue()
                        self.num0queue.put([i,j])
                        while(self.num0queue.empty()==False):
                            getqueuehead=self.num0queue.get()
                            self.findopis_bfs(getqueuehead[0], getqueuehead[1],2)
                        if self.thisislandsolved==True:
                            self.solvedislands+=1
        self.bbbv=self.ops+numelse
        self.solvedbbbv=self.solvedops+solvedelse

    def leveljudge(self):
        gamesize=self.column*100000+self.row*1000+self.mineNum
        if gamesize==808010:
            return 'BEG'
        elif gamesize==1616040:
            return 'INT'
        elif gamesize==3016099:
            return 'EXP'
        else:
            return 'CUS%d'%(gamesize)

    def stylejudge(self):
        if self.allclicks[1]==0:
            return 'NF'
        else:
            return 'Flag'
