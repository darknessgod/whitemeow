from tkinter import VERTICAL
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QPalette, QPixmap, QFont, QIcon ,QPainter
from PyQt5.QtWidgets import QLineEdit, QInputDialog
from gamestatus import gamestatus
import mainWindowGUI,superGUI, mineLabel,window_custom,window_settings,gamestatus,window_news,window_record,window_replay
import time,struct
from window_counter import Counter
from constants import *

class MineSweeperGUI(superGUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        
        self.getdata()
        self.mainWindow = MainWindow        
        self.mainWindow.setWindowIcon(QIcon("media/mine.ico"))
        self.mainWindow.setFixedSize(self.mainWindow.minimumSize())
        self.mainWindow.move(694,200)
        self.maxsize=[1000,800]
        self.widthmargin,self.heightmargin=28,141
        self.initlanguage()
        self.setupUi(self.mainWindow)
        if self.options.settings['defaultlevel']=='beg':
            self.game=gamestatus.gamestatus(8,8,10,self.options.settings)
        elif self.options.settings['defaultlevel']=='exp':
            self.game=gamestatus.gamestatus(16,30,99,self.options.settings)
        else:
            self.game=gamestatus.gamestatus(16,16,40,self.options.settings)
        self.game.gamenum=self.gamescount()
        self.gridsize=32
        self.game.oldCell = 0  # 鼠标的上个停留位置，用于绘制按下去时的阴影
        self.counterWindow,self.counterui,self.replaywindow,self.replayui=None,None,None,None
        self.label=None
        self.needtorefresh=True
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
        if self.game.isreplaying():
            print(1)
            self.replaywindow.setVisible(True)
        self.mainWindow.activateWindow()

    def hidecounter(self):
        self.counterWindow.setVisible(False)

    def showcounter(self):
        self.counterWindow = mainWindowGUI.meowcounter ()
        self.counterui = Counter(self.counterWindow,self.game)
        self.counterWindow.show()
        if self.game.finish==True:
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
        self.label.setMinimumSize(QtCore.QSize(self.gridsize*self.game.column, self.gridsize*self.game.row))
        self.label.leftPressed.connect(self.mineAreaLeftPressed)
        self.label.leftRelease.connect(self.mineAreaLeftRelease)
        self.label.leftAndRightPressed.connect(self.mineAreaLeftAndRightPressed)
        self.label.leftAndRightRelease.connect(self.mineAreaLeftAndRightRelease)
        self.label.rightPressed.connect(self.mineAreaRightPressed)
        self.label.rightRelease.connect(self.mineAreaRightRelease)
        self.label.setObjectName("label")
        self.label.resize(QtCore.QSize(self.gridsize*self.game.column, self.gridsize*self.game.row))
        self.label.setContentsMargins(0,0,0,0)
        self.scroll_area = QtWidgets.QScrollArea(self.mainWindow)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedWidth(min(self.maxsize[0]-self.widthmargin+2,self.game.column*self.gridsize+2))
        self.scroll_area.setFixedHeight(min(self.maxsize[1]-self.heightmargin+2,self.game.row*self.gridsize+2))
        self.scroll_area.wheelEvent=self.wheelscroll
        #self.scrollbar = QtWidgets.QScrollBar(Qt.Horizontal)
        #self.scrollbar2 = QtWidgets.QScrollBar(Qt.Vertical)
        #self.scrollbar.setMaximum(self.scroll_area.horizontalScrollBar().maximum())
        #self.scrollbar2.setMaximum(self.scroll_area.verticalScrollBar().maximum())
        self.gridLayout.addWidget(self.scroll_area,0,0,1,1)
        #self.gridLayout.addWidget(self.scrollbar,1,0,1,1)
        #self.gridLayout.addWidget(self.scrollbar2,0,1,1,1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.label.mouseMove.connect(self.mineMouseMove)
        
    def showface(self,scale):
        facenum=[0,0]#第一位：颜色 0黄1蓝 #第二位：状态 0正常1输2赢
        if self.game.gametype==4:
            if self.game.replayboardinfo[8]==2:
                facenum[0]=1
            elif self.game.isnggame():
                facenum[0]=2
            else:
                facenum[0]=0
        elif self.game.gametype==2:
            facenum[0]=1
        elif self.game.isnggame():
            facenum[0]=2
        else:
            facenum[0]=0
        if not self.game.finish:
            if self.game.gametype==4:
                if self.game.intervaltime==0:
                    facenum[1]=0
                elif not self.replayui.finishedreplay():
                    facenum[1]=0
                elif self.game.replayboardinfo[11]==2:
                    facenum[1]=1
                elif self.game.replayboardinfo[11]==1:
                    facenum[1]=2
        elif self.game.result==2:
            facenum[1]=1
        elif self.game.result==1:
            facenum[1]=2
        facepixmaps=["smileface","lostface","winface"]
        facecolors=["","blue","green"]
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
        self.action_saveboard.triggered.connect(self.game.saveboard)
        self.action_savereplay.triggered.connect(self.game.savereplay)
        self.action_loadboard.triggered.connect(self.loadboard)
        self.action_loadreplay.triggered.connect(self.loadreplay)
        self.action_record.triggered.connect(self.action_showrecord)
        self.action_X_2.triggered.connect(QCoreApplication.instance().quit)
        self.action_counter.triggered.connect(self.showcounter)
        self.action_settings.triggered.connect(self.action_setevent)
        self.action_gridup.triggered.connect(self.gridup)
        self.action_griddown.triggered.connect(self.griddown)
        self.mainWindow.closeEvent_.connect(self.mainwindowclose)
        self.mainWindow.closeEvent2_.connect(self.hidecounter)
        self.mainWindow.gridupdownEvent.connect(self.wheelupdown)
        self.mainWindow.keypressEvent.connect(self.keypress)
        self.mainWindow.keyreleaseEvent.connect(self.keyrelease)
        self.mainWindow.minbackEvent.connect(self.counterback)
        self.counterWindow.preview.connect(self.previewreplay)
        self.action_gridsize.setText(_('current size:%d')%(self.gridsize))
        self.actionChecked(self.options.settings['defaultlevel'])  # 默认选择中级

    def mainwindowclose(self):
        if self.counterui!=None:
            self.counterWindow.close()
        if self.replayui!=None:
            self.replaywindow.close()

    def timeCount(self):
        if self.game.isreplaying():
            if not self.replayui.paused:
                nt=time.time()
                self.replayui.acctime=min(self.replayui.endtime,self.replayui.pasttime+self.replayui.xspeed*(nt-self.replayui.starttime))
                self.replayui.pasttime=self.replayui.acctime
                self.replayui.starttime=nt
                oldvalue=self.replayui.replayprogress.value()
                newvalue=min(self.replayui.replayprogress.maximum(),self.replayui.acctime*self.replayui.replayprogress.maximum()//self.replayui.endtime)
                if newvalue!=oldvalue:
                    self.replayui.replayprogress.setValue(newvalue)
                    self.game.intervaltime=min(self.replayui.endtime,self.replayui.acctime)
                else:
                    self.replayui.switchtostatus(int(self.replayui.acctime*1000))
            self.showtimenum(self.replayui.pasttime)
            self.changecounter(2)
            self.showface(8.5)
            if self.options.settings['showsafesquares']:
                self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
            else:
                self.showminenum(self.game.mineNum-self.game.allclicks[3])
        else:
            self.oldinttime=int(self.game.intervaltime+0.9999)
            self.game.intervaltime=time.time()-self.game.starttime
            inttime=int(self.game.intervaltime+0.9999)
            if inttime!=self.game.oldinttime and self.options.settings['timeringame']:
                self.showtimenum(self.game.intervaltime)
            self.changecounter(1)


    def resettimer(self):
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeCount)
        self.game.timeStart = False

    def mineAreaLeftPressed(self, i, j):
        if not self.game.finish or self.game.isreplaying():
            optime=self.getoptime()
            self.game.leftHeld = True
            self.game.mousestatelist.append(('lh',optime))
            self.game.oldCell = self.game.getindex(i, j)
            self.label.update()
            if self.options.settings['instantclick']:
                self.mineAreaLeftRelease(i,j)

    def mineAreaLeftRelease(self, i, j):
        if self.game.leftHeld and not self.game.finish:
            optime=self.getoptime()
            self.game.leftHeld = False  # 防止双击中的左键弹起被误认为真正的左键弹起
            if not self.game.isreplaying():
                self.game.mousestatelist.append(('lr',optime))
            if not self.game.outOfBorder(i, j) and not self.game.finish:
                self.game.failed=False
                self.game.doleft(self.game.getindex(i, j),optime)
                self.changecounter(1)
                if not self.game.timeStart:
                    self.game.timeStart = True
                    self.timer.start()
                    self.setshortcuts(False)
                    self.game.starttime=time.time()
                self.label.update()
                if self.game.failed==True:
                    self.gameFailed(optime)
                else:
                    if self.options.settings['showsafesquares']:
                        self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
                    if self.game.isGameFinished()==True:
                        self.gameWin(optime)

    def mineAreaRightPressed(self, i, j):
        if not self.game.finish and not self.game.settings['disableright']:
            optime=self.getoptime()
            self.game.mousestatelist.append(('rh',optime))
            self.game.doright(self.game.getindex(i, j),optime)
            self.label.update()
            if not self.options.settings['showsafesquares']:
                self.showminenum(self.game.mineNum-self.game.allclicks[3])
            self.changecounter(1)
            if self.options.settings['instantclick']:
                self.mineAreaRightRelease(i,j)
            
    def mineAreaRightRelease(self, i, j):
        if not self.game.finish and not self.game.settings['disableright']:
            optime=self.getoptime()
            self.game.mousestatelist.append(('rr',optime))

    def mineAreaLeftAndRightPressed(self, i, j):
        if not self.game.finish:
            optime=self.getoptime()
            self.game.leftAndRightHeld = True
            self.game.mousestatelist.append(('dh',optime))
            self.game.oldCell = self.game.getindex(i, j)
            self.game.pressdouble(self.game.getindex(i, j))
            self.label.update()
            if self.options.settings['instantclick']:
                self.mineAreaLeftAndRightRelease(i,j)

    def mineAreaLeftAndRightRelease(self, i, j):
        if not self.game.finish:
            self.game.leftAndRightHeld = False
            optime=self.getoptime()
            self.game.leftHeld = False
            self.game.mousestatelist.append(('dr',optime))
            self.game.mousestatelist.append(('lr',optime))
            if not self.game.outOfBorder(i, j):
                self.game.failed=False
                self.game.dodouble(self.game.getindex(i, j),optime)
                self.changecounter(1)
                self.label.update()
                if self.game.failed==True:
                    self.gameFailed(optime)
                else:
                    if self.options.settings['showsafesquares']:
                        self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
                    if self.game.isGameFinished()==True:
                        self.gameWin(optime)
                
                    
    def mineMouseMove(self, i, j):
        if not self.game.finish:
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
            for i in range(self.gridLayout.count()-2):
                w = self.gridLayout.itemAt(i).widget()
                w.setParent(None)
        self.game.settings=self.options.settings
        self.game.finish = False
        self.timer.stop()
        if self.needtorefresh==True:
            self.initMineArea()
        self.game.renewminearea()
        self.label.update()
        self.label.lastcell=None
        self.game.renewstatus()
        self.game.createMine(self.game.gametype)
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
        if self.replayui!=None:
            self.replaywindow.close()
        if self.needtorefresh==True:
            windowsize=self.calwindowsize(self.game.row,self.game.column,self.gridsize)
            self.mainWindow.setFixedSize(windowsize[0],windowsize[1])
            self.mainWindow.resize(self.mainWindow.minimumSize())
        self.needtorefresh=False

    def changecounter(self,status):
        if status==1 and self.game.finish==True:
            return
        else:
            self.counterui.refreshvalues(status)
        
        
    def gameFinished(self,result,optime):
        self.game.endtime=time.time()
        self.timer.stop()
        if self.game.finish==True:
            return
        self.game.intervaltime=max(float('%.2f'%(optime/1000-0.005)),0.01)
        self.game.cal_3bv_solved()
        if result==1:
            if self.game.gametype==1:
                self.game.gamenum+=1
                score=[self.game.intervaltime,self.game.bbbv/self.game.intervaltime,(self.game.intervaltime**1.7)/self.game.bbbv]
                self.game.ranks=self.gamerank(score)
        self.changecounter(2)
        self.showtimenum(self.game.intervaltime)
        self.game.dofinish()
        self.label.update()
        self.game.finish=True
        self.showface(8.5)
        if result==1 and self.game.gametype==1:
            self.savethisgame()   
        self.setshortcuts(True)
        if self.game.failed and self.options.settings['failrestart']:
            p=(self.game.solvedelse+self.game.solvedops)*100/self.game.bbbv
            if p<self.options.settings['failrestart_percentage']:
                self.newgameStart()



    def gameWin(self,optime):
        self.game.result=1        
        self.gameFinished(self.game.result,optime)
        

    def gameFailed(self,optime):
        self.game.result=2
        self.gameFinished(self.game.result,optime)
        

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
        if self.game.finish==False:
            self.newgameStart()
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
        elif keynum==3:
            constant=3
            self.options.settings['language']=constant-self.options.settings['language']
            self.resetlanguage()

    def initlanguage(self):
        if self.options.settings['language']==1:
            Chinese.install()
        elif self.options.settings['language']==2:
            English.install()

    def resetlanguage(self):
        self.initlanguage()
        self.retranslateUi(self.mainWindow)
        self.resetplayertag()
        self.counterui.retranslate()
        if self.replayui!=None:
            self.replayui.retranslate()
        
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
            self.action_gridsize.setText(_('current size:%d')%(self.gridsize))
            self.action_griddown.setEnabled(True)
            if self.gridsize==48:
                self.action_gridup.setEnabled(False)
            if self.game.isreplaying():
                self.replayui.label=self.label
            
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
            self.action_gridsize.setText(_('current size:%d')%(self.gridsize))
            self.action_gridup.setEnabled(True)
            if self.gridsize==12:
                self.action_griddown.setEnabled(False)
            if self.game.isreplaying():
                self.replayui.label=self.label
            
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
                self.game.savereplay()
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

    def previewreplay(self):
        self.game.replayboardinfo=self.game.getboardinfo()
        self.game.calpath()
        self.playnvf()

    def loadboard(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow,_('load board'), '', '(board file *.abf *.mbf)')
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

    def loadreplay(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow,_('play video'), '', '(video file *.nvf)')
        if fname[0]:
            f = open(fname[0], 'rb')
            replay=self.datas.picklereplay(f)
            f.close()
            self.game.replay=[*replay]
            del replay
            status=self.game.dealreplay()
            if status==0:
                self.playnvf()
            else:
                print(status)
                self.newgameStart()

    def playnvf(self):
        if self.replayui!=None:
            self.replayui.dontpaint=True
        self.timer.stop()
        self.setshortcuts(False)
        self.needtorefresh=True
        self.replaygameStart()
        self.game.initreplays()
        self.game.cal_3bv()
        if len(self.game.tracklist)==0:
            self.game.tracklist.append((0,0,-1))
        self.game.replaynodes=[0,0,0,0]
        mainpos=[self.mainWindow.x(),self.mainWindow.y(),self.mainWindow.width(),self.mainWindow.height()]

        if  True:
            #self.replayui!=None and self.replaywindow.isVisible():
            #self.replaywindow.setVisible(True)
            #self.replayui.acctime,self.replayui.pasttime,self.replayui.starttime,self.replayui.paused=0,0,0,False
            #self.replayui.endtime=self.game.replayboardinfo[5]
            #self.replayui.lastms=-2
            #self.replayui.timetext.setText('%.2f/%.2f'%(0.00,self.replayui.endtime))
            self.replaywindow= QtWidgets.QMainWindow()
            self.replayui=window_replay.ui_replaydialog(mainpos,self.replaywindow,self.game)
        self.game.replaynodes=[0,0,0,0]
        self.replayui.starttime=time.time()
        self.replayui.Dialog.show()
        self.replayui.timer,self.replayui.label=self.timer,self.label
        self.replayui.replayprogress.setEnabled(True)
        self.replayui.dontpaint=False
        self.replayui.replayprogress.setValue(0)

        self.replayui.switchtostatus(0)
        
        if self.game.replaynodes[0]==self.game.statelist:
            for i in range(self.game.row*self.game.column):
                self.game.finishpaint(i)
            self.game.intervaltime=0.01
            self.replayui.timetext.setText('0.01/0.01')
            self.showface(8.5)
            self.changecounter(2)
            self.showtimenum(1)
            self.game.cursorplace=[100*self.game.tracklist[-1][0],100*self.game.tracklist[-1][1]]
            if self.options.settings['showsafesquares']:
                self.showminenum(min(999,self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)))
            else:
                self.showminenum(self.game.allclicks[3])
            self.label.update()
            self.replayui.replayprogress.setValue(self.replayui.replayprogress.maximum())
            self.replayui.replayprogress.setEnabled(False)
        else:
            self.timer.start()
    
    def getoptime(self):
        if self.game.timeStart==False:
            optime=-1
        else:
            optime=int(1000*(time.time()-self.game.starttime))
        return optime
