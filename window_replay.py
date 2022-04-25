from PyQt5 import QtCore, QtGui, QtWidgets
import time



class ui_replaydialog (object):

    
    
    def __init__(self,geo,window,game):
        self.game=game
        self.geo=geo
        self.Dialog = window
        self.label,self.timer=None,None
        self.dontpaint=False
        self.game.tocheck=set()
        self.acctime,self.starttime,self.xspeed,self.pasttime,self.lastms=0,0,1,0,-2
        self.endtime=self.game.replayboardinfo[5]
        self.setupui()
        self.continuebutton.clicked.connect (self.continuereplay)
        self.pausebutton.clicked.connect (self.pausereplay)   
        self.speeds=[]
        for i in range(25):
            self.speeds.append(0.05*i+0.1)
        self.speeds+=[1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.2,2.5,3,4,5]
        self.paused,self.calculating=False,False

    def retranslate(self):
        self.Dialog.setWindowTitle(_("replay control bar"))

    def setupui(self):
        self.Dialog.setWindowIcon(QtGui.QIcon("media/mine.ico"))
        self.retranslate()
        self.Dialog.move(self.geo[0],self.geo[1]-68)
        self.Dialog.setFixedSize(520,32)
        self.Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Dialog.setWindowFlags(QtCore.Qt.Tool)
        self.frame = QtWidgets.QFrame(self.Dialog)
        self.frame.setFixedSize(520,32)
        self.frame.move(0,0)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.continuebutton=QtWidgets.QPushButton (self.frame)
        self.continuebutton.setFixedSize(32,32)
        self.continuebutton.setStyleSheet("QPushButton{border-image: url(media/continue.png)}")
        self.horizontalLayout.addWidget(self.continuebutton)
        self.pausebutton=QtWidgets.QPushButton (self.frame)
        self.pausebutton.setFixedSize(32,32)
        self.pausebutton.setStyleSheet("QPushButton{border-image: url(media/pause.png)}")
        self.horizontalLayout.addWidget(self.pausebutton)
        self.adjustspeed=QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.adjustspeed.setParent(self.frame)
        self.adjustspeed.setMinimum(0)
        self.adjustspeed.setMaximum(37)
        self.adjustspeed.setSingleStep(1)
        self.adjustspeed.setValue(18)
        self.adjustspeed.valueChanged.connect(self.speedchange)
        self.adjustspeed.setStyleSheet("QSlider::groove {\n"
        "    border: 0px solid #bbbbbb;\n"
        "    background-color: #ffffff;\n"
        "    border-radius: 4px;\n"
        "}\n"
        "QSlider::groove:horizontal {\n"
        "    height: 6px;\n"
        "}\n"
        "QSlider::handle:horizontal {\n"
        "    background: #bbbbbb;\n"
        "    border-style: solid;\n"
        "    border-width: 1px;\n"
        "    border-color: rgb(207,207,207);\n"
        "    width: 5px;\n"
        "    margin: -5px 0;\n"
        "    border-radius: 2px;\n"
        "}")
        self.adjustspeed.setFixedWidth(72)
        self.horizontalLayout.addWidget(self.adjustspeed)
        self.speedtext=QtWidgets.QLabel(self.frame)
        self.speedtext.setFixedSize(48,32)
        self.speedtext.setText('%.2fx'%(self.xspeed))
        self.horizontalLayout.addWidget(self.speedtext)
        self.replayprogress=QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.replayprogress.setParent(self.Dialog)
        self.replayprogress.setMinimum(0)
        self.replayprogress.setMaximum(150)
        self.replayprogress.setSingleStep(1)
        self.replayprogress.setValue(0)
        #self.replayprogress.setEnabled(False)
        self.replayprogress.setStyleSheet("QSlider::groove {\n"
        "    border: 0px solid #bbbbbb;\n"
        "    background-color: #ffffff;\n"
        "    border-radius: 4px;\n"
        "}\n"
        "QSlider::groove:horizontal {\n"
        "    height: 6px;\n"
        "}\n"
        "QSlider::handle:horizontal {\n"
        "    background: #bbbbbb;\n"
        "    border-style: solid;\n"
        "    border-width: 1px;\n"
        "    border-color: rgb(207,207,207);\n"
        "    width: 5px;\n"
        "    margin: -5px 0;\n"
        "    border-radius: 2px;\n"
        "}")
        self.replayprogress.setFixedWidth(151)
        self.replayprogress.setPageStep(0)
        self.replayprogress.valueChanged.connect(self.progresschange)
        self.replayprogress.sliderPressed.connect(self.pausereplay)
        self.horizontalLayout.addWidget(self.replayprogress)
        self.timetext=QtWidgets.QLabel(self.frame)
        self.timetext.setFixedSize(120,32)
        self.timetext.setText('%.2f/%.2f'%(min(max(0,self.acctime-0.005),self.endtime),self.endtime))
        self.horizontalLayout.addWidget(self.timetext)        
        self.horizontalLayout.addStretch(1)
        self.horizontalLayout.setSpacing(2)
        
    def continuereplay(self):
        self.paused=False
        self.starttime=time.time()

    def progresschange(self):
        self.switchtostatus(int(1000*self.replayprogress.value()*self.endtime/self.replayprogress.maximum()))
           

    def pausereplay(self):
        if self.paused:
            return
        self.paused=True
        nt=time.time()
        self.acctime=(nt-self.starttime)*self.xspeed+self.pasttime
        self.pasttime=self.acctime
        self.starttime=nt
        oldvalue=self.replayprogress.value()
        newvalue=min(self.replayprogress.maximum(),self.acctime*self.replayprogress.maximum()//self.endtime)
        if newvalue!=oldvalue:
            self.replayprogress.setValue(newvalue)
        else:
            self.switchtostatus(int(self.acctime*1000))    

    def speedchange(self):
        self.xspeed=self.speeds[self.adjustspeed.value()]
        self.speedtext.setText('%.2fx'%(self.xspeed))

    def switchtostatus(self,pastms):#将局面的全部状态切换至pastms毫秒处
        if pastms>=self.endtime*1000:
            pastms+=10
        replaying=False
        if not self.paused:
            replaying=True
        if self.lastms>pastms:
            self.game.replaynodes=[0,0,0,0]
            self.switchback_init()
        self.switchforward_state(pastms)
        self.switchforward_cursor(pastms)
        self.switchforward_clicks(pastms)
        self.switchforward_mousestatus(pastms)
        if self.finishedreplay() and not self.dontpaint:
            pastms-=10
            self.showtime=self.endtime
            self.game.redmine=self.game.replayboardinfo[12]
            self.game.result=self.game.replayboardinfo[11]
            for i in range(self.game.row*self.game.column):
                self.game.finishpaint(i)
        self.game.intervaltime=min(self.endtime,pastms/1000)
        self.timetext.setText('%.2f/%.2f'%(min(self.endtime,pastms/1000),self.endtime))
        if not self.dontpaint:
            self.label.update()
        self.lastms=pastms
        if not replaying:
            self.pasttime=self.replayprogress.value()*self.endtime/self.replayprogress.maximum()

    def switchforward_state(self,pastms):
        while(True):
            index=self.game.replaynodes[0]
            if index==len(self.game.statelist):
                break
            i=self.game.statelist[index]
            if i[2]<=pastms:
                self.game.status[i[0]]=i[1]
                if i[1]==2:
                    self.game.allclicks[3]+=1
                elif i[1]==0:
                    self.game.allclicks[3]-=1
                else:
                    gq=self.game.gridquality[i[0]]
                    if not self.game.isMine(i[0]):
                        if gq>0:
                            self.game.replayoplist[gq-1].discard(i[0])
                            self.game.tocheck.add(gq)
                        elif gq<0:
                            self.game.replayislist[-gq-1].discard(i[0])
                            self.game.solvedelse+=1
                            self.game.tocheck.add(gq)
                        else:
                            for k in self.game.adjacent1(i[0]):
                                if self.game.isOpening(k):
                                    self.game.replayoplist[self.game.gridquality[k]-1].discard(i[0])
                tmpturple=(9,self.game.num[i[0]],10)
                self.game.pixmapindex[i[0]]=tmpturple[i[1]]
            else:
                break
            self.game.replaynodes[0]+=1
        self.game.checkSolved()

    def switchforward_cursor(self,pastms):
        left,right=self.game.replaynodes[1],len(self.game.tracklist)-1
        mid=(left+right)//2
        while(1):
            if right-left<=1:
                index=mid
                break
            if self.game.tracklist[mid][2]<=pastms and self.game.tracklist[mid+1][2]>pastms:
                index=mid
                break
            if self.game.tracklist[mid][2]>pastms:
                right=mid
                mid=(left+right)//2
            elif self.game.tracklist[mid+1][2]<=pastms:
                left=mid
                mid=(left+right)//2
        self.game.cursorplace=[self.game.tracklist[index][0],self.game.tracklist[index][1]]
        self.game.oldCell=self.game.getindex(self.game.tracklist[index][0],self.game.tracklist[index][1])
        self.game.replaynodes[1]=index
        self.game.path=self.game.pathlist[index]

    def switchforward_clicks(self,pastms):
        clicksdict={'l':(0,1),'r':(1,1),'d':(2,1),'R':(1,-1)}
        eclicksdict={'le':(0,1),'re':(1,1),'de':(2,1)}
        while(True):
            index=self.game.replaynodes[2]
            if index==len(self.game.clicklist):
                break
            i=self.game.clicklist[index]            
            if i[1]<=pastms:
                if len(i[0])==1:
                    calresult=clicksdict[i[0]]
                    self.game.allclicks[calresult[0]]+=calresult[1]
                elif len(i[0])==2:
                    calresult=eclicksdict[i[0]]
                    self.game.eclicks[calresult[0]]+=calresult[1]
            else:
                break
            self.game.replaynodes[2]+=1

    def switchforward_mousestatus(self,pastms):
        while(True):
            index=self.game.replaynodes[3]
            if index==len(self.game.mousestatelist):
                break
            i=self.game.mousestatelist[index]   
            if i[1]>pastms:
                break
            if i[0]=='lh':
                self.game.leftHeld=True
            elif i[0]=='lr':
                self.game.leftHeld=False
            if i[0]=='dh':
                self.game.leftAndRightHeld=True
            elif i[0]=='dr':
                self.game.leftAndRightHeld=False    
            self.game.replaynodes[3]+=1    

    def switchback_init(self):
        for i in range(self.game.row*self.game.column):
            self.game.status[i]=0
            self.game.pixmapindex[i]=9
            gq=self.game.gridquality[i]
            if not self.game.isMine(i):
                if gq>0:
                    self.game.replayoplist[gq-1].add(i)
                elif gq<0:
                    self.game.replayislist[-gq-1].add(i)
                else:
                    for k in self.game.adjacent1(i):
                        if self.game.isOpening(k):
                            self.game.replayoplist[self.game.gridquality[k]-1].add(i)
        self.game.leftHeld,self.game.rightHeld,self.game.leftAndRightHeld=False,False,False
        self.game.allclicks,self.game.eclicks=[0,0,0,0],[0,0,0]
        self.game.solvedelse,self.game.solvedops,self.game.solvedislands=0,0,0

    def endreplay(self):
        return self.replayprogress.value()==self.replayprogress.maximum()

    def finishedreplay(self):
        return self.game.replaynodes[0]>=len(self.game.statelist)