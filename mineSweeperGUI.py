from tkinter import VERTICAL
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon ,QPainter
from PyQt5.QtWidgets import QLineEdit, QInputDialog
from gamestatus import gamestatus
import mainWindowGUI,superGUI, mineLabel,window_custom,window_settings,gamestatus,window_news,window_record
import time,struct
from window_counter import Counter
from constants import *




class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.mainWindow = MainWindow        
        self.mainWindow.setWindowIcon(QIcon("media/mine.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.mainWindow.move(694,200)
        self.maxsize=[1000,800]
        self.widthmargin,self.heightmargin=24,135

        self.setupUi(self.mainWindow)
        if self.options.settings['defaultlevel']=='beg':
            self.game=gamestatus.gamestatus(8,8,10,self.options.settings)
        elif self.options.settings['defaultlevel']=='exp':
            self.game=gamestatus.gamestatus(16,30,99,self.options.settings)
        else:
            self.game=gamestatus.gamestatus(16,16,40,self.options.settings)
        
        self.gridsize=32
        self.game.oldCell = 0  # 鼠标的上个停留位置，用于绘制按下去时的阴影

        self.counterWindow =None
        self.counterui=None
        self.label=None
        self.needtorefresh=True
        self.finish=False
        self.ctrlpressed,self.zpressed=False,False
        
        

        self.resettimer()
        self.initMineArea()
        self.game.createMine(1)
        self.showcounter()
        self.label_2.leftRelease.connect(self.newgameStart)
        self.frame.leftRelease.connect(self.newgameStart)
        self.showface(8.5)
        if not self.options.settings['showsafesquares']:
            self.showminenum(self.game.mineNum)
        else:
            self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
        self.showtimenum(self.game.intervaltime)
        self.connectactions()

    def counterback(self):
        self.counterWindow.setVisible(True)

    def hidecounter(self):
        self.counterWindow.setVisible(False)

    def showcounter(self):
        self.counterWindow = mainWindowGUI.meowcounter ()
        self.counterui = Counter(self.counterWindow,self.game)
        self.counterWindow.show()
        if self.finish==True:
            self.changecounter(2)
        else:
            self.changecounter(1)
        self.counterWindow.move(max(0,(self.mainWindow.x())-sum(self.counterui.columnwidth)),(max(0,self.mainWindow.y())))
        self.counterWindow.activateWindow()
        self.mainWindow.activateWindow()
        self.mainWindow.closeEvent_.connect(self.counterWindow.close)
        self.mainWindow.minbackEvent.connect(self.counterback)

   
    def initMineArea(self):
        for i in range(self.gridLayout.count()):
            w = self.gridLayout.itemAt(i).widget()
            w.setParent(None)
        #self.gridLayout.removeWidget(self.scrollArea)
        self.label = mineLabel.mineLabel(self.game,self.gridsize)
        self.label.setMinimumSize(QtCore.QSize(self.gridsize*self.game.column-2, self.gridsize*self.game.row-2))
        self.label.leftPressed.connect(self.mineAreaLeftPressed)
        self.label.leftRelease.connect(self.mineAreaLeftRelease)
        self.label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
        self.label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
        self.label.rightPressed.connect(self.mineAreaRightPressed)
        self.label.rightRelease.connect(self.mineAreaRightRelease)
        self.label.setObjectName("label")
        self.label.resize(QtCore.QSize(self.gridsize*self.game.column-2, self.gridsize*self.game.row-2))
        self.scroll_area = QtWidgets.QScrollArea(self.mainWindow)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedWidth(min(self.maxsize[0]-self.widthmargin,self.game.column*self.gridsize))
        self.scroll_area.setFixedHeight(min(self.maxsize[1]-self.heightmargin,self.game.row*self.gridsize))
        self.scroll_area.wheelEvent=self.wheelscroll
        #self.scrollbar = QtWidgets.QScrollBar(Qt.Horizontal)
        #self.scrollbar2 = QtWidgets.QScrollBar(Qt.Vertical)
        #self.scrollbar.setMaximum(self.scroll_area.horizontalScrollBar().maximum())
        #self.scrollbar2.setMaximum(self.scroll_area.verticalScrollBar().maximum())
        self.gridLayout.addWidget(self.scroll_area,0,0,1,1)
        #self.gridLayout.addWidget(self.scrollbar,1,0,1,1)
        #self.gridLayout.addWidget(self.scrollbar2,0,1,1,1)
        self.gridLayout.setSpacing(0)
        self.label.mouseMove.connect(self.mineMouseMove)
        
    def showface(self,scale):
        facenum=[0,0]#第一位：颜色 0黄1蓝 #第二位：状态 0正常1输2赢
        if self.game.gametype==4:
            if self.game.replayboardinfo[8]==1:
                facenum[0]=0
            elif self.game.replayboardinfo[8]==2:
                facenum[0]=1
        elif self.game.gametype==1:
            facenum[0]=0
        elif self.game.gametype==2:
            facenum[0]=1
        if not self.game.finish:
            facenum[1]=0
        elif self.game.result==2:
            facenum[1]=1
        elif self.game.result==1:
            facenum[1]=2
        facepixmaps=["smileface","lostface","winface"]
        facecolors=["","blue"]
        pixmapname=facepixmaps[facenum[1]]
        pixmapname+=facecolors[facenum[0]]
        pixmapname+=".svg"
        pixmap = QPixmap(FACE_PATH + pixmapname)
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/scale)
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
        self.mainWindow.closeEvent_.connect(self.hidecounter)
        self.mainWindow.gridupdownEvent.connect(self.wheelupdown)
        self.mainWindow.keypressEvent.connect(self.keypress)
        self.mainWindow.keyreleaseEvent.connect(self.keyrelease)
        self.mainWindow.minbackEvent.connect(self.counterback)
        self.action_gridsize.setText(_('当前尺寸:%d')%(self.gridsize))
        self.actionChecked(self.options.settings['defaultlevel'])  # 默认选择中级

    def timeCount(self):
        self.oldinttime=int(self.game.intervaltime+0.9999)
        self.game.intervaltime=time.time()-self.game.starttime
        inttime=int(self.game.intervaltime+0.9999)
        if inttime!=self.game.oldinttime and self.options.settings['timeringame']:
            self.showtimenum(self.game.intervaltime)
        if not self.game.isreplaying():
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
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.timeCount)
        self.game.timeStart = False

    def mineAreaLeftPressed(self, i, j):
        if not self.finish:
            if not self.game.isreplaying():
                self.game.addoperation(1,i,j)
            self.game.leftHeld = True
            self.game.oldCell = self.game.getindex(i, j)
            self.label.update()
            if self.options.settings['instantclick']:
                self.mineAreaLeftRelease(i,j)

    def mineAreaLeftRelease(self, i, j):
        if self.game.leftHeld and not self.finish:
            if not self.game.isreplaying():
                self.game.addoperation(2,i,j)
            self.game.leftHeld = False  # 防止双击中的左键弹起被误认为真正的左键弹起
            if not self.game.outOfBorder(i, j) and not self.finish:
                self.game.failed=False
                self.game.doleft(self.game.getindex(i, j))
                self.changecounter(1)
                if not self.game.timeStart:
                    self.game.timeStart = True
                    self.timer.start()
                    self.setshortcuts(False)
                    self.game.starttime=time.time()
                self.label.update()
                if self.game.failed==True:
                    self.gameFailed()
                else:
                    if self.options.settings['showsafesquares']:
                        self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
                    if self.isGameFinished()==True:
                        self.gameWin()
               

    def mineAreaRightPressed(self, i, j):
        if not self.finish and not self.game.settings['disableright']:
            if not self.game.isreplaying():
                self.game.addoperation(3,i,j)
            self.game.doright(self.game.getindex(i, j))
            self.label.update()
            if not self.options.settings['showsafesquares']:
                self.showminenum(self.game.mineNum-self.game.allclicks[3])
            self.changecounter(1)
            if self.options.settings['instantclick']:
                self.mineAreaRightRelease(i,j)
            
    def mineAreaRightRelease(self, i, j):
        if not self.finish and not self.game.settings['disableright']:
            if not self.game.isreplaying():
                self.game.addoperation(4,i,j)

    def mineAreaLeftAndRightPressed(self, i, j):
        if not self.finish:
            if not self.game.isreplaying():
                self.game.addoperation(5,i,j)
            self.game.leftAndRightHeld = True
            self.game.oldCell = self.game.getindex(i, j)
            self.game.pressdouble(self.game.getindex(i, j))
            self.label.update()
            if self.options.settings['instantclick']:
                self.mineAreaLeftAndRightRelease(i,j)

    def mineAreaLeftAndRightRelease(self, i, j):
        if not self.finish:
            self.game.leftAndRightHeld = False
            self.game.leftHeld = False
            if not self.game.isreplaying():
                self.game.addoperation(6,i,j)
            if not self.game.outOfBorder(i, j):
                self.game.failed=False
                self.game.dodouble(self.game.getindex(i, j))
                self.changecounter(1)
                self.label.update()
                if self.game.failed==True:
                    self.gameFailed()
                else:
                    if self.options.settings['showsafesquares']:
                        self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
                    if self.isGameFinished()==True:
                        self.gameWin()
                
                    
    def mineMouseMove(self, i, j):
        if not self.finish:
            self.game.domove(self.game.getindex(i,j))
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
            for i in range(self.gridLayout.count()-2):
                w = self.gridLayout.itemAt(i).widget()
                w.setParent(None)
        self.game.settings=self.options.settings
        self.finish = False
        self.timer.stop()
        if self.needtorefresh==True:
            self.initMineArea()
        self.game.renewminearea()
        self.label.update()
        self.label.lastcell=None
        self.game.createMine(self.game.gametype)
        self.game.renewstatus()
        if not self.options.settings['showsafesquares']:
            self.showminenum(self.game.mineNum)
        else:
            self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
        self.setshortcuts(True)
        self.action_saveboard.setEnabled(False)
        self.action_savereplay.setEnabled(False)
        self.game.gamenum,self.game.ranks=self.gamescount(),[0,0,0]
        self.changecounter(1)
        self.showtimenum(self.game.intervaltime)
        self.showface(8.5)
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
            self.game.intervaltime=self.game.replayboardinfo[5]
        else:
            self.game.intervaltime=max(float('%.2f'%(self.game.endtime-self.game.starttime-0.005)),0.01)
        self.timer.stop()
        if not self.game.isreplaying():
            self.game.cal_3bv_solved()
        if result==1:
            if self.game.gametype==1:
                self.game.gamenum+=1
            score=[self.game.intervaltime,self.game.bbbv/self.game.intervaltime,(self.game.intervaltime**1.7)/self.game.bbbv]
            if not self.game.isreplaying():
                self.game.ranks=self.gamerank(score)
        self.changecounter(2)
        self.showtimenum(self.game.intervaltime)
        self.game.dofinish()
        self.label.update()
        self.finish = True
        self.game.finish=True
        if result==1 and self.game.gametype==1:
            self.savethisgame()
        self.setshortcuts(True)
        if self.game.isreplaying():
            self.action_savereplay.setEnabled(False)
        if self.game.failed and self.options.settings['failrestart']:
            p=(self.game.solvedelse+self.game.solvedops)*100/self.game.bbbv
            if p<self.options.settings['failrestart_percentage']:
                self.newgameStart()

    def isGameFinished(self):
        for i in range(self.game.row*self.game.column):
            if not self.game.isOpened(i) and not self.game.isMine(i):
                return False
        return True

    def gameWin(self):
        self.game.result=1
        self.gameFinished(self.game.result)
        self.showface(8.5)

    def gameFailed(self):
        self.game.result=2
        self.gameFinished(self.game.result)
        self.showface(8.5)

    def actionChecked(self, k):
        self.action_B.setChecked(False)
        self.action_I.setChecked(False)
        self.action_E.setChecked(False)
        self.action_C.setChecked(False)
        if k == 'beg':
            self.action_B.setChecked(True)
        elif k == 'int':
            self.action_I.setChecked(True)
        elif k == 'exp':
            self.action_E.setChecked(True)
        elif k == 'cus':
            self.action_C.setChecked(True)

    def action_bie(self,r,c,m):
        oldrow,oldcolumn=self.game.row,self.game.column
        self.game.row = r
        self.game.column = c
        if oldrow==r and oldcolumn==c:
            self.needtorefresh=False
        else:
            self.needtorefresh=True
        self.game.mineNum = m
        self.newgameStart()

    def action_BEvent(self):
        self.actionChecked('beg')
        self.action_bie(8,8,10)
        
    def action_IEvent(self):
        self.actionChecked('int')
        self.action_bie(16,16,40)

    def action_Event(self):
        self.actionChecked('exp')
        self.action_bie(16,30,99)

    def action_CEvent(self):
        self.actionChecked('cus')
        ui = window_custom.Ui_Dialog(self.game.row, self.game.column,
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
        recordui=window_record.ui_recorddialog(mainpos,self.datas.records)
        recordui.Dialog.setModal(True)
        recordui.Dialog.show()
        recordui.Dialog.exec_()        

    def action_setevent(self):
        if self.game.gametype==4:
            self.game.gametype=self.game.replayboardinfo[8]
        self.gameStart()
        uiwindow = mainWindowGUI.meowsettings()
        ui = window_settings.Ui_SettingDialog(uiwindow,self.options)
        ui.Dialog.setModal(True)
        ui.Dialog.show()
        ui.Dialog.exec_()
        if not self.game.finish:
            self.gameStart()
        self.resetplayertag()

    def keypress(self,keynum):
        if keynum==1:
            self.ctrlpressed=True
        elif keynum==2:
            self.zpressed=True

    def keyrelease(self,keynum):
        if keynum==1:
            self.ctrlpressed=False
        elif keynum==2:
            self.zpressed=False     

    def wheelupdown(self,direction):
        if self.ctrlpressed:
            if direction>0:
                self.griddown()
            elif direction<0:
                self.gridup()
                        
    def wheelscroll(self,e):
        if self.ctrlpressed:
            return
        elif self.zpressed:
            horizontal_bar=self.scroll_area.horizontalScrollBar()
            deltay=-e.angleDelta().y()
            v=horizontal_bar.value()+deltay
            v=max(min(v,horizontal_bar.maximum()),horizontal_bar.minimum())
            horizontal_bar.setValue(v)
        else:
            vertical_bar=self.scroll_area.verticalScrollBar()
            deltay=-e.angleDelta().y()
            v=vertical_bar.value()+deltay
            v=max(min(v,vertical_bar.maximum()),vertical_bar.minimum())
            vertical_bar.setValue(v)

    def gridup(self):
        if self.gridsize<=46:
            self.gridsize+=2
            self.label.pixSize=self.gridsize
            self.label.resizepixmaps(self.gridsize)
            num,status=[*self.game.num],[*self.game.status]
            self.initMineArea()
            self.game.num,self.game.status=num,status
            windowsize=self.calwindowsize(self.game.row,self.game.column,self.gridsize)
            self.mainWindow.setFixedSize(windowsize[0],windowsize[1])
            self.action_gridsize.setText(_('当前尺寸：%d')%(self.gridsize))
            self.action_griddown.setEnabled(True)
            if self.gridsize==48:
                self.action_gridup.setEnabled(False)
            
    def griddown(self):
        if self.gridsize>=14:
            self.gridsize-=2
            self.label.pixSize=self.gridsize
            self.label.resizepixmaps(self.gridsize)
            num,status=[*self.game.num],[*self.game.status]
            self.initMineArea()
            self.game.num,self.game.status=num,status
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
        thisgamedata.append(self.game.modejudge())
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
                self.savereplay()
                self.shownews(breakrecord,self.game.stylejudge())
                

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
        window=window_news.news_Dialog(mainpos,breakrecord,style)
        window.Dialog.setModal(True)
        window.Dialog.show()
        window.Dialog.exec_()

    def calwindowsize(self,row,column,size):
        height=row*size+self.heightmargin
        width=max(153,column*size+self.widthmargin)
        return [min(width,self.maxsize[0]),min(height,self.maxsize[1])]

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
        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow,_('载入局'), '', '(board file *.abf *.mbf)')
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
        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow,_('播放录像'), '', '(video file *.nvf)')
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
        self.replaygameStart()
        self.game.initreplays()
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
