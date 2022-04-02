import random
import time
from queue import Queue
from readdata import *

class gamestatus(object):
    def __init__(self,row,column,mines,settings):
        self.settings=settings
        self.row,self.column,self.mineNum=row,column,mines
        self.failed,self.timeStart,self.finish,self.mouseout,self.result=False,False,False,False,0
        self.redmine,self.oldCell=(0,0),(0,0)
        self.replayboardinfo=[]
        self.tmplist=[i for i in range(self.column*self.row-1)]
        self.gamemode,self.gametype=self.modejudge(),1
        self.leftHeld,self.rightHeld,self.leftAndRightHeld,self.rightfirst=False,False,False,False
        self.path,self.gamenum,self.ranks=0,0,[0,0,0]
        self.starttime,self.intervaltime,self.endtime,self.oldinttime=0,0,0,0
        self.num0seen,self.islandseen,self.isbv=[],[],[]
        self.num0get,self.bvget=0,0
        self.ops,self.solvedops,self.bbbv,self.solvedbbbv,self.solvedelse,self.islands,self.solvedislands=0,0,0,0,0,0,0
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0]
        self.operationlist,self.tracklist,self.replay,self.pathlist=[],[],[],[]
        self.replayoplist,self.replayislist=[],[]
        self.replaynodes,self.cursorplace=[0,0],[0,0]
        self.thisop,self.thisis=[],[]
        self.num = [0]*(self.row*self.column) # -1雷，0-8数字
        self.status = [0]*(self.row*self.column) # 0未开 1打开 2标雷
        self.pixmapindex = [9]*(self.row*self.column)
        self.num0queue=Queue()
        self.counter=None

    def recursive(self):
        return bool(self.gamemode&1)
    def canflagnumber(self):
        return bool(self.gamemode&1)
    def isreplaying(self):
        return self.gametype==4
    def isCovered(self,i,j):
        return self.status[self.getindex(i,j)]==0
    def isOpened(self,i,j):
        return self.status[self.getindex(i,j)]==1
    def isFlag(self,i,j):
        return self.status[self.getindex(i,j)]==2
    def isMine(self,i,j):
        return self.num[self.getindex(i,j)]==-1
    def isOpening(self,i,j):
        return self.num[self.getindex(i,j)]==0
    def forceUncover(self,i,j):
        self.status[self.getindex(i,j)]=1
    def safeUncover(self,i,j):
        if self.isCovered(i,j):
            self.forceUncover(i,j)
    def forceFlag(self,i,j):
        self.status[self.getindex(i,j)]=2
    def forceUnflag(self,i,j):
        self.status[self.getindex(i,j)]=0

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
    def forceUncover(self,index):
        self.status[index]=1
    def safeUncover(self,index):
        if self.isCovered(index):
            self.forceUncover(index)
    def forceFlag(self,index):
        self.status[index]=2
    def forceUnflag(self,index):
        self.status[index]=0

    def rowRange(self,top,bottom):
        return range(max(0,top),min(self.row,bottom))
    def columnRange(self,left,right):
        return range(max(0,left),min(self.column,right))

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
                self.num[self.getindex(r,c)]=-1
                self.calnumbers(r,c)


    def renewminearea(self):
        self.status=[0]*(self.row*self.column)
        self.pixmapindex=[9]*(self.row*self.column)
        if self.gametype not in [2,4]:
            self.num=[0]*(self.row*self.column)
                        
    def renewstatus(self):
        self.timeStart = False
        self.finish=False
        self.result=0
        self.solvedbbbv,self.solvedops,self.path=0,0,0
        self.intervaltime,self.oldinttime =0,0
        self.allclicks,self.eclicks=[0,0,0,0],[0,0,0]
        self.leftAndRightHeld,self.leftHeld,self.rightfirst,self.rightHeld=False,False,False,False
        if not self.isreplaying():
            self.operationlist,self.tracklist=[],[],
            self.bbbv,self.ops=0,0

    def BFS(self, i, j ,start0):
        if self.isCovered(i,j):
            self.forceUncover(i,j)
            index=self.getindex(i,j)
            self.pixmapindex[index]=self.num[index]
            if self.isreplaying():
                if self.gridquality[index]<0:
                    self.solvedelse+=1
                if self.gridquality[index] not in self.tocheck:
                    self.tocheck.append(self.gridquality[index])
        if not self.isMine(i,j):
            if self.isOpening(i,j): #左键开op递归
                for r in self.rowRange(i - 1, i + 2):
                    for c in self.columnRange(j - 1, j + 2):
                        if self.isCovered(r,c) and not self.isMine(r,c):
                            self.forceUncover(r,c)
                            index=self.getindex(r,c)
                            self.pixmapindex[index]=self.num[index]
                            if self.isreplaying():
                                if self.gridquality[index]<0:
                                    self.solvedelse+=1
                                if self.gridquality[index] not in self.tocheck:
                                    self.tocheck.append(self.gridquality[index])
                            self.num0queue.put([r,c,start0])
            elif self.recursive(): 
                flagged=0
                for r in self.rowRange(i - 1, i + 2):
                    for c in self.columnRange(j - 1, j + 2):
                        if self.isFlag(r,c):
                            flagged+=1
                if flagged==self.num[self.getindex(i,j)]:
                    for r in self.rowRange(i - 1, i + 2):
                        for c in self.columnRange(j - 1, j + 2):
                            if self.isCovered(r,c) and not self.isMine(r,c):
                                self.forceUncover(r,c)
                                index=self.getindex(r,c)
                                self.pixmapindex[index]=self.num[index]
                                if self.isreplaying():
                                    if self.gridquality[index]<0:
                                        self.solvedelse+=1
                                    if self.gridquality[index] not in self.tocheck:
                                        self.tocheck.append(self.gridquality[index])
                                self.num0queue.put([r,c,start0])
                            elif self.isMine(r,c) and self.isCovered(r,c):
                                self.failed=True
                                self.redmine=[r,c]

    def doleft(self,i,j):
        self.allclicks[0]+=1
        if self.isCovered(i,j):
            self.eclicks[0]+=1
            self.tocheck=[]
            if not self.isMine(i,j):
                self.num0queue=Queue()
                self.num0queue.put([i,j,self.isOpening(i,j)])
                while(self.num0queue.empty()==False):
                    getqueuehead=self.num0queue.get()
                    self.BFS(getqueuehead[0], getqueuehead[1],getqueuehead[2])
            else:
                if not self.timeStart and self.gametype==1 :#第一下不能为雷
                    self.exchange1tolast(i,j)
                    self.num0queue=Queue()
                    self.num0queue.put([i,j,self.isOpening(i,j)])
                    while(self.num0queue.empty()==False):
                        getqueuehead=self.num0queue.get()
                        self.BFS(getqueuehead[0],getqueuehead[1],getqueuehead[2])        
                else:
                    self.failed=True
                    self.redmine=[i,j]
            if self.isreplaying():
                if len(self.tocheck)!=0:
                    for s in self.tocheck:
                        if s>0:
                            self.issolved(1,s-1)
                        elif s<0:
                            self.issolved(2,-s-1)
                    self.solvedops=self.calsolved(1)
                    self.solvedislands=self.calsolved(2)

    def doright(self,i,j):
        self.allclicks[1]+=1
        self.rightfirst=True
        if self.isCovered(i,j):
            self.flagonmine(i,j)
        elif self.isFlag(i,j):
            self.unflagonmine(i,j)
        elif self.isOpened(i,j) and not self.isOpening(i,j) and self.canflagnumber():
            self.flagonnumber(i,j)

    def pressdouble(self,i,j):
        pass

    def dodouble(self,i,j):
        if self.rightfirst==True:
            self.allclicks[1]-=1
            self.rightfirst=False
        self.allclicks[2]+=1
        if self.chordingFlag(i, j):
            self.tocheck=[]
            edouble=False
            for r in self.rowRange(i - 1, i + 2):
                for c in self.columnRange(j - 1, j + 2):
                    if self.isCovered(r,c):
                        edouble=True
                        if not self.isMine(r,c):
                            self.num0queue=Queue()
                            self.num0queue.put([r,c,self.isOpening(r,c)])
                            while(self.num0queue.empty()==False):
                                getqueuehead=self.num0queue.get()
                                self.BFS(getqueuehead[0], getqueuehead[1],getqueuehead[2])
                        else:
                            self.failed=True
                            self.redmine=[r,c]
            if edouble==True:
                self.eclicks[2]+=1
                if self.isreplaying():
                    if len(self.tocheck)!=0:
                        for s in self.tocheck:
                            if s>0:
                                self.issolved(1,s-1)
                            elif s<0:
                                self.issolved(2,-s-1)
                        self.solvedops=self.calsolved(1)
                        self.solvedislands=self.calsolved(2)

                        
    def domove(self,i,j):
        if not self.outOfBorder(i, j):
            self.mouseout=False
            if (i, j) != self.oldCell and (self.leftAndRightHeld or self.leftHeld):
                self.oldCell = (i, j)
        elif self.leftAndRightHeld or self.leftHeld:#拖到界外
            self.mouseout=True

    def dofinish(self):
        for i in range(self.row):
            for j in range(self.column):
                self.finishpaint(i,j)
            

    def exchange1tolast(self,i,j):
        self.num[self.getindex(i,j)]=0
        self.num[self.getindex(self.row-1,self.column-1)]=-1
        for ii in self.rowRange(i - 1, i + 2):
            for jj in self.columnRange(j - 1, j + 2):
                if not self.isMine(ii,jj):     
                    count=0
                    for rr in self.rowRange(ii - 1, ii + 2):
                        for cc in self.columnRange(jj - 1, jj + 2):
                            if self.isMine(rr,cc):
                                count+=1
                    self.num[self.getindex(ii,jj)]=count
        for ii in range(self.row-2, self.row):
            for jj in range(self.column-2, self.column):
                if not self.isMine(ii,jj):     
                    count=0
                    for rr in self.rowRange(ii - 1, ii + 2):
                        for cc in self.columnRange(jj - 1, jj + 2):
                            if self.isMine(rr,cc):
                                count+=1
                    self.num[self.getindex(ii,jj)]=count

    def chordingFlag(self, i, j):
        # i, j 周围标雷数是否满足双击的要求
        if not self.isMine(i,j) and self.isOpened(i,j):
            count = 0
            for r in self.rowRange(i - 1, i + 2):
                for c in self.columnRange(j - 1, j + 2):
                    if self.isFlag(r,c):
                        count += 1
            if count == 0 and not self.isOpening(i,j):
                return False
            else:
                return count == self.num[self.getindex(i,j)]
        else:
            return False

    def flagonmine(self,i,j):
        self.eclicks[1]+=1
        self.allclicks[3]+=1
        self.rightfirst=False
        self.forceFlag(i,j)
        self.pixmapindex[self.getindex(i,j)]=10

    def unflagonmine(self,i,j):
        self.eclicks[1]+=1
        self.allclicks[3]-=1
        self.rightfirst=False
        self.forceUnflag(i,j)
        self.pixmapindex[self.getindex(i,j)]=9

    def flagonnumber(self,i,j):
        count=0
        for r in self.rowRange(i - 1, i + 2):
            for c in self.columnRange(j - 1, j + 2):
                if self.isCovered(r,c) or self.isFlag(r,c):
                    count += 1
        if count== self.num[self.getindex(i,j)]:
            eright=False
            for r in self.rowRange(i - 1, i + 2):
                for c in self.columnRange(j - 1, j + 2):
                    if self.isCovered(r,c):
                        self.forceFlag(r,c)
                        self.pixmapindex[self.getindex(r,c)]=10
                        self.allclicks[3]+=1
                        self.rightfirst=False
                        eright=True
            if eright==True:
                self.eclicks[1]+=1
                
    def findopis_bfs(self,i,j,num):
        index=self.getindex(i,j)
        if num==1:#op模式    
            if self.isOpening(i,j):
                self.num0get+=1
                for ii in self.rowRange(i-1,i+2):
                    for jj in self.columnRange(j-1,j+2):
                        index=self.getindex(ii,jj)
                        if self.gridquality[index]!=self.ops and not self.isMine(ii,jj):
                            self.gridquality[index]=self.ops
                            self.thisop.append(index)
                            self.num0queue.put([ii,jj])
        elif num==2:
            if not self.isMine(i,j):
                for ii in self.rowRange(i-1,i+2):
                    for jj in self.columnRange(j-1,j+2):
                        index=self.getindex(ii,jj)
                        if self.gridquality[index]==0 and not self.isMine(ii,jj):
                            self.bvget+=1
                            self.gridquality[index]=-self.islands
                            self.thisis.append(index)
                            self.num0queue.put([ii,jj])
                    

    def cal_3bv(self):
        self.islands,self.solvedislands,self.ops,self.solvedops,self.solvedbbbv,self.solvedelse=0,0,0,0,0,0
        self.bvget,self.num0get,num0=0,0,0
        self.replayoplist,self.replayislist=[],[]
        self.gridquality = [0]*(self.row*self.column)#格子性质，0为雷或未标记，正数A为第A个op,负数-B为第B个is
        for i in range(self.row):#对0格计数
            for j in range(self.column):
                if self.isOpening(i,j):
                    num0+=1
        for i in range(self.row):
            for j in range(self.column):
                index=self.getindex(i,j)
                if self.num0get==num0:#所有0被标记，标志op计算完全，终止
                    break
                if self.isOpening(i,j):
                    if self.gridquality[index]==0:
                        self.ops+=1#找到新的op
                        self.thisop=[0]
                        self.num0queue=Queue()
                        self.num0queue.put([i,j])
                        while(self.num0queue.empty()==False):
                            getqueuehead=self.num0queue.get()
                            self.findopis_bfs(getqueuehead[0], getqueuehead[1],1)
                        self.replayoplist.append(self.thisop)
        #此时所有的op及op边缘都被标记，剩下的数字一定是bv
        for i in range(self.row):
            for j in range(self.column):
                index=self.getindex(i,j)
                if not self.isMine(i,j) and  self.gridquality[index]==0:
                    self.islands+=1
                    self.thisis=[0]
                    self.num0queue=Queue()
                    self.num0queue.put([i,j])
                    while(self.num0queue.empty()==False):
                        getqueuehead=self.num0queue.get()
                        self.findopis_bfs(getqueuehead[0], getqueuehead[1],2)
                    self.replayislist.append(self.thisis)
        self.bbbv=self.bvget+self.ops

    def issolved(self,num,index):
        if num==1:
            for i in range(1,len(self.replayoplist[index])):
                if self.status[self.replayoplist[index][i]]!=1:
                    self.replayoplist[index][0]=0
                    return
            self.replayoplist[index][0]=1
        elif num==2:
            for i in range(1,len(self.replayislist[index])):
                if self.status[self.replayislist[index][i]]!=1:
                    self.replayislist[index][0]=0
                    return
            self.replayislist[index][0]=1

    def calsolved(self,num):
        if num==1:
            count=0
            for i in range(len(self.replayoplist)):
                if self.replayoplist[i][0]==1:
                    count+=1
        elif num==2:
            count=0
            for i in range(len(self.replayislist)):
                if self.replayislist[i][0]==1:
                    count+=1
        elif num==3:
            count=0
            for i in range(len(self.replayislist)):
                if self.replayislist[i][0]==1:
                    count+=len(self.replayislist[i])-1
                else:
                    for j in range(1,len(self.replayislist[i])):
                        if self.status[self.replayislist[i][j]]==1:
                            count+=1
        return count


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

    def calnumbers(self,r,c):
        for i in self.rowRange(r - 1, r + 2):
            for j in self.columnRange(c - 1, c + 2):
                if not self.isMine(i,j):
                    self.num[self.getindex(i,j)] += 1

    def addoperation(self,num,i,j):
        if self.timeStart==False:
            optime=-1
        else:
            optime=int(1000*(time.time()-self.starttime))
        self.operationlist.append((num,i,j,optime))

    def addtrack(self,yy,xx):
        if self.timeStart==True:
            optime=int(1000*(time.time()-self.starttime))
            self.tracklist.append((yy,xx,optime))

    def getboardlist(self):
        boardlist=[self.column,self.row,self.mineNum//256,self.mineNum%256]
        for i in range(self.row):
            for j in range(self.column):
                if self.isMine(i,j):
                    boardlist+=[j,i]
        return boardlist

    def getboardinfo(self):
        playertag,playername=self.settings['defaultplayertag'],self.settings['playername']
        st,et,deltat,bbbv=self.starttime,self.endtime,self.intervaltime,self.bbbv
        mode,type,level,style=self.gamemode,self.gametype,self.leveljudge(),self.stylejudge()
        kept1,kept2,kept3,kept4,kept5,kept6,version=0,0,0,0,0,0,'v1.5'
        leveldict={'BEG':self.settings['level1name'],'INT':self.settings['level2name'],'EXP':self.settings['level3name'],'CUS':self.settings['level4name']}
        levelname=leveldict[level[:3]]
        if self.failed==True:
            result=2
            prefix='#'
            replayname='%s%s_%.2f_3bv=%d_%s.nvf'%(prefix,levelname,deltat,bbbv,playername)
        else:
            result=1
            prefix=''
            replayname='%s%s_%.2f_3bv=%d_3bvs=%.3f_%s.nvf'%(prefix,levelname,deltat,bbbv,bbbv/deltat,playername)
        boardinfo=[replayname,playertag,playername,st,et,deltat,bbbv]
        boardinfo+=[mode,type,level,style,result,kept1,kept2,kept3,kept4,kept5,kept6,version]
        return boardinfo

    def dealreplay(self):
        l1,l2,l3,l4=self.replay[0],self.replay[1],self.replay[2],self.replay[3]
        if len(self.replay)!=4+l1+l2+l3+l4:
            return 1
        self.replayboardinfo=[*self.replay[4:4+l1]]
        if self.replayboardinfo[8] not in[1,2] or self.replayboardinfo[11] not in [1,2]:
            return 2
        boardlist=[*self.replay[4+l1:4+l1+l2]]
        boardlegal=self.dealboard(boardlist)
        if boardlegal!=0:
            return boardlegal
        self.operationlist=[*self.replay[4+l1+l2:4+l1+l2+l3]]
        try:
            for i in range(len(self.operationlist)):
                if self.operationlist[i][0] not in [1,2,3,4,5,6]:
                    return 3
                if i!=len(self.operationlist)-1:
                    if self.operationlist[i][3]>self.operationlist[i+1][3]:
                        return 4
                if self.operationlist[i][1]<0 or self.operationlist[i][1]>100*(self.row-1):
                    return 5
                if self.operationlist[i][2]<0 or self.operationlist[i][2]>100*(self.column-1):
                    return 6
        except:
            return 7
        self.tracklist=[*self.replay[4+l1+l2+l3:]]
        try:
            for i in range(len(self.tracklist)):
                if i!=len(self.tracklist)-1:
                    if self.tracklist[i][2]>self.tracklist[i+1][2]:
                        return 8
        except:
            return 11
        self.pathlist=[0]
        for i in range(len(self.tracklist)-1):
            self.pathlist.append(self.pathlist[-1]+((self.tracklist[i][0]-self.tracklist[i+1][0])**2+(self.tracklist[i][1]-self.tracklist[i+1][1])**2)**0.5/100)
        return 0

    def initreplays(self):
        self.gamemode=self.replayboardinfo[7]

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
        if min(column,row)<4 or max(column,row)>50 or minenum/(column*row)>0.5:
            return -2
        num = [0]*(self.row*self.column)
        self.num=[*num]
        for i in range(minenum):
            if boardarea[2*i+1]>=row or boardarea[2*i]>column or num[self.getindex(boardarea[2*i+1],boardarea[2*i])]==-1:
                return -3
            num[self.getindex(boardarea[2*i+1],boardarea[2*i])]=-1
        self.num=[*num]
        for i in range(minenum):
            self.calnumbers(boardarea[2*i+1],boardarea[2*i])
        return 0

    def dopreoperations(self):
        flags=[]
        for i in range(0,len(self.operationlist)):
            if self.operationlist[i][3]!=-1:
                break
            if self.operationlist[i][0]==3:
                self.allclicks[1]+=1
                self.eclicks[1]+=1
                tempturple=(self.operationlist[i][1],self.operationlist[i][2])
                if tempturple in flags:
                    flags.remove(tempturple)
                else:
                    flags.append(tempturple)
            elif self.operationlist[i][0]==6:
                self.allclicks[2]+=1
            elif self.operationlist[i][0]==2: 
                tempturple=(self.operationlist[i][1],self.operationlist[i][2])
                for s in flags:
                    self.forceFlag(s[0],s[1])
                    self.pixmapindex[self.getindex(s[0],s[1])]=10
                return tempturple
            self.replaynodes[0]+=1

    def getindex(self,i,j):
        return i*self.column+j

    def modejudge(self):
        mode=0
        if self.settings['enablerec']==True:
            mode+=1
        self.gamemode=mode
        return self.gamemode

    def finishpaint(self,i,j):
        index=self.getindex(i,j)
        if self.result==2:
            if i==self.redmine[0] and j==self.redmine[1]:
                self.pixmapindex[index]=13
            elif self.isMine(i,j) and not self.isFlag(i,j):
                self.pixmapindex[index]=11
            elif self.isFlag(i,j) and not self.isMine(i,j):
                self.pixmapindex[index]=12
        elif self.result==1:
            if self.isMine(i,j) and not self.isFlag(i,j):
                self.pixmapindex[index]=14
