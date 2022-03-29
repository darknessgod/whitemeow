from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon ,QPainter
from PyQt5.QtWidgets import QLineEdit, QInputDialog
from gamestatus import gamestatus
import mainWindowGUI,superGUI, mineLabel,selfDefinedParameter,preference,gamestatus,newswindow,recordwindow
import time,struct
from counter import Counter,calbbbvThread


class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.game=gamestatus.gamestatus(16,16,40,[1,1])
        self.gridsize=32
        self.game.oldCell = (0, 0)  # 鼠标的上个停留位置，用于绘制按下去时的阴影
        self.mainWindow = MainWindow
        self.mainWindow.setWindowIcon(QIcon("media/mine.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.mainWindow.move(694,200)
        self.setupUi(self.mainWindow)
        self.counterWindow =None
        self.counterui=None
        self.label=None
        self.needtorefresh=True
        self.finish=False
        self.ctrlpressed=False

        self.resettimer()
        self.initMineArea()
        self.game.createMine(1)
        self.showcounter()
        self.label_2.leftRelease.connect(self.newgameStart)
        self.frame.leftRelease.connect(self.newgameStart)
        self.showface(8.5)
        self.showminenum(self.game.mineNum)
        self.showtimenum(self.game.intervaltime)
        self.connectactions()

    def counterback(self):
        self.showcounter()

    def replaying(self):
        return self.game.gametype==4 

    def showcounter(self):
        self.counterWindow = mainWindowGUI.meowcounter ()
        self.counterui = Counter(self.counterWindow,self.game)
        self.counterWindow.show()
        if self.finish==True:
            self.changecounter(2)
        else:
            self.changecounter(1)
        self.counterWindow.move(max(0,(self.mainWindow.x())-sum(self.counterui.columnwidth)),(max(0,self.mainWindow.y())))
        self.mainWindow.activateWindow()
   
    def initMineArea(self):
        for i in range(self.gridLayout.count()):
            w = self.gridLayout.itemAt(i).widget()
            w.setParent(None)
        self.label = mineLabel.mineLabel(self.game,self.gridsize)
        self.label.setMinimumSize(QtCore.QSize(self.gridsize*self.game.column, self.gridsize*self.game.row))
        self.label.leftPressed.connect(self.mineAreaLeftPressed)
        self.label.leftRelease.connect(self.mineAreaLeftRelease)
        self.label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
        self.label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
        self.label.rightPressed.connect(self.mineAreaRightPressed)
        self.label.rightRelease.connect(self.mineAreaRightRelease)
        self.label.setObjectName("label")
        self.label.resize(QtCore.QSize(self.gridsize*self.game.column, self.gridsize*self.game.row))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label.mouseMove.connect(self.mineMouseMove)
        
    def showface(self,num):
        if self.game.gametype==1:
            pixmap = QPixmap("media/svg/smileface.svg")
        elif self.game.gametype in [2,4]:
            pixmap = QPixmap("media/svg/smilefaceblue.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/num)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)

    def connectactions(self):
        self.action.triggered.connect(self.newgameStart)
        self.action_re.triggered.connect(self.gamereStart)
        self.action_B.triggered.connect(self.action_BEvent)
        self.action_I.triggered.connect(self.action_IEvent)
        self.action_E.triggered.connect(self.action_Event)
        self.action_C.triggered.connect(self.action_CEvent)
        self.action_saveboard.triggered.connect(self.saveboard)
        self.action_savereplay.triggered.connect(self.savereplay)
        self.action_loadboard.triggered.connect(self.loadboard)
        self.action_loadreplay.triggered.connect(self.loadreplay)
        self.action_record.triggered.connect(self.action_showrecord)
        self.action_X_2.triggered.connect(QCoreApplication.instance().quit)
        self.action_counter.triggered.connect(self.showcounter)
        self.action_settings.triggered.connect(self.action_setevent)
        self.action_gridup.triggered.connect(self.gridup)
        self.action_griddown.triggered.connect(self.griddown)
        self.mainWindow.closeEvent_.connect(self.counterWindow.close)
        self.mainWindow.gridupdownEvent.connect(self.wheelupdown)
        self.mainWindow.ctrlpressEvent.connect(self.ctrlpress)
        self.mainWindow.ctrlreleaseEvent.connect(self.ctrlrelease)
        self.mainWindow.minbackEvent.connect(self.counterback)
        self.action_gridsize.setText('当前尺寸：%d'%(self.gridsize))
        self.actionChecked('I')  # 默认选择中级

    def timeCount(self):
        self.oldinttime=int(self.game.intervaltime+0.9999)
        self.game.intervaltime=time.time()-self.game.starttime
        inttime=int(self.game.intervaltime+0.9999)
        if inttime!=self.game.oldinttime:
            self.showtimenum(self.game.intervaltime)
        if self.game.gametype!=4:
            self.changecounter(1)
        else:
            while(1):
                k1=self.game.replaynodes[0]
                if k1==len(self.game.operationlist):
                    break
                if self.game.operationlist[k1][3]>=1000*(self.game.intervaltime):
                    break
                else:
                    self.dooperation(self.game.operationlist[k1][0],self.game.operationlist[k1][1],self.game.operationlist[k1][2])
                    self.game.replaynodes[0]+=1
            while(1):
                k2=self.game.replaynodes[1]
                if k2==len(self.game.tracklist):
                    break
                if self.game.tracklist[k2][2]>1000*(self.game.intervaltime):
                    break
                self.game.cursorplace=[self.game.tracklist[k2][0],self.game.tracklist[k2][1]]
                self.mineMouseMove(self.game.cursorplace[0]//100,self.game.cursorplace[1]//100)
                self.game.replaynodes[1]+=1
            if k2>0:
                self.game.path=self.game.pathlist[k2-1]
            else:
                self.game.path=0
            self.label.update()
            self.changecounter(2)
                    


    def resettimer(self):
        self.timer = QTimer()
        self.timer.setInterval(43)
        self.timer.timeout.connect(self.timeCount)
        self.game.timeStart = False

    def mineAreaLeftPressed(self, i, j):
        if not self.finish:
            if not self.replaying():
                self.game.addoperation(1,i,j)
            self.game.leftHeld = True
            self.game.oldCell = (i, j)
            if self.game.status[i][j] == 0:
                self.game.pressed[i][j]=1
                self.label.update()

    def mineAreaLeftRelease(self, i, j):
        if self.game.leftHeld and not self.finish:
            if not self.replaying():
                self.game.addoperation(2,i,j)
            self.game.leftHeld = False  # 防止双击中的左键弹起被误认为真正的左键弹起
            if not self.game.outOfBorder(i, j) and not self.finish:
                self.game.failed=False
                self.game.doleft(i,j)
                self.changecounter(1)
                if not self.game.timeStart:
                    self.game.timeStart = True
                    self.timer.start()
                    self.setshortcuts(False)
                    if self.game.isreplaying():
                        self.counterthread=calbbbvThread(self.game)
                        self.counterthread.start()
                    self.game.starttime=time.time()
                self.label.update()
                if self.game.failed==True:
                    self.gameFailed(self.game.redmine[0],self.game.redmine[1])
                elif self.isGameFinished()==True:
                    self.gameWin()
               

    def mineAreaRightPressed(self, i, j):
        if not self.finish:
            if not self.replaying():
                self.game.addoperation(3,i,j)
            self.game.doright(i,j)
            self.label.update()
            self.showminenum(self.game.mineNum-self.game.allclicks[3])
            self.changecounter(1)
            
    def mineAreaRightRelease(self, i, j):
        if not self.finish:
            if not self.replaying():
                self.game.addoperation(4,i,j)

    def mineAreaLeftAndRightPressed(self, i, j):
        if not self.finish:
            if not self.replaying():
                self.game.addoperation(5,i,j)
            self.game.leftAndRightHeld = True
            self.game.oldCell = (i, j)
            self.game.pressdouble(i,j)
            self.label.update()

    def mineAreaLeftAndRightRelease(self, i, j):
        if not self.finish:
            self.game.leftAndRightHeld = False
            self.game.leftHeld = False
            if not self.replaying():
                self.game.addoperation(6,i,j)
            if not self.game.outOfBorder(i, j):
                self.game.failed=False
                self.game.dodouble(i,j)
                self.changecounter(1)
                self.label.update()
                if self.game.failed==True:
                    self.gameFailed(self.game.redmine[0],self.game.redmine[1])
                elif self.isGameFinished()==True:
                    self.gameWin()

    def mineMouseMove(self, i, j):
        if not self.finish:
            self.game.domove(i,j)
            self.label.update()
 
    def gamereStart(self):
        self.game.gametype=2
        self.gameStart()

    def newgameStart(self):
        self.game.gametype=1
        self.gameStart()

    def replaygameStart(self):
        self.game.gametype=4
        self.gameStart()

    def gameStart(self):
        if self.needtorefresh==True:
            for i in range(self.gridLayout.count()):
                w = self.gridLayout.itemAt(i).widget()
                w.setParent(None)
        self.showface(8.5)
        self.showminenum(self.game.mineNum)
        self.finish = False
        self.timer.stop()
        if self.needtorefresh==True:
            self.initMineArea()
        self.game.renewminearea()
        self.label.update()
        self.label.lastcell=None
        self.game.createMine(self.game.gametype)
        self.game.renewstatus()
        self.setshortcuts(True)
        self.action_saveboard.setEnabled(False)
        self.action_savereplay.setEnabled(False)
        self.game.gamenum,self.game.ranks=self.gamescount(),[0,0,0]
        self.changecounter(1)
        self.showtimenum(self.game.intervaltime)
        if self.needtorefresh==True:
            windowsize=self.calwindowsize(self.game.row,self.game.column,self.gridsize)
            self.mainWindow.setFixedSize(windowsize[0],windowsize[1])
            self.mainWindow.resize(self.mainWindow.minimumSize())
        self.needtorefresh=False

    def changecounter(self,status):
        if status==1 and self.finish==True:
            return
        else:
            self.counterui.refreshvalues(status)
        
        
    def gameFinished(self,result):
        if self.finish==True:
            return
        self.game.endtime=time.time()
        if self.game.isreplaying():
            self.counterthread.terminate()
            self.counterthread.quit()
            self.game.intervaltime=self.game.replayboardinfo[5]
        else:
            self.game.intervaltime=max(float('%.2f'%(self.game.endtime-self.game.starttime-0.005)),0.01)
        self.timer.stop()
        self.game.cal_3bv()
        if result==1:
            if self.game.gametype==1:
                self.game.gamenum+=1
            score=[self.game.intervaltime,self.game.bbbv/self.game.intervaltime,(self.game.intervaltime**1.7)/self.game.bbbv]
            if self.game.gametype!=4:
                self.game.ranks=self.gamerank(score)
        self.changecounter(2)
        self.showtimenum(self.game.intervaltime)
        self.game.dofinish(result)
        self.label.update()
        self.finish = True
        self.game.finish=True
        if result==1 and self.game.gametype==1:
            self.savethisgame()
        self.setshortcuts(True)
        #print(self.game.operationlist)
        #print(self.game.tracklist)

    def isGameFinished(self):
        for i in range(self.game.row):
            for j in  range(self.game.column):
                if self.game.status[i][j] !=1 and self.game.num[i][j] != -1:
                    return False
        return True

    def gameWin(self):
        if self.game.gametype==1:
            pixmap = QPixmap("media/svg/winface.svg")
        elif self.game.gametype==2 or 4:
            pixmap = QPixmap("media/svg/winfaceblue.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/8.5)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)
        self.gameFinished(1)

    def gameFailed(self,i,j):
        if self.game.gametype==1:
            pixmap = QPixmap("media/svg/lostface.svg")
        elif self.game.gametype==2 or 4:
            pixmap = QPixmap("media/svg/lostfaceblue.svg")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/8.5)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setScaledContents(True)
        self.gameFinished(2)

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
        oldrow,oldcolumn=self.game.row,self.game.column
        self.game.row = 8
        self.game.column = 8
        if oldrow==8 and oldcolumn==8:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.game.mineNum = 10
        self.newgameStart()

    def action_IEvent(self):
        self.actionChecked('I')
        oldrow,oldcolumn=self.game.row,self.game.column
        self.game.row = 16
        self.game.column = 16
        if oldrow==16 and oldcolumn==16:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.game.mineNum = 40
        self.newgameStart()


    def action_Event(self):
        self.actionChecked('E')
        oldrow,oldcolumn=self.game.row,self.game.column
        self.game.row = 16
        self.game.column = 30
        if oldrow==16 and oldcolumn==30:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.game.mineNum = 99
        self.newgameStart()

    def action_CEvent(self):
        self.actionChecked('C')
        ui = selfDefinedParameter.Ui_Dialog(self.game.row, self.game.column,
                                            self.game.mineNum)
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if ui.alter:
            self.game.row = ui.row
            self.game.column = ui.column
            self.game.mineNum = ui.mineNum
            self.needtorefresh=True
            self.newgameStart()

    def action_showrecord(self):
        if self.finish==False:
            self.gameStart()
        mainpos=[self.mainWindow.x(),self.mainWindow.y(),self.mainWindow.width(),self.mainWindow.height()]
        recordui=recordwindow.ui_recorddialog(mainpos,self.datas.records)
        recordui.Dialog.setModal(True)
        recordui.Dialog.show()
        recordui.Dialog.exec_()        

    def action_setevent(self):
        self.gameStart()
        ui = preference.Ui_SettingDialog()
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()

    def ctrlpress(self):
        self.ctrlpressed=True

    def ctrlrelease(self):
        self.ctrlpressed=False       

    def wheelupdown(self,direction):
        if self.ctrlpressed==True:
            if direction>0:
                self.griddown()
            elif direction<0:
                self.gridup()
                        
    def gridup(self):
        if self.gridsize<=46:
            self.gridsize+=2
            self.label.pixSize=self.gridsize
            self.label.resizepixmaps(self.gridsize)
            num,status,pressed=[*self.game.num],[*self.game.status],[*self.game.pressed]
            self.initMineArea()
            self.game.num,self.game.status,self.game.pressed=num,status,pressed
            windowsize=self.calwindowsize(self.game.row,self.game.column,self.gridsize)
            self.mainWindow.setFixedSize(windowsize[0],windowsize[1])
            self.action_gridsize.setText('当前尺寸：%d'%(self.gridsize))
            self.action_griddown.setEnabled(True)
            if self.gridsize==48:
                self.action_gridup.setEnabled(False)
            
        
    def griddown(self):
        if self.gridsize>=14:
            self.gridsize-=2
            self.label.pixSize=self.gridsize
            self.label.resizepixmaps(self.gridsize)
            num,status,pressed=[*self.game.num],[*self.game.status],[*self.game.pressed]
            self.initMineArea()
            self.game.num,self.game.status,self.game.pressed=num,status,pressed
            windowsize=self.calwindowsize(self.game.row,self.game.column,self.gridsize)
            self.mainWindow.setFixedSize(windowsize[0],windowsize[1])
            self.action_gridsize.setText('当前尺寸：%d'%(self.gridsize))
            self.action_gridup.setEnabled(True)
            if self.gridsize==12:
                self.action_griddown.setEnabled(False)
            
    def generatedata(self):
        thisgamedata=[]
        finishtime=list(time.localtime(self.game.endtime))
        thisgamedata+=[finishtime[2],finishtime[1],finishtime[0]]
        thisgamedata+=finishtime[3:6]
        thisgamedata.append(self.game.intervaltime)
        thisgamedata.append(self.game.bbbv)
        thisgamedata.append(self.game.gamemode)
        thisgamedata.append(self.game.leveljudge())
        thisgamedata.append(self.game.stylejudge())
        thisgamedata+=self.game.allclicks[0:3]
        thisgamedata+=self.game.eclicks
        thisgamedata+=[self.game.ops,self.game.islands,float('%.2f'%(self.game.path))]
        return thisgamedata

    def savethisgame(self):
        thisgameinfo=self.generatedata()
        self.datas.addtostats(thisgameinfo)
        self.datas.writestats()
        if len(thisgameinfo[self.datas.numlevel])==3:
            #recordindex=self.datas.dict1[thisgameinfo[self.datas.numstyle]]+self.datas.dict2[thisgameinfo[self.datas.numlevel]]
            breakrecord=self.datas.judgerecord(thisgameinfo)
            if sum(breakrecord)>=1:
                self.shownews(breakrecord,self.game.stylejudge())
                self.savereplay()

    def gamescount(self):
        level=self.game.leveljudge()
        count=0
        for s in self.datas.stats:
            if s[self.datas.numlevel]==level:
                count+=1
        return count

    def gamerank(self,score):
        level=self.game.leveljudge()
        style=self.game.stylejudge()
        ranks=[1,1,1]
        for s in self.datas.stats:
            if s[self.datas.numlevel]==level and s[self.datas.numstyle]==style:
                if score[0]>s[self.datas.numrt]:
                    ranks[0]+=1
                if score[1]<s[self.datas.numbbbv]/s[self.datas.numrt]:
                    ranks[1]+=1
                if score[2]>(s[self.datas.numrt]**1.7)/s[self.datas.numbbbv]:
                    ranks[2]+=1
        return ranks

    def shownews(self,breakrecord,style):
        mainpos=[self.mainWindow.x(),self.mainWindow.y(),self.mainWindow.width(),self.mainWindow.height()]
        window=newswindow.news_Dialog(mainpos,breakrecord,style)
        window.Dialog.setModal(True)
        window.Dialog.show()
        window.Dialog.exec_()

    def calwindowsize(self,row,column,size):
        height=135+row*size
        width=max(153,column*size+24)
        return [width,height]

    def setshortcuts(self,state):
        self.action_X_2.setEnabled(state)
        self.action_loadboard.setEnabled(state)
        self.action_saveboard.setEnabled(state)
        self.action_savereplay.setEnabled(state)
        self.action_loadreplay.setEnabled(state)

    def saveboard(self):
        if self.game.finish==False:
            return
        boardlist=self.game.getboardlist()
        abf=bytes(boardlist)
        ft=list(time.localtime(time.time()))
        filename='%dx%d_%dmines_%d_%d_%d_%d_%d_%d.abf'%(self.game.column,self.game.row,
        self.game.mineNum,ft[0],ft[1],ft[2],ft[3],ft[4],ft[5])
        with open(r"%s"%(filename),'wb') as f:
            f.write(abf)

    def loadboard(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow,'载入局', '', '(board file *.abf *.mbf)')
        if fname[0]:
            f = open(fname[0], 'rb')
            with f:
                boardlist=[]
                while(True):
                    data= f.read(1)
                    if data==b'':
                        break
                    num=struct.unpack('B',data)
                    boardlist.append(num[0])
            f.close()
            status=self.game.dealboard(boardlist)
            if status==0:
                self.needtorefresh=True
                self.gamereStart()

    def savereplay(self):
        if self.game.finish==False:
            return
        boardlist=self.game.getboardlist()
        boardinfo=self.game.getboardinfo()
        replay=[len(boardinfo),len(boardlist),len(self.game.operationlist),len(self.game.tracklist)]
        replay+=boardinfo
        replay+=boardlist
        replay+=self.game.operationlist
        replay+=self.game.tracklist
        self.datas.makereplayfile(replay)

    def loadreplay(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow,'播放录像', '', '(video file *.nvf)')
        if fname[0]:
            f = open(fname[0], 'rb')
            replay=self.datas.picklereplay(f)
            f.close()
            self.game.replay=[*replay]
            del replay
            status=self.game.dealreplay()
            if status==0:
                self.needtorefresh=True
                self.playnvf()
            else:
                print(status)
                self.newgameStart()
                    

    def playnvf(self):
        print(self.game.operationlist[1:20])
        print(self.game.tracklist[50:100])
        self.replaygameStart()
        self.label.update()
        self.game.cal_3bv()
        self.game.replaynodes=[0,0]
        start=self.game.dopreoperations()
        self.dooperation(1,start[0],start[1])
        self.dooperation(2,start[0],start[1])



    def dooperation(self,num,i,j):
        if num==1:
            self.mineAreaLeftPressed(i,j)
        elif num==2:
            self.mineAreaLeftRelease(i,j)
        elif num==3:
            self.mineAreaRightPressed(i,j)
        elif num==4:
            self.mineAreaRightRelease(i,j)
        elif num==5:
            self.mineAreaLeftAndRightPressed(i,j)
        elif num==6:
            self.mineAreaLeftAndRightRelease(i,j)

    


