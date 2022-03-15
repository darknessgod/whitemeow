from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QLineEdit, QInputDialog
import superGUI, mineLabel,selfDefinedParameter
import random, sip
import time
import sys
from counter import Counter


class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.row = 16
        self.column = 16
        self.mineNum = 40
        self.leftHeld = False
        self.leftAndRightHeld = False  # 鼠标是否被按下的标志位
        self.oldCell = (0, 0)  # 鼠标的上个停留位置，用于绘制按下去时的阴影
        self.finish = False
        self.starttime=0
        self.mainWindow = MainWindow
        self.mainWindow.setWindowIcon(QIcon("media/mine.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.setupUi(self.mainWindow)
        self.mineLabel = []#局面
        self.num0seen=[]
        self.num0get=0
        self.ops=0
        self.solvedops=0
        self.bbbv=0
        self.solvedbbbv=0
        self.islands=0
        self.solvedislands=0
        self.intervaltime=0
        self.islandseen=[]
        self.isbv=[]
        self.allclicks=[0,0,0,0]
        self.eclicks=[0,0,0]
        self.counterWindow =None
        self.counterui=None
        self.thisislandsolved=False
        self.bvget=0
        
        pixmap0=QPixmap("media/10.png")
        pixmap1=QPixmap("media/11.png")
        pixmap2=QPixmap("media/12.png")
        pixmap3=QPixmap("media/13.png")
        pixmap4=QPixmap("media/14.png")
        pixmap5=QPixmap("media/15.png")
        pixmap6=QPixmap("media/16.png")
        pixmap7=QPixmap("media/17.png")
        pixmap8=QPixmap("media/18.png")
        pixmap9=QPixmap("media/00.png")
        pixmap10=QPixmap("media/03.png")
        self.pixmapNum={0:pixmap0,1:pixmap1,2:pixmap2,3:pixmap3,4:pixmap4,
                   5:pixmap5,6:pixmap6,7:pixmap7,8:pixmap8,9:pixmap9,10:pixmap10}
        
        self.initMineArea()
        self.createMine()
        self.label_2.leftRelease.connect(self.gameStart)
        pixmap = QPixmap("media/f0.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)  # 设置字体颜色
        self.label_3.setPalette(pe)
        self.label_3.setFont(QFont("Roman times", 12, QFont.Bold))
        self.label.setPalette(pe)
        self.label.setFont(QFont("Roman times", 12, QFont.Bold))
        self.label.setText(str(self.mineNum))
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeCount)
        self.timeStart = False

        # 绑定菜单栏事件
        self.showcounter()

        self.action.triggered.connect(self.gameStart)
        self.action_B.triggered.connect(self.action_BEvent)
        self.action_I.triggered.connect(self.action_IEvent)
        self.action_E.triggered.connect(self.action_Event)
        self.action_C.triggered.connect(self.action_CEvent)
        self.action_X_2.triggered.connect(QCoreApplication.instance().quit)
        self.action_counter.triggered.connect(self.showcounter)
        self.actionChecked('I')  # 默认选择中级
        
        


    def showcounter(self):
        self.action_counter.setChecked(True)
        self.counterWindow = QtWidgets.QMainWindow ()
        self.counterui = Counter(self.counterWindow)
        self.counterWindow.show()
        if self.finish==True:
            self.changecounter(2)
        else:
            self.changecounter(1)

        

    
    def outOfBorder(self, i, j):
        if i < 0 or i >= self.row or j < 0 or j >= self.column:
            return True
        return False

    def createMine(self):    #mineLabel[r][c].num是真实局面，-1为雷，数字为数字
        num = self.mineNum
        while num > 0:
            r = random.randint(0, self.row - 1)
            c = random.randint(0, self.column - 1)
            if self.mineLabel[r][c].num != -1:
                self.mineLabel[r][c].num = -1
                num -= 1
                for i in range(r - 1, r + 2):
                    for j in range(c - 1, c + 2):
                        if not self.outOfBorder(i, j) and (
                                self.mineLabel[i][j].num != -1):
                            self.mineLabel[i][j].num += 1

    def initMineArea(self):
        self.gridLayout.setSpacing(0)#网格布局间距为0
        for i in range(0, self.row):
            self.mineLabel.append([])
            for j in range(0, self.column):
                label = mineLabel.mineLabel(i, j, 0, "")
                label.setPixmap(self.pixmapNum[9])
                label.setMinimumSize(16, 16)
                label.setAlignment(Qt.AlignCenter)

                # 绑定雷区点击事件
                label.leftPressed.connect(self.mineAreaLeftPressed)
                label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
                label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
                label.leftRelease.connect(self.mineAreaLeftRelease)
                label.rightPressed.connect(self.mineAreaRightPressed)
                label.mouseMove.connect(self.mineMouseMove)
                label.setStyleSheet("border:0px solid red")

                self.mineLabel[i].append(label)
                self.gridLayout.addWidget(label, i, j)#把子控件添加到网格布局管理器中

    def timeCount(self):
        self.label_3.setText(str('%.0f'%((float(self.label_3.text()) + 1))))


    def DFS(self, i, j, start0):
        if self.mineLabel[i][j].status == 0:
            self.mineLabel[i][j].status = 1
            if self.mineLabel[i][j].num >= 0:
                if not self.timeStart:
                    self.timeStart = True
                    self.timer.start()
                    self.starttime=time.time()
                self.mineLabel[i][j].setPixmap(self.pixmapNum[self.mineLabel[i][j].num])
            if self.isGameFinished():
                self.gameWin()
            if self.mineLabel[i][j].num == 0:
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.mineLabel[r][
                            c].status == 0 and self.mineLabel[r][c].num != -1:
                            self.DFS(r, c, start0)
            elif self.mineLabel[i][j].num > 0:
                flagged=0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c) and self.mineLabel[r][
                            c].status == 2:
                            flagged+=1
                if flagged==self.mineLabel[i][j].num:
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c) and self.mineLabel[r][
                                c].status == 0 and self.mineLabel[r][c].num != -1:
                                self.DFS(r, c, start0)
                if self.isGameFinished():
                    self.gameWin()

    def mineAreaLeftRelease(self, i, j):
        if self.leftHeld and not self.finish:
            self.leftHeld = False  # 防止双击中的左键弹起被误认为真正的左键弹起
            self.allclicks[0]+=1
            self.changecounter(1)
            if not self.outOfBorder(i, j) and not self.finish:
                if self.mineLabel[i][j].status == 0:
                    self.eclicks[0]+=1
                    self.changecounter(1)
                    self.mineLabel[i][j].setPixmap(self.pixmapNum[9])
                    if self.mineLabel[i][j].num >= 0:
                        self.DFS(i, j, self.mineLabel[i][j].num == 0)
                        if self.isGameFinished():
                            self.gameWin()
                    else:
                        if not self.timeStart:#第一下不能为雷，第一下就赢了的事件也在这里写
                            self.mineLabel[i][j].num=0
                            while(True):
                                r = random.randint(0, self.row - 1)
                                c = random.randint(0, self.column - 1)
                                if self.mineLabel[r][c].num==-1 or (r==i and c==j):
                                    continue
                                self.mineLabel[r][c].num=-1
                                break
                            for ii in range(i - 1, i + 2):
                                for jj in range(j - 1, j + 2):
                                    if not self.outOfBorder(ii, jj) and self.mineLabel[ii][jj].num!=-1:     
                                        count=0
                                        for rr in range(ii - 1, ii + 2):
                                            for cc in range(jj - 1, jj + 2):
                                                if not self.outOfBorder(rr, cc) and self.mineLabel[rr][cc].num==-1:
                                                    count+=1
                                        self.mineLabel[ii][jj].num=count
                            for ii in range(r - 1, r + 2):
                                for jj in range(c - 1, c + 2):
                                    if not self.outOfBorder(ii, jj) and self.mineLabel[ii][jj].num!=-1:     
                                        count=0
                                        for rr in range(ii - 1, ii + 2):
                                            for cc in range(jj - 1, jj + 2):
                                                if not self.outOfBorder(rr, cc) and self.mineLabel[rr][cc].num==-1:
                                                    count+=1
                                        self.mineLabel[ii][jj].num=count
                            self.DFS(i, j, self.mineLabel[i][j].num == 0)
                            if self.isGameFinished():
                                self.gameWin()         
                        else:
                            self.gameFailed(i,j)

    def mineAreaRightPressed(self, i, j):
        if not self.finish:
            self.allclicks[1]+=1
            self.changecounter(1)
            if self.mineLabel[i][j].status == 0:
                self.eclicks[1]+=1
                self.allclicks[3]+=1
                self.changecounter(1)
                pixmap = QPixmap(self.pixmapNum[10])
                self.mineLabel[i][j].setPixmap(pixmap)
                self.mineLabel[i][j].setScaledContents(True)
                self.mineLabel[i][j].status = 2
                self.label.setText(str(int(self.label.text()) - 1))
            elif self.mineLabel[i][j].status == 2:
                self.eclicks[1]+=1
                self.allclicks[3]-=1
                self.changecounter(1)
                self.mineLabel[i][j].setPixmap(self.pixmapNum[9])
                self.mineLabel[i][j].status = 0
                self.label.setText(str(int(self.label.text()) + 1))
            elif self.mineLabel[i][j].status == 1 and self.mineLabel[i][j].num != 0:
                count=0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.mineLabel[r][c].status == 0 or self.mineLabel[r][c].status==2:
                                count += 1
                if count== self.mineLabel[i][j].num:
                    eright=False
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            if not self.outOfBorder(r, c):
                                if self.mineLabel[r][c].status == 0:
                                    self.mineLabel[r][c].status =2
                                    self.mineLabel[r][c].setPixmap(self.pixmapNum[10])
                                    self.allclicks[3]+=1
                                    eright=True
                                    self.label.setText(str(int(self.label.text()) - 1))
                    if eright==True:
                        self.eclicks[1]+=1
                        self.changecounter(1)

    def mineAreaLeftPressed(self, i, j):
        self.leftHeld = True
        self.oldCell = (i, j)
        if not self.finish:
            if self.mineLabel[i][j].status == 0:
                self.mineLabel[i][j].setPixmap(self.pixmapNum[0])

    def chordingFlag(self, i, j):
        # i, j 周围标雷数是否满足双击的要求
        if self.mineLabel[i][j].num <= 8 and self.mineLabel[i][j].num >= 0 and self.mineLabel[i][j].status==1:
            count = 0
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if not self.outOfBorder(r, c):
                        if self.mineLabel[r][c].status == 2:
                            count += 1
            if count == 0:
                return False
            else:
                return count == self.mineLabel[i][j].num
        else:
            return False

    def mineAreaLeftAndRightPressed(self, i, j):
#        return 0
        self.leftAndRightHeld = True
        self.oldCell = (i, j)
        if not self.finish:
            if self.mineLabel[i][j].status == 1:
                count = 0
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.mineLabel[r][c].status == 0:
                                self.mineLabel[r][c].setPixmap(self.pixmapNum[0])
                                #self.mineLabel[r][c].setFrameShape(QtWidgets.QFrame.Panel)
                                #self.mineLabel[r][c].setFrameShadow(QtWidgets.QFrame.Sunken)
                            elif self.mineLabel[r][c].status == 2:
                                count += 1
                return count == self.mineLabel[i][j].num
            else:
                return False


    def mineAreaLeftAndRightRelease(self, i, j):
        self.leftAndRightHeld = False
        self.leftHeld = False
        if not self.finish and not self.outOfBorder(i, j):
            self.allclicks[2]+=1
            self.changecounter(1)
            if self.chordingFlag(i, j):
                Fail = False
                edouble=False
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if not self.outOfBorder(r, c):
                            if self.mineLabel[r][c].status == 0:
                                edouble=True
                                if self.mineLabel[r][c].num >= 0:
                                    self.DFS(r, c, self.mineLabel[r][c].num == 0)
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
                            if self.mineLabel[r][c].status == 0:
                                self.mineLabel[r][c].setPixmap(self.pixmapNum[9])
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
                                    if self.mineLabel[r][c].status == 0:
                                        self.mineLabel[r][c].setPixmap(self.pixmapNum[9])
                        for r in range(i - 1, i + 2):
                            for c in range(j - 1, j + 2):
                                if not self.outOfBorder(r, c):
                                    if self.mineLabel[r][c].status == 0:
                                        self.mineLabel[r][c].setPixmap(self.pixmapNum[0])

                    elif self.leftHeld:
                        if self.mineLabel[i][j].status == 0:
                            self.mineLabel[i][j].setPixmap(self.pixmapNum[0])
                        if self.mineLabel[ii][jj].status == 0:
                            self.mineLabel[ii][jj].setPixmap(self.pixmapNum[9])
            elif self.leftAndRightHeld or self.leftHeld:
                ii, jj = self.oldCell
                if self.leftAndRightHeld:
                    for r in range(ii - 1, ii + 2):
                        for c in range(jj - 1, jj + 2):
                            if not self.outOfBorder(r, c):
                                if self.mineLabel[r][c].status == 0:
                                    self.mineLabel[r][c].setPixmap(self.pixmapNum[9])
                elif self.leftHeld:
                    if self.mineLabel[ii][jj].status == 0:
                        self.mineLabel[ii][jj].setPixmap(self.pixmapNum[9])

    def gameStart(self):
        for i in self.mineLabel:
            for j in i:
                self.gridLayout.removeWidget(j)
                sip.delete(j)
        self.label.setText(str(self.mineNum))
        pixmap = QPixmap("media/f0.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.label_3.setText("0")
        self.timeStart = False
        self.finish = False
        self.timer.stop()
        self.mineLabel.clear()
        self.mineLabel = []
        self.initMineArea()
        self.createMine()
        self.bbbv=0
        self.solvedbbbv=0
        self.ops=0
        self.solvedops=0
        self.intervaltime=0
        self.allclicks=[0,0,0,0]
        self.eclicks=[0,0,0]
        self.changecounter(1)
        self.mainWindow.setMinimumSize(0, 0)
        self.mainWindow.resize(self.mainWindow.minimumSize())

    def changecounter(self,status):
        #self.counterui.valuelabelarray[0].setText('%.2f'%(self.intervaltime))
        #状态2为游戏结束，状态1为游戏开始
        if status==1 and self.finish==True:
            return
        if status==2:
            rt=max(float(self.intervaltime),0.01)
            allbv=int(self.bbbv)
            solvedbv=int(self.solvedbbbv)
            allclicks=self.allclicks[0]+self.allclicks[1]+self.allclicks[2]
            eclicks=self.eclicks[0]+self.eclicks[1]+self.eclicks[2]
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
            rt=0
            allbv='-'
            allclicks=self.allclicks[0]+self.allclicks[1]+self.allclicks[2]
            eclicks=self.eclicks[0]+self.eclicks[1]+self.eclicks[2]
            if eclicks==0:
                corr=0
            else:
                corr=eclicks/allclicks
            values=['%.2f'%(rt),'-','-','-','-','-','-','-']
            values+=['%d/%d/%d'%(self.allclicks[0],self.allclicks[1],self.allclicks[2])]
            values+=['%d'%(self.allclicks[3])]
            values+=['%d@%s'%(allclicks,'-')]
            values+=['%d@%s'%(eclicks,'-')]
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
        self.label_3.setText("%d"%(int(self.intervaltime)))
        for i in self.mineLabel:
            for j in i:
                if result==2:#输了
                    if j.num == -1 or j.status == 2:
                        j.setFrameShape(QtWidgets.QFrame.Panel)
                        j.setFrameShadow(QtWidgets.QFrame.Sunken)
                        if j.num == -1 and j.status == 2:
                            pixmap = QPixmap("media/03.png")
                        elif j.num == -1:
                            pixmap = QPixmap("media/01.png")
                        else:
                            pixmap = QPixmap("media/04.png")
                        j.setPixmap(pixmap)
                        j.setScaledContents(True)
                elif result==1:#赢了
                    if j.num == -1 or j.status == 2:
                        j.setFrameShape(QtWidgets.QFrame.Panel)
                        j.setFrameShadow(QtWidgets.QFrame.Sunken)
                        if j.num == -1 and j.status == 0:#游戏过程中未标上的雷
                            pixmap = QPixmap("media/05.png")
                        elif j.num == -1 and j.status == 2:#游戏过程中标上的雷
                            pixmap = QPixmap("media/03.png")
                        else:
                            pixmap = QPixmap("media/04.png")
                        j.setPixmap(pixmap)
                        j.setScaledContents(True)
                #j.status = 1
        if result==2 and extra!=None:
            pixmap= QPixmap("media/02.png")
            self.mineLabel[extra[0]][extra[1]].setPixmap(pixmap)
        self.finish = True
        

    def isGameFinished(self):
        for i in self.mineLabel:
            for j in i:
                if j.status == 0 and j.num != -1:
                    return False
        return True

    def gameWin(self):
        pixmap = QPixmap("media/f3.png")
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
        self.gameFinished(1,None)

    def gameFailed(self,i,j):
        pixmap = QPixmap("media/f2.png")
        self.label_2.setPixmap(pixmap)
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
        self.row = 8
        self.column = 8
        self.mineNum = 10
        self.gameStart()

    def action_IEvent(self):
        self.actionChecked('I')
        self.row = 16
        self.column = 16
        self.mineNum = 40
        self.gameStart()


    def action_Event(self):
        self.actionChecked('E')
        self.row = 16
        self.column = 30
        self.mineNum = 99
        self.gameStart()

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
            self.gameStart()

    def findop_dfs(self,i,j,num):
        for ii in range(i-1,i+2):
            if ii<0 or ii>=self.row:
                continue
            for jj in range(j-1,j+2):
                if jj<0 or jj>=self.column:
                    continue
                if num==1:
                    if self.mineLabel[ii][jj].num==0 and self.num0seen[ii][jj]==False:
                        self.num0seen[ii][jj]=True
                        self.num0get+=1
                        self.findop_dfs(ii,jj,1)
                elif num==2:
                    if self.isbv[ii][jj]==True and self.islandseen[ii][jj]==False:
                        if self.mineLabel[ii][jj].status==0:
                            self.thisislandsolved=False
                        self.islandseen[ii][jj]=True
                        self.bvget+=1
                        self.findop_dfs(ii,jj,2)
                        

    def cal_3bv(self):
        self.islands=0
        self.solvedislands=0
        self.ops=0
        self.solvedops=0
        self.solvedbbbv=0
        solvedelse=0
        num0=0
        self.bvget=0
        self.num0seen = [[False for j in range(self.column)] for i in range(self.row)]
        self.islandseen = [[False for j in range(self.column)] for i in range(self.row)]
        self.isbv = [[False for j in range(self.column)] for i in range(self.row)]
        self.num0get=0
        numelse=0
        for i in range(self.row):
            for j in range(self.column):
                if self.mineLabel[i][j].num==0:
                    num0+=1
        for i in range(self.row):
            for j in range(self.column):
                if self.num0get==num0:
                    break
                if self.mineLabel[i][j].num==0:
                    if self.num0seen[i][j]==True:
                        continue
                    else:
                        self.ops+=1
                        if self.mineLabel[i][j].status==1:
                            self.solvedops+=1
                        self.num0seen[i][j]=True
                        self.num0get+=1
                        self.findop_dfs(i,j,1)
                        
        for i in range(self.row):
            for j in range(self.column):
                if self.mineLabel[i][j].num>0:
                    nearnum0=False
                    for ii in range(i-1,i+2):
                        if ii<0 or ii>=self.row:
                            continue
                        for jj in range(j-1,j+2):
                            if jj<0 or jj>=self.column:
                                continue
                            if self.mineLabel[ii][jj].num==0:
                                nearnum0=True
                                break
                    if nearnum0==False:
                        self.isbv[i][j]=True
                        numelse+=1
                        if self.mineLabel[i][j].status==1:
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
                        if self.mineLabel[i][j].status==0:
                            self.thisislandsolved=False
                        self.islandseen[i][j]=True
                        self.bvget+=1
                        self.findop_dfs(i,j,2)
                        if self.thisislandsolved==True:
                            self.solvedislands+=1
        self.bbbv=self.ops+numelse
        self.solvedbbbv=self.solvedops+solvedelse
        #print(self.islands,self.solvedislands)
