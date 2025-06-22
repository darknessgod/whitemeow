import random
import time
import pickle
from queue import Queue
from readdata import *
from constants import adjacent
import ms_toollib as ms
import encoder

class gamestatus(object):
    def __init__(self,row,column,mines,settings):
        self.settings=settings
        self.row,self.column,self.mineNum=row,column,mines # height=row, width=column, mines=mineNum
        self.failed,self.timeStart,self.finish,self.mouseout,self.result=False,False,False,False,0 # some flags for events
        self.redmine=0 # blast
        self.oldCell=0
        self.startcross=None
        self.replayboardinfo=[]
        self.tmplist=[i for i in range(self.column*self.row-1)]
        self.gamemode,self.gametype=self.modejudge(),1
        self.leftHeld,self.rightHeld,self.leftAndRightHeld,self.rightfirst,self.midHeld=False,False,False,False,False # mouse status
        self.path,self.gamenum,self.ranks=0,0,[0,0,0]
        self.starttime,self.intervaltime,self.endtime,self.oldinttime=0,0,0,0
        self.num0seen,self.islandseen,self.isbv=[],[],[]
        self.num0get,self.bvget=0,0
        self.ops,self.solvedops,self.bbbv,self.solvedbbbv,self.solvedelse,self.islands,self.solvedislands=0,0,0,0,0,0,0 # (solved) openings, (solved) bbbv, (solved) islands. solvedelse = solvedbbbv-solvedops
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0] # clicks and efficient clicks
        self.operationlist,self.tracklist,self.statelist,self.replay,self.pathlist=[],[],[],[],[]
        self.clicklist,self.mousestatelist=[],[]
        self.replayoplist,self.replayislist=[],[] # contain indices of cells in each opening/island
        self.replaynodes,self.cursorplace=[0,0,0,0],[0,0]
        self.thisop,self.thisis=[],[]
        self.num = [0]*(self.row*self.column) # mine=-1, -2, ..., numbers=0,1,2,3,4,5,6,7,8
        self.status = [0]*(self.row*self.column) # covered=0, opened=1, flagged=2
        self.pixmapindex = [9]*(self.row*self.column)
        self.counter=None
        self.tocheck=set() # openings and islands to update

    def recursive(self): # recursive chord
        return bool(self.gamemode&1)
    def isnggame(self):
        return bool(self.gamemode&2)
    def canflagnumber(self): # fast flag
        return bool(self.gamemode&1)
    def isreplaying(self):
        return self.gametype==4

    # index conversion
    def getindex(self,i,j):
        return i*self.column+j
    def getrow(self,index):
        return index//self.column
    def getcolumn(self,index):
        return index % self.column
    
    # check cell status
    def isCovered(self,index):
        return self.status[index]==0
    def isOpened(self,index):
        return self.status[index]==1
    def isFlag(self,index):
        return self.status[index]==2
    def isMine(self,index):
        return self.num[index]==-1
    def isOpening(self,index):
        return self.num[index]==0
    def isGameFinished(self):
        for i in range(self.row*self.column):
            if not self.isOpened(i) and not self.isMine(i):
                return False
        return True        
    # cell operations
    def forceUncover(self,index):
        #print("uncovering ", index)
        self.status[index]=1
        self.pixmapindex[index]=self.num[index]

    def safeUncover(self,index):
        if self.isCovered(index):
            self.forceUncover(index)
    def forceFlag(self,index,optime):
        self.status[index]=2
        self.addstate(index,2,optime)
    def forceUnflag(self,index,optime):
        self.status[index]=0
        self.addstate(index,0,optime)

    # in-border ranges
    def rowRange(self,top,bottom):
        return range(max(0,top),min(self.row,bottom))
    def columnRange(self,left,right):
        return range(max(0,left),min(self.column,right))

    # adjacent cells
    def adjacent3(self,i,j,index):
        return adjacent(i,j,index,self.row,self.column)
    def adjacent2(self,i,j):
        return self.adjacent3(i,j,self.getindex(i,j))
    def adjacent1(self,index):
        return self.adjacent3(self.getrow(index),self.getcolumn(index),index)
        
    # border check
    def outOfBorder(self, i, j):
        return i < 0 or i >= self.row or j < 0 or j >= self.column


    def createMine(self,gtype):    
        num = self.mineNum
        if len(self.tmplist)!=self.column*self.row-1:
            self.tmplist=[i for i in range(self.column*self.row-1)]
        if gtype==1:
            if self.settings['noguess']:
                startrow,startcolumn=int(self.row*random.random()),int(self.column*random.random())
                result=ms.laymine_solvable_thread(self.row,self.column,self.mineNum,startrow,startcolumn,100000)
                index=0
                for i in range(self.row):
                    for j in range(self.column):
                        self.num[index]=result[0][i][j]
                        index+=1
                if result[1]:
                    self.gamemode+=2
                    self.startcross=(startcolumn,startrow)
            else:
                random.shuffle(self.tmplist)
                for i in range(num):
                    r= int(self.tmplist[i]/self.column)
                    c= self.tmplist[i]-r*self.column
                    self.num[self.getindex(r,c)]=-1
                    self.calnumbers(self.getindex(r,c))

    def renewminearea(self):
        self.status=[0]*(self.row*self.column)
        self.pixmapindex=[9]*(self.row*self.column)
        if self.gametype not in [2,4]:
            self.num=[0]*(self.row*self.column)
                        
    def renewstatus(self):
        self.timeStart = False
        self.finish=False
        self.result=0
        self.startcross=None
        self.solvedbbbv,self.solvedops,self.path=0,0,0
        self.intervaltime,self.oldinttime =0,0
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0]
        self.leftAndRightHeld,self.leftHeld,self.rightfirst,self.rightHeld,self.midHeld=False,False,False,False,False
        self.gamemode=self.modejudge()
        if not self.isreplaying():
            self.operationlist,self.tracklist,self.statelist,self.clicklist,self.mousestatelist=[],[],[],[],[]
            self.bbbv,self.ops=0,0

    def recursiveChord(self,index,optime):
        q=Queue()
        q.put(index)
        while not q.empty():
            next=q.get()
            if self.chordingFlag(next) or self.isOpening(next):
                for i in self.adjacent1(next):
                    if not self.isCovered(i):
                        continue
                    elif self.isMine(i):
                        self.failed=True
                        self.redmine=i
                    else:
                        self.forceUncover(i)
                        self.addstate(i,1,optime)
                        q.put(i)

    def getOpening(self,index,optime):
        q=Queue()
        q.put(index)
        while not q.empty():
            next=q.get()
            if self.isOpening(next):
                for i in self.adjacent1(next):
                    if not self.isCovered(i):
                        continue
                    elif self.isMine(i):
                        self.failed=True
                        self.redmine=i
                    else:
                        self.forceUncover(i)
                        self.addstate(i,1,optime)
                        q.put(i)

    def doleft(self,index,optime):
        self.allclicks[0]+=1
        self.clicklist.append(('l',optime))
        if self.isCovered(index):
            self.eclicks[0]+=1
            self.clicklist.append(('le',optime))
            self.tocheck=set()
            if not self.isMine(index):
                self.forceUncover(index)
                self.addstate(index,1,optime)
                if self.recursive():
                    self.recursiveChord(index,optime)
                elif self.isOpening(index):
                    self.getOpening(index,optime)
            else:
                if not self.timeStart and self.gametype==1 and not self.isnggame():#第一下不能为雷
                    self.exchange1tolast(index)
                    self.doleft(index,optime)    
                else:
                    self.addstate(index,1,optime)
                    self.failed=True
                    self.redmine=index

    def doright(self,index,optime):
        self.allclicks[1]+=1
        self.clicklist.append(('r',optime))
        self.rightfirst=True
        if self.isCovered(index):
            self.flagonmine(index,optime)
        elif self.isFlag(index):
            self.unflagonmine(index,optime)
        elif self.isOpened(index) and not self.isOpening(index) and self.canflagnumber():
            self.flagonnumber(index,optime)

    def pressdouble(self,index):
        pass

    def dodouble(self,index,optime,mid=False):
        if not mid and self.rightfirst==True:
            self.allclicks[1]-=1
            self.clicklist.append(('R',optime))
            self.rightfirst=False
        self.allclicks[2]+=1
        self.clicklist.append(('d',optime))
        if self.chordingFlag(index):
            self.tocheck=set()
            self.eclicks[2]+=1
            self.clicklist.append(('de',optime))
            if self.recursive():
                self.recursiveChord(index,optime)
            else:
                for i in self.adjacent1(index):
                    if self.isCovered(i):
                        if self.isMine(i):
                            self.addstate(i,1,optime)
                            self.failed=True
                            self.redmine=i
                        elif self.isOpening(i):
                            self.forceUncover(i)
                            self.addstate(i,1,optime)
                            self.getOpening(i,optime)
                        else:
                            self.forceUncover(i)
                            self.addstate(i,1,optime)
                        
    def domove(self,i,j):
        pass

    def dofinish(self):
        self.leftAndRightHeld,self.leftHeld,self.rightHeld,self.rightfirst,self.midHeld=False,False,False,False,False
        for i in range(self.row*self.column):
            self.finishpaint(i)

    def exchange1tolast(self,index):
        if self.isMine(index):
            self.num[index]=0
            for i in self.adjacent1(index):
                if self.isMine(i):
                    self.num[index]+=1
                else:
                    self.num[i]-=1
            self.num[-1]=-1
            for i in self.adjacent2(self.row-1,self.column-1):
                if not self.isMine(i):
                    self.num[i]+=1

    def chordingFlag(self, index):
        # i, j 周围标雷数是否满足双击的要求
        covered=False
        count=0
        if not self.isMine(index) and self.isOpened(index):
            count = 0
            for r in self.adjacent1(index):
                if self.isFlag(r):
                    count += 1
                elif self.isCovered(r):
                    covered=True
        else:
            return False
        return covered and count == self.num[index]

    def flagonmine(self,index,optime):
        self.eclicks[1]+=1
        self.clicklist.append(('re',optime))
        self.allclicks[3]+=1
        self.rightfirst=False
        self.forceFlag(index,optime)
        self.pixmapindex[index]=10

    def unflagonmine(self,index,optime):
        self.eclicks[1]+=1
        self.clicklist.append(('re',optime))
        self.allclicks[3]-=1
        self.rightfirst=False
        self.forceUnflag(index,optime)
        self.pixmapindex[index]=9

    def flagonnumber(self,index,optime):
        count=0
        for r in self.adjacent1(index):
            if self.isCovered(r) or self.isFlag(r):
                count += 1
        if count== self.num[index]:
            eright=False
            for r in self.adjacent1(index):
                if self.isCovered(r):
                    self.forceFlag(r,optime)
                    self.pixmapindex[r]=10
                    self.allclicks[3]+=1
                    self.rightfirst=False
                    eright=True
            if eright==True:
                self.eclicks[1]+=1
                self.clicklist.append(('re',optime))

    def cal_3bv(self):
        self.islands,self.solvedislands,self.ops,self.solvedops,self.solvedbbbv,self.solvedelse=0,0,0,0,0,0
        self.bvget,self.num0get=0,0
        self.bbbv=self.row*self.column-self.mineNum
        #print("bbbv="+str(self.bbbv))
        self.replayoplist,self.replayislist=[],[]
        m=32767
        self.gridquality = [m]*(self.row*self.column)#格子性质，m为雷，0为op边缘，正数A为第A个op内部,负数-B为第B个is
        for i in range(self.row*self.column): # 找op
            if self.isOpening(i) and self.gridquality[i]==m:
                self.ops+=1
                self.gridquality[i]=self.ops
                #print("op="+str(self.ops)+", starting from ("+str(self.getrow(i))+","+str(self.getcolumn(i))+")")
                q=Queue()
                q.put(i)
                thisop=set()
                thisop.add(i)
                while not q.empty():
                    index=q.get()
                    for next in self.adjacent1(index):
                        thisop.add(next)
                        if self.gridquality[next]==m:
                            self.bbbv-=1
                            #print("subtract bv at ("+str(self.getrow(next))+","+str(self.getcolumn(next))+")")
                            if self.isOpening(next):
                                self.gridquality[next]=self.ops
                                q.put(next)
                            else:
                                self.gridquality[next]=0
                self.replayoplist.append(thisop)
                #print("index = ",self.ops, "content = ", thisop)
        for i in range(self.row*self.column):
            if self.gridquality[i]==m and not self.isMine(i):
                self.islands+=1
                self.gridquality[i]=-self.islands
                q=Queue()
                q.put(i)
                thisis=set()
                thisis.add(i)
                while not q.empty():
                    index=q.get()
                    for next in self.adjacent1(index):
                        if self.gridquality[next]==m and not self.isMine(next):
                            thisis.add(next)
                            self.gridquality[next]=-self.islands
                            q.put(next)
                self.replayislist.append(thisis)
                #print("index = ",-self.islands, "content = ", thisis)
        return

    def cal_3bv_solved(self):
        self.cal_3bv()
        self.tocheck=set()
        if self.isreplaying():
            for index in range(self.row*self.column):
                if self.isOpened(index):
                    self.tocheck.add(self.gridquality[index])
        else:
            for index in range(self.row*self.column):
                if self.isOpened(index):
                    self.tocheck.add(self.gridquality[index])
                    if self.gridquality[index]<0:
                        self.solvedelse+=1
        self.checkSolved()

    def checkSolved(self):
        if self.isreplaying():
            for index in self.tocheck:
                if index>0:
                    #print("index = ",index, ", cells left = ", len(self.replayoplist[index-1]))
                    if len(self.replayoplist[index-1])==0:
                        self.solvedops+=1 
                elif index<0:
                    #print("index = ",index, ", cells left = ", len(self.replayislist[-index-1]))
                    if len(self.replayislist[-index-1])==0:
                        self.solvedislands+=1
            self.tocheck.clear()
        else:
            for index in self.tocheck:
                solved=True
                if index>0:
                    for s in self.replayoplist[index-1]:
                        if not self.isOpened(s):
                            solved=False
                    if solved==True:
                        self.solvedops+=1
                elif index<0:
                    for s in self.replayislist[-index-1]:
                        if not self.isOpened(s):
                            solved=False
                    if solved==True:
                        self.solvedislands+=1
        

    def issolved(self,index):
        if index>0:
            if len(self.replayoplist[index-1])==0:
                return True
            return False
        elif index<0:
            if len(self.replayislist[-index-1])==0:
                return True
            return False

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

    def calnumbers(self,index):
        for i in self.adjacent1(index):
            if not self.isMine(i):
                self.num[i] += 1

    def addstate(self,index,state,optime):
        self.statelist.append((index,state,optime))

    def addtrack(self,yy,xx):
        if self.timeStart==True:
            optime=int(1000*(time.time()-self.starttime))
            self.tracklist.append((yy,xx,optime))

    def getboardlist(self):
        boardlist=[self.column,self.row,self.mineNum//256,self.mineNum%256]
        for i in range(self.row):
            for j in range(self.column):
                if self.isMine(self.getindex(i,j)):
                    boardlist+=[j,i]
        return boardlist

    def getboardinfo(self):
        playertag,playername=self.settings['defaultplayertag'],self.settings['playername']
        st,et,deltat,bbbv=self.starttime,self.endtime,self.intervaltime,self.bbbv
        mode,type,level,style=self.gamemode,self.gametype,self.leveljudge(),self.stylejudge()
        redmine,kept1,kept2,kept3,kept4,kept5,version=self.redmine,0,0,0,0,0,'v1.5'
        leveldict={'BEG':self.settings['level1name'],'INT':self.settings['level2name'],'EXP':self.settings['level3name'],'CUS':self.settings['level4name']}
        levelname=leveldict[level[:3]]
        if self.isreplaying():
            deltat=self.replayboardinfo[5]
            type=self.replayboardinfo[8]
        if self.failed==True:
            result=2
            prefix='#'
            replayname='%s%s_%.2f_3bv=%d_%s.nvf'%(prefix,levelname,deltat,bbbv,playername)
        else:
            result=1
            prefix=''
            replayname='%s%s_%.2f_3bv=%d_3bvs=%.3f_%s.nvf'%(prefix,levelname,deltat,bbbv,bbbv/deltat,playername)
        boardinfo=[replayname,playertag,playername,st,et,deltat,bbbv]
        boardinfo+=[mode,type,level,style,result,redmine,kept1,kept2,kept3,kept4,kept5,version]
        return boardinfo

    def dealreplay(self):
        try:
            l1,l2,l3,l4,l5,l6=self.replay[0],self.replay[1],self.replay[2],self.replay[3],self.replay[4],self.replay[5]
            if len(self.replay)!=6+l1+l2+l3+l4+l5+l6:
                return 1
            self.replayboardinfo=[*self.replay[6:6+l1]]
            if self.replayboardinfo[8] not in[1,2] or self.replayboardinfo[11] not in [1,2]:
                print(self.replayboardinfo)
                return 2
            boardlist=[*self.replay[6+l1:6+l1+l2]]
            boardlegal=self.dealboard(boardlist)
            if boardlegal!=0:
                return boardlegal
        except:
            return 3
        try:
            self.tracklist=[*self.replay[6+l1+l2:6+l1+l2+l3]]
            for i in range(len(self.tracklist)):
                if i!=len(self.tracklist)-1:
                    if self.tracklist[i][2]>self.tracklist[i+1][2]:
                        return 9
        except:
            return 10
        try:
            self.statelist=[*self.replay[6+l1+l2+l3:6+l1+l2+l3+l4]]
            for i in range(len(self.statelist)):
                if self.statelist[i][0]<0 or self.statelist[i][0]>(self.row*self.column):
                    return 11
                if self.statelist[i][1] not in [0,1,2]:
                    return 12
                if i!=len(self.statelist)-1:
                    if self.statelist[i][2]>self.statelist[i+1][2]:
                        return 13
        except:
            return 14
        try:
            self.clicklist=[*self.replay[6+l1+l2+l3+l4:6+l1+l2+l3+l4+l5]]
            for i in range(len(self.clicklist)):
                if self.clicklist[i][0] not in ('l','r','d','le','re','de','R'):
                    return 15
                if i!=len(self.clicklist)-1:
                    if self.clicklist[i][1]>self.clicklist[i+1][1]:
                        return 16
        except:
            return 17
        try:
            self.mousestatelist=[*self.replay[6+l1+l2+l3+l4+l5:]]
            for i in range(len(self.mousestatelist)):
                if self.mousestatelist[i][0] not in ('lh','rh','dh','mh','lr','rr','dr','mr'):
                    return 18
                if i!=len(self.mousestatelist)-1:
                    if self.mousestatelist[i][1]>self.mousestatelist[i+1][1]:
                        return 19            
        except:
            return 20
        self.calpath()
        return 0

    def calpath(self):
        self.pathlist=[0]
        for i in range(len(self.tracklist)-1):
            self.pathlist.append(self.pathlist[-1]+((self.tracklist[i][0]-self.tracklist[i+1][0])**2+(self.tracklist[i][1]-self.tracklist[i+1][1])**2)**0.5/100)
       

    def initreplays(self):
        self.gamemode=self.replayboardinfo[7]
        self.redmine=self.replayboardinfo[12]

    def dealboard(self,boardlist):
        if len(boardlist)<4:
            return -1
        boardinfo=boardlist[0:4]
        boardarea=boardlist[4:]
        minenum=boardinfo[2]*256+boardinfo[3]
        column,row=boardinfo[0],boardinfo[1]
        self.row,self.column,self.mineNum=row,column,minenum
        if len(boardlist)!=4+2*minenum:
            return -1
        if min(column,row)<4 or max(column,row)>80 or minenum/(column*row)>0.5:
            return -2
        num = [0]*(self.row*self.column)
        self.num=[*num]
        for i in range(minenum):
            if boardarea[2*i+1]>=row or boardarea[2*i]>column or num[self.getindex(boardarea[2*i+1],boardarea[2*i])]==-1:
                return -3
            num[self.getindex(boardarea[2*i+1],boardarea[2*i])]=-1
        self.num=[*num]
        for i in range(minenum):
            self.calnumbers(self.getindex(boardarea[2*i+1],boardarea[2*i]))
        return 0

    def modejudge(self):
        mode=0
        if self.settings['enablerec']:
            mode+=1
        self.gamemode=mode
        return self.gamemode

    def finishpaint(self,index):
        if self.result==2:
            if index==self.redmine:
                self.pixmapindex[index]=13
            elif self.isMine(index) and not self.isFlag(index):
                self.pixmapindex[index]=11
            elif self.isFlag(index) and not self.isMine(index):
                self.pixmapindex[index]=12
        elif self.result==1:
            if self.settings['endflagall']:
                if self.isMine(index) and not self.isFlag(index):
                    self.pixmapindex[index]=14
                    
    def saveboard(self):
        if self.finish==False:
            return
        boardlist=self.getboardlist()
        abf=bytes(boardlist)
        ft=list(time.localtime(time.time()))
        filename='%dx%d_%dmines_%d_%d_%d_%d_%d_%d.abf'%(self.column,self.row,
        self.mineNum,ft[0],ft[1],ft[2],ft[3],ft[4],ft[5])
        with open(r"%s"%(filename),'wb') as f:
            f.write(abf)

    def savereplay(self):
        if self.finish==False:
            return
        boardlist=self.getboardlist()
        boardinfo=self.getboardinfo()
        replay=[len(boardinfo),len(boardlist),len(self.tracklist),len(self.statelist),len(self.clicklist),len(self.mousestatelist)]
        replay+=boardinfo
        replay+=boardlist
        replay+=self.tracklist
        replay+=self.statelist
        replay+=self.clicklist
        replay+=self.mousestatelist
        self.makereplayfile(replay)

    def makereplayfile(self,replay):
        filename=replay[6]
        file=open('%s'%(filename),'wb')
        pickle.dump(replay,file)
        file.close()
        #encoder.encode(file)

    def makereplayfile2(self,replay):
        filename=replay[6]
        input=pickle.dumps(replay)
        encoder.encode(replay)