from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon ,QPainter
from PyQt5.QtWidgets import QLineEdit, QInputDialog
from queue import Queue
import superGUI, mineLabel,selfDefinedParameter,preference
import random
import time
from counter import Counter


class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.row = 16
        self.column = 16
        self.mineNum = 40
        self.oldinttime =0
        self.tmplist=[]
        self.gridsize=32
        self.leftHeld = False
        self.rightHeld = False
        self.rightfirst = False 
        self.leftAndRightHeld = False  # 鼠标是否被按下的标志位
        self.oldCell = (0, 0)  # 鼠标的上个停留位置，用于绘制按下去时的阴影
        self.finish = False
        self.needtorefresh=True 
        self.gamemode=1 #游戏模式，1为正常，2为重玩
        self.starttime,self.intervaltime=0,0
        self.mainWindow = MainWindow
        self.mainWindow.setWindowIcon(QIcon("media/mine.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.setupUi(self.mainWindow)
        
        self.num0queue=Queue()
        self.num0seen,self.islandseen,self.isbv=[],[],[]
        self.num0get,self.bvget=0,0
        self.ops,self.solvedops,self.bbbv,self.solvedbbbv,self.islands,self.solvedislands=0,0,0,0,0,0
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0]
        self.counterWindow =None
        self.counterui=None
        self.thisislandsolved,self.thisopsolved=False,False
        self.label=None

        
        self.timer = QTimer()
        self.timer.setInterval(43)
        self.timer.timeout.connect(self.timeCount)
        self.timeStart = False
        self.initMineArea()
        self.createMine(1)
        self.showcounter()
        self.label_2.leftRelease.connect(self.gameStart)
        self.frame.leftRelease.connect(self.gameStart)
        pixmap = QPixmap("media/svg/smileface.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/8.5)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)
        self.showminenum(self.mineNum)
        self.showtimenum(self.intervaltime)

        # 绑定菜单栏事件
        

        self.action.triggered.connect(self.newgameStart)
        self.action_re.triggered.connect(self.gamereStart)
        self.action_B.triggered.connect(self.action_BEvent)
        self.action_I.triggered.connect(self.action_IEvent)
        self.action_E.triggered.connect(self.action_Event)
        self.action_C.triggered.connect(self.action_CEvent)
        self.action_X_2.triggered.connect(QCoreApplication.instance().quit)
        self.action_counter.triggered.connect(self.showcounter)
        self.action_settings.triggered.connect(self.action_setevent)
        self.action_gridup.triggered.connect(self.gridup)
        self.action_griddown.triggered.connect(self.griddown)
        self.action_gridsize.setText('当前尺寸：%d'%(self.gridsize))
        self.actionChecked('I')  # 默认选择中级
        self.needtorefresh=False
    
    def left(self):
        return self.leftHeld
    def right(self):
        return self.rightHeld
    def chord(self):
        return self.left() and self.right()
    def recursive(self):
        return True
    def isCovered(self,i,j):
        return self.label.status[i][j]==0
    def isMine(self,i,j):
        return self.label.num[i][j]==-1
    def isFlag(self,i,j):
        return self.label.status[i][j]==2
    def isGameStarted(self):
        return self.timeStart
    def isGameFinished(self):
        return self.finish
    def putFlag(self,i,j):
        self.label.status[i][j]=2
    def rmFlag(self,i,j):
        self.label.status[i][j]=0
        
    def showcounter(self):
        self.action_counter.setChecked(True)
        self.counterWindow = QtWidgets.QMainWindow ()
        self.counterui = Counter(self.counterWindow)
        self.mainWindow.closeEvent_.connect(self.counterWindow.close)
        self.counterWindow.show()
        if self.finish==True:
            self.changecounter(2)
        else:
            self.changecounter(1)
   
    def outOfBorder(self, i, j):
        if i < 0 or i >= self.row or j < 0 or j >= self.column:
            return True
        return False

    def createMine(self,mode):    
        num = self.mineNum
        if len(self.tmplist)!=self.column*self.row:
            self.tmplist=[i for i in range(self.column*self.row)]
        if mode==1:
            self.tmplist=[i for i in range(self.column*self.row)]
            random.shuffle(self.tmplist)
        for i in range(num):
            r= int(self.tmplist[i]/self.column)
            c= self.tmplist[i]-r*self.column
            self.label.num[r][c]=-1
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    if not self.outOfBorder(i, j) and (
                        self.label.num[i][j] != -1):
                        self.label.num[i][j] += 1

    def initMineArea(self):
        for i in range(self.gridLayout.count()):
            w = self.gridLayout.itemAt(i).widget()
            w.setParent(None)
        self.label = mineLabel.mineLabel(self.row, self.column, self.gridsize)
        self.label.setMinimumSize(QtCore.QSize(self.gridsize*self.column, self.gridsize*self.row))
        self.label.leftPressed.connect(self.mineAreaLeftPressed)
        self.label.leftRelease.connect(self.mineAreaLeftRelease)
        self.label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
        self.label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
        self.label.rightPressed.connect(self.mineAreaRightPressed)
        self.label.setObjectName("label")
        self.label.resize(QtCore.QSize(self.gridsize*self.column, self.gridsize*self.row))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label.mouseMove.connect(self.mineMouseMove)
        

    def timeCount(self):
        self.intervaltime=time.time()-self.starttime
        inttime=int(self.intervaltime+0.9999)
        if inttime!=self.oldinttime:
            self.showtimenum(self.intervaltime)
        self.changecounter(1)

    def BFS(self, i, j ,start0):
        #print(self.num0queue.qsize())
        if self.label.status[i][j] == 0:
            self.label.status[i][j] = 1
        if self.label.num[i][j] >= 0:
            if not self.timeStart:
                self.timeStart = True
                self.timer.start()
                self.starttime=time.time()
                self.label.update()
            if self.label.num[i][j] == 0: #左键开op递归
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.label.status[r][c] == 0 and self.label.num[r][c] != -1:
                            self.label.status[r][c] = 1
                            self.num0queue.put([r,c,start0])
                self.label.update()
            elif self.label.num[i][j] > 0: #双键递归，此处为假条件，将来会替换为递归开关
                flagged=0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.label.status[r][c] == 2:
                            flagged+=1
                if flagged==self.label.num[i][j]:
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c) and self.label.status[r][c] == 0 and self.label.num[r][c] != -1:
                                self.label.status[r][c] = 1
                                self.num0queue.put([r,c,start0])
                    self.label.update()

    def mineAreaLeftRelease(self, i, j):
        if self.isGameFinished() or self.outOfBorder(i,j):
        elif self.chord():
            self.sendChord(i,j)
        elif self.left():
            self.sendLeft(i,j)
        self.leftHeld=False
        self.label.update()
        if self.isGameFinished():
            self.gameWin()
    
    def sendLeft(self,i,j): # 处理左键点击事件
        self.allclicks[0]+=1 # cl+1
        self.label.pressed[i][j]=0
        if self.isCovered(i,j): # 未打开的格子
            self.eclicks[0]+=1 # lce+1
            self.changecounter(1)
            self.doLeft(i,j)
            
    
    def sendChord(self,i,j):
    
    # 暂时先用递归调用，队列的事情以后再写
    
    def doLeft(self,i,j): # 执行左键点击行为
        if not self.isGameStarted():
            # 加入摆雷功能
        if self.isMine(i,j):
            # 加入踩雷代码
        else:
            self.label.status[i][j]=1
            if self.recursive() or self.label.num[i][j]==0: # 递归双击或开空
                self.doChord(i,j)
                
    def doRight(self,i,j):
        if self.isCovered(i,j):
            self.putFlag(i,j)
        else:
            self.rmFlag(i,j)
    
    def doChord(self,i,j): # 执行双击或开空行为
        if not self.canChord(i,j):
            return
        for ii in range(max(0,i-1),min(self.row,i+2)):
            for jj in range(max(0,j-1),min(self.column,j+2)):
                if self.isCovered(ii,jj):
                    self.doLeft(i,j)
                    
    def canChord(self,i,j): # 判断是否可双击
        if self.isMine(i,j): # 不可双击雷
            return False
        flagged=0 # 插旗计数
        for ii in range(max(0,i-1),min(self.row,i+2)):
            for jj in range(max(0,j-1),min(self.column,j+2)):
                if self.isFlag(i,j):
                    flagged+=1
        return flagged==self.label.num[i][j]

    def mineAreaRightPressed(self, i, j):
        if self.isGameFinished:
        else:
            
        
        if not self.finish:
            self.allclicks[1]+=1
            self.changecounter(1)
            self.rightfirst=True
            if self.label.status[i][j] == 0:
                self.eclicks[1]+=1
                self.allclicks[3]+=1
                self.rightfirst=False
                self.changecounter(1)
                self.label.status[i][j] = 2
                self.showminenum(self.mineNum-self.allclicks[3])
                self.label.update()
                #self.label.setText(str(int(self.label.text()) - 1))
            elif self.label.status[i][j] == 2:
                self.eclicks[1]+=1
                self.allclicks[3]-=1
                self.rightfirst=False
                self.changecounter(1)
                self.label.status[i][j] = 0
                self.showminenum(self.mineNum-self.allclicks[3])
                #self.label.setText(str(int(self.label.text()) + 1))
                self.label.update()
            elif self.label.status[i][j] == 1 and self.label.num[i][j] != 0:
                count=0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.label.status[r][c] == 0 or self.label.status[r][c]==2:
                                count += 1
                if count== self.label.num[i][j]:
                    eright=False
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c):
                                if self.label.status[r][c] == 0:
                                    self.label.status[r][c] =2
                                    self.allclicks[3]+=1
                                    self.rightfirst=False
                                    eright=True
                                    self.showminenum(self.mineNum-self.allclicks[3])
                    if eright==True:
                        self.eclicks[1]+=1
                        self.changecounter(1)
                    self.label.update()

    def mineAreaLeftPressed(self, i, j):
        self.leftHeld = True
        self.oldCell = (i, j)
        if not self.finish:
            if self.label.status[i][j] == 0:
                self.label.pressed[i][j]=1
                self.label.update()

    def chordingFlag(self, i, j):
        # i, j 周围标雷数是否满足双击的要求
        if self.label.num[i][j] <= 8 and self.label.num[i][j] >= 0 and self.label.status[i][j]==1:
            count = 0
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.label.status[r][c] == 2:
                            count += 1
            if count == 0 and self.label.num[i][j] !=0:
                return False
            else:
                return count == self.label.num[i][j]
        else:
            return False

    def mineAreaLeftAndRightPressed(self, i, j):
#        return 0
        self.leftAndRightHeld = True
        self.oldCell = (i, j)
        if not self.finish:
            if self.label.status[i][j] == 1:
                count = 0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.label.status[r][c] == 0:
                                self.label.pressed[r][c]=1
                                #self.mineLabel[r][c].setFrameShape(QtWidgets.QFrame.Panel)
                                #self.mineLabel[r][c].setFrameShadow(QtWidgets.QFrame.Sunken)
                            elif self.label.status[r][c] == 2:
                                count += 1
                self.label.update()
                return count == self.label.num[i][j]
            else:
                return False


    def mineAreaLeftAndRightRelease(self, i, j):
        self.leftAndRightHeld = False
        self.leftHeld = False
        if not self.finish and not self.outOfBorder(i, j):
            if self.rightfirst==True:
                self.allclicks[1]-=1
                self.rightfirst=False
            self.allclicks[2]+=1
            self.changecounter(1)
            if self.chordingFlag(i, j):
                Fail = False
                edouble=False
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            self.label.pressed[r][c]=0
                            if self.label.status[r][c] == 0:
                                edouble=True
                                if self.label.num[r][c] >= 0:
                                    self.num0queue=Queue()
                                    self.num0queue.put([r,c,self.label.num[r][c] == 0])
                                    while(self.num0queue.empty()==False):
                                        getqueuehead=self.num0queue.get()
                                        self.BFS(getqueuehead[0], getqueuehead[1],getqueuehead[2])
                                    self.label.update()
                                    if self.isGameFinished():
                                        self.gameWin()
                                else:
                                    Fail = True
                if edouble==True:
                    self.eclicks[2]+=1
                    self.changecounter(1)
                if Fail:
                    self.gameFailed(None,None)
            else:
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.label.status[r][c] == 0:
                                self.label.pressed[r][c]=0
                self.label.update()
                                #self.mineLabel[r][c].setFrameShape(QtWidgets.QFrame.Panel)
                                #self.mineLabel[r][c].setFrameShadow(QtWidgets.QFrame.Sunken)
    def mineMouseMove(self, i, j):
        if not self.finish:
            if not self.outOfBorder(i, j):
                if (i, j) != self.oldCell and (self.leftAndRightHeld or self.leftHeld):
                    ii, jj = self.oldCell
                    self.oldCell = (i, j)
                    if self.leftAndRightHeld:
                        for r in range(ii - 1, ii + 2):
                            for c in range(jj - 1, jj + 2):
                                if not self.outOfBorder(r, c):
                                    if self.label.status[r][c] == 0:
                                        self.label.pressed[r][c]=0
                        for r in range(i - 1, i + 2):
                            for c in range(j - 1, j + 2):
                                if not self.outOfBorder(r, c):
                                    if self.label.status[r][c] == 0:
                                        self.label.pressed[r][c]=1
                        self.label.update()
                    elif self.leftHeld:
                        if self.label.status[i][j] == 0:
                            self.label.pressed[i][j]=1
                        if self.label.status[ii][jj] == 0:
                            self.label.pressed[ii][jj]=0
                        self.label.update()
            elif self.leftAndRightHeld or self.leftHeld:#拖到界外
                ii, jj = self.oldCell
                if self.leftAndRightHeld:
                    for r in range(ii - 1, ii + 2):
                        for c in range(jj - 1, jj + 2):
                            if not self.outOfBorder(r, c):
                                if self.label.status[r][c] == 0:
                                    self.label.pressed[r][c]=0
                elif self.leftHeld:
                    if self.label.status[ii][jj] == 0:
                        self.label.pressed[ii][jj]=0
                self.label.update()
 
    def gamereStart(self):
        self.gamemode=2
        self.needtorefresh=False
        self.gameStart()

    def newgameStart(self):
        self.gamemode=1
        self.gameStart()

    def gameStart(self):
        if self.needtorefresh==True:
            for i in range(self.gridLayout.count()):
                w = self.gridLayout.itemAt(i).widget()
                w.setParent(None)
        if self.gamemode==1:
            pixmap = QPixmap("media/svg/smileface.svg")
        elif self.gamemode==2:
            pixmap = QPixmap("media/svg/smilefaceblue.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/8.5)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)
        self.showminenum(self.mineNum)
        self.timeStart = False
        self.finish = False
        self.timer.stop()
        if self.needtorefresh==True:
            self.initMineArea()
        else:
            self.label.num=[[0 for j in range(self.column)] for i in range(self.row)]
            self.label.status=[[0 for j in range(self.column)] for i in range(self.row)]
            self.label.pressed=[[0 for j in range(self.column)] for i in range(self.row)]
            self.label.update()
        self.createMine(self.gamemode)
        self.bbbv,self.solvedbbbv,self.ops,self.solvedops=0,0,0,0
        self.intervaltime,self.oldinttime =0,0
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0]
        self.changecounter(1)
        self.showtimenum(self.intervaltime)
        if self.needtorefresh==True:
            self.mainWindow.setMinimumSize(0, 0)
            self.mainWindow.resize(self.mainWindow.minimumSize())

    def changecounter(self,status):
        #self.counterui.valuelabelarray[0].setText('%.2f'%(self.intervaltime))
        #状态2为游戏结束，状态1为游戏开始
        if status==1 and self.finish==True:
            return
        allclicks=self.allclicks[0]+self.allclicks[1]+self.allclicks[2]
        eclicks=self.eclicks[0]+self.eclicks[1]+self.eclicks[2]
        if status==2:
            rt=max(float(self.intervaltime),0.01)
            allbv=int(self.bbbv)
            solvedbv=int(self.solvedbbbv)
            if eclicks==0:
                ioe,corr,thrp=0,0,0
            else:
                ioe,corr,thrp=solvedbv/allclicks,eclicks/allclicks,solvedbv/eclicks
            if solvedbv==0:
                est=999.99
            else:
                est=rt/(solvedbv+2*self.solvedops)*(allbv+2*self.ops)
            values=['%.2f'%(rt),'%.2f'%(est),'%d/%d'%(solvedbv,allbv),'%.3f'%(solvedbv/rt),'%.3f'%(pow(est,1.7)/allbv)]
            values+=['%.2f'%(est*(est+1)/allbv),'%d/%d'%(self.solvedops,self.ops),'%d/%d'%(self.solvedislands,self.islands)]
            values+=['%d/%d/%d'%(self.allclicks[0],self.allclicks[1],self.allclicks[2])]
            values+=['%d'%(self.allclicks[3])]
            values+=['%d@%.3f'%(allclicks,allclicks/rt)]
            values+=['%d@%.3f'%(eclicks,eclicks/rt)]
            values+=['%.3f'%(ioe),'%.3f'%(corr),'%.3f'%(thrp)]
            for i in range(len(self.counterui.valuelabelarray)):
                self.counterui.valuelabelarray[i].setText(values[i])
        elif status==1:
            rt=self.intervaltime
            allbv='-'
            if eclicks==0:
                corr=0
            else:
                corr=eclicks/allclicks
            if rt==0:
                cls='-'
                ces='-'
            else:
                cls='%.3f'%(float(allclicks/rt))
                ces='%.3f'%(float(eclicks/rt))
            values=['%.2f'%(rt),'-','-','-','-','-','-','-']
            values+=['%d/%d/%d'%(self.allclicks[0],self.allclicks[1],self.allclicks[2])]
            values+=['%d'%(self.allclicks[3])]
            values+=['%d@%s'%(allclicks,cls)]
            values+=['%d@%s'%(eclicks,ces)]
            values+=['%s'%('-'),'%.3f'%(corr),'%s'%('-')]
            for i in range(len(self.counterui.valuelabelarray)):
                self.counterui.valuelabelarray[i].setText(values[i])
        
    def gameFinished(self,result,extra):
        if self.finish==True:
            return
        self.intervaltime=time.time()-self.starttime
        self.timer.stop()
        self.cal_3bv()
        self.changecounter(2)
        #self.label_3.setText("%.2f"%(self.intervaltime))
        self.showtimenum(self.intervaltime)
        for i in range(self.row):
            for j in range(self.column):
                if result==2:#输了
                    if self.label.num[i][j] == -1 or self.label.status[i][j] == 2:
                        if self.label.num[i][j] == -1 and self.label.status[i][j] == 2:
                            pass
                        elif self.label.num[i][j] == -1:
                            self.label.pressed[i][j]= 2
                        else:
                            self.label.pressed[i][j]= 3

                elif result==1:#赢了
                    if self.label.num[i][j]==-1 or self.label.status[i][j] == 2:
                        if self.label.num[i][j]==-1  and self.label.status[i][j] == 0:#游戏过程中未标上的雷
                            self.label.pressed[i][j]=5
                        elif self.label.num[i][j]==-1  and self.label.status[i][j] == 2:#游戏过程中标上的雷
                            pass
                        else:
                            self.label.pressed[i][j]=3
                #j.status = 1
        if result==2 and extra!=None:
            self.label.pressed[extra[0]][extra[1]]=4
        self.label.update()
        self.finish = True
        

    def isGameFinished(self):
        for i in range(self.row):
            for j in  range(self.column):
                if self.label.status[i][j] == 0 and self.label.num[i][j] != -1:
                    return False
        return True

    def gameWin(self):
        if self.gamemode==1:
            pixmap = QPixmap("media/svg/winface.svg")
        elif self.gamemode==2:
            pixmap = QPixmap("media/svg/winfaceblue.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/8.5)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)
        self.gameFinished(1,None)

    def gameFailed(self,i,j):
        if self.gamemode==1:
            pixmap = QPixmap("media/svg/lostface.svg")
        elif self.gamemode==2:
            pixmap = QPixmap("media/svg/lostfaceblue.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/8.5)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)
        if i==None and j==None:
            self.gameFinished(2,None)
        else:
            self.gameFinished(2,[i,j])

    def actionChecked(self, k):
        self.action_B.setChecked(False)
        self.action_I.setChecked(False)
        self.action_E.setChecked(False)
        self.action_C.setChecked(False)
        if k == 'B':
            self.action_B.setChecked(True)
        elif k == 'I':
            self.action_I.setChecked(True)
        elif k == 'E':
            self.action_E.setChecked(True)
        elif k == 'C':
            self.action_C.setChecked(True)

    def action_BEvent(self):
        self.actionChecked('B')
        oldrow,oldcolumn=self.row,self.column
        self.row = 8
        self.column = 8
        if oldrow==8 and oldcolumn==8:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.mineNum = 10
        self.newgameStart()
        self.needtorefresh=False

    def action_IEvent(self):
        self.actionChecked('I')
        oldrow,oldcolumn=self.row,self.column
        self.row = 16
        self.column = 16
        if oldrow==16 and oldcolumn==16:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.mineNum = 40
        self.newgameStart()
        self.needtorefresh=False


    def action_Event(self):
        self.actionChecked('E')
        oldrow,oldcolumn=self.row,self.column
        self.row = 16
        self.column = 30
        if oldrow==16 and oldcolumn==30:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.mineNum = 99
        self.newgameStart()
        self.needtorefresh=False

    def action_CEvent(self):
        self.actionChecked('C')
        ui = selfDefinedParameter.Ui_Dialog(self.row, self.column,
                                            self.mineNum)
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if ui.alter:
            self.row = ui.row
            self.column = ui.column
            self.mineNum = ui.mineNum
            self.needtorefresh=True
            self.newgameStart()
            self.needtorefresh=False

    def action_setevent(self):
        self.gameStart()
        self.counterWindow.close()
        ui = preference.Ui_SettingDialog()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()


    def findopis_bfs(self,i,j,num):
        for ii in range(i-1,i+2):
            if ii<0 or ii>=self.row:
                continue
            for jj in range(j-1,j+2):
                if jj<0 or jj>=self.column:
                    continue
                if num==1:
                    if self.label.num[ii][jj]>=0 and self.label.status[ii][jj]==0:
                        self.thisopsolved=False
                    if self.label.num[ii][jj]==0 and self.num0seen[ii][jj]==False:
                        self.num0seen[ii][jj]=True
                        self.num0get+=1
                        self.num0queue.put([ii,jj])
                elif num==2:
                    if self.isbv[ii][jj]==True and self.islandseen[ii][jj]==False:
                        if self.label.status[ii][jj]==0:
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
                if self.label.num[i][j]==0:
                    num0+=1
        for i in range(self.row):
            for j in range(self.column):
                if self.num0get==num0:#所有0被染色，标志op计算完全，终止
                    break
                if self.label.num[i][j]==0:
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
                if self.label.num[i][j]>0:
                    nearnum0=False
                    for ii in range(i-1,i+2):
                        if ii<0 or ii>=self.row:
                            continue
                        for jj in range(j-1,j+2):
                            if jj<0 or jj>=self.column:
                                continue
                            if self.label.num[ii][jj]==0:
                                nearnum0=True
                                break
                    if nearnum0==False:
                        self.isbv[i][j]=True
                        numelse+=1
                        if self.label.status[i][j]==1:
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
                        if self.label.status[i][j]==0:
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
        
    def gridup(self):
        if self.gridsize<=46:
            self.gridsize+=2
            self.label.pixSize=self.gridsize
            self.label.resizepixmaps(self.gridsize)
            num,status,pressed=[*self.label.num],[*self.label.status],[*self.label.pressed]
            self.initMineArea()
            self.label.num,self.label.status,self.label.pressed=num,status,pressed
            self.mainWindow.setMinimumSize(0, 0)
            self.mainWindow.resize(self.mainWindow.minimumSize())
            self.action_gridsize.setText('当前尺寸：%d'%(self.gridsize))
            self.action_griddown.setEnabled(True)
            if self.gridsize==48:
                self.action_gridup.setEnabled(False)
            
        
    def griddown(self):
        if self.gridsize>=14:
            self.gridsize-=2
            self.label.pixSize=self.gridsize
            self.label.resizepixmaps(self.gridsize)
            num,status,pressed=[*self.label.num],[*self.label.status],[*self.label.pressed]
            self.initMineArea()
            self.label.num,self.label.status,self.label.pressed=num,status,pressed
            self.label.update()
            self.mainWindow.setMinimumSize(0, 0)
            self.mainWindow.resize(self.mainWindow.minimumSize())
            self.action_gridsize.setText('当前尺寸：%d'%(self.gridsize))
            self.action_gridup.setEnabled(True)
            if self.gridsize==12:
                self.action_griddown.setEnabled(False)


            
