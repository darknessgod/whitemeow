import random
import time
from queue import Queue

class gamestatus(object):
    def __init__(self,row,column,mines,options):
        self.row,self.column,self.mineNum=row,column,mines
        self.failed,self.timeStart,self.finish,self.mouseout,self.result=False,False,False,False,0
        self.redmine=[0,0]
        self.replayboardinfo=[]
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
        self.operationlist,self.tracklist,self.replay,self.pathlist=[],[],[],[]
        self.replaynodes,self.cursorplace=[0,0],[0,0]
        self.thisislandsolved,self.thisopsolved=False,False
        self.num = [0]*(self.row*self.column) # -1雷，0-8数字
        self.status = [0]*(self.row*self.column) # 0未开 1打开 2标雷
        self.num0queue=Queue()
        self.counter=None

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
        if not self.isMine(i,j):
            if self.isOpening(i,j): #左键开op递归
                for r in self.rowRange(i - 1, i + 2):
                    for c in self.columnRange(j - 1, j + 2):
                        if self.isCovered(r,c) and not self.isMine(r,c):
                            self.forceUncover(r,c)
                            self.num0queue.put([r,c,start0])
            elif self.num[self.getindex(i,j)] > 0: #双键递归，此处为假条件，将来会替换为递归开关
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
                                self.num0queue.put([r,c,start0])
                            elif self.isMine(r,c) and self.isCovered(r,c):
                                self.failed=True
                                self.redmine=[r,c]

    def doleft(self,i,j):
        self.allclicks[0]+=1
        if self.isCovered(i,j):
            self.eclicks[0]+=1
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

    def doright(self,i,j):
        self.allclicks[1]+=1
        self.rightfirst=True
        if self.isCovered(i,j):
            self.flagonmine(i,j)
        elif self.isFlag(i,j):
            self.unflagonmine(i,j)
        elif self.isOpened(i,j) and not self.isOpening(i,j):
            self.flagonnumber(i,j)

    def pressdouble(self,i,j):
        pass

    def dodouble(self,i,j):
        if self.rightfirst==True:
            self.allclicks[1]-=1
            self.rightfirst=False
        self.allclicks[2]+=1
        if self.chordingFlag(i, j):
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
                        
    def domove(self,i,j):
        if not self.outOfBorder(i, j):
            self.mouseout=False
            if (i, j) != self.oldCell and (self.leftAndRightHeld or self.leftHeld):
                self.oldCell = (i, j)
        elif self.leftAndRightHeld or self.leftHeld:#拖到界外
            self.mouseout=True

    def dofinish(self,result):
        pass
            

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

    def unflagonmine(self,i,j):
        self.eclicks[1]+=1
        self.allclicks[3]-=1
        self.rightfirst=False
        self.forceUnflag(i,j)

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
                        self.allclicks[3]+=1
                        self.rightfirst=False
                        eright=True
            if eright==True:
                self.eclicks[1]+=1
                
    def findopis_bfs(self,i,j,num):
        for ii in self.rowRange(i-1,i+2):
            for jj in self.columnRange(j-1,j+2):
                if num==1:
                    if not self.isMine(ii,jj) and self.isCovered(ii,jj):
                        self.thisopsolved=False
                    if self.isOpening(ii,jj) and self.num0seen[self.getindex(ii,jj)]==False:
                        self.num0seen[self.getindex(ii,jj)]=True
                        self.num0get+=1
                        self.num0queue.put([ii,jj])
                elif num==2:
                    if self.isbv[self.getindex(ii,jj)]==True and self.islandseen[self.getindex(ii,jj)]==False:
                        if self.isCovered(ii,jj):
                            self.thisislandsolved=False
                        self.islandseen[self.getindex(ii,jj)]=True
                        self.bvget+=1
                        self.num0queue.put([ii,jj])

    def cal_3bv(self):
        self.islands,self.solvedislands,self.ops,self.solvedops,self.solvedbbbv=0,0,0,0,0
        solvedelse,num0,numelse=0,0,0
        self.bvget,self.num0get=0,0
        self.num0seen = [0]*(self.row*self.column)
        self.islandseen = [0]*(self.row*self.column)
        self.isbv = [0]*(self.row*self.column)
        for i in range(self.row):#对0格计数
            for j in range(self.column):
                if self.isOpening(i,j):
                    num0+=1
        for i in range(self.row):
            for j in range(self.column):
                if self.num0get==num0:#所有0被染色，标志op计算完全，终止
                    break
                if self.isOpening(i,j):
                    if self.num0seen[self.getindex(i,j)]==True:
                        continue
                    else:
                        self.ops+=1#找到新的op
                        self.thisopsolved=True
                        self.num0seen[self.getindex(i,j)]=True
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
                if self.num[self.getindex(i,j)]>0:
                    nearnum0=False
                    for ii in self.rowRange(i-1,i+2):
                        for jj in self.columnRange(j-1,j+2):
                            if self.isOpening(ii,jj):
                                nearnum0=True
                                break
                    if nearnum0==False:
                        self.isbv[self.getindex(i,j)]=True
                        numelse+=1
                        if self.isOpened(i,j):
                            solvedelse+=1

        for i in range(self.row):#算islands
            for j in range(self.column):
                if self.bvget==numelse:
                    break
                if self.isbv[self.getindex(i,j)]==True:
                    if self.islandseen[self.getindex(i,j)]==True:
                        continue
                    else:
                        self.islands+=1
                        self.thisislandsolved=True
                        if self.isCovered(i,j):
                            self.thisislandsolved=False
                        self.islandseen[self.getindex(i,j)]=True
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
        playertag,playername='fairy','anonymous'
        st,et,deltat,bbbv=self.starttime,self.endtime,self.intervaltime,self.bbbv
        mode,type,level,style=self.gamemode,self.gametype,self.leveljudge(),self.stylejudge()
        kept1,kept2,kept3,kept4,kept5,kept6,version=0,0,0,0,0,0,'v1.5'
        if self.failed==True:
            result=2
            prefix='#'
            replayname='%s%s_%.2f_3bv=%d_%s.nvf'%(prefix,level,deltat,bbbv,playername)
        else:
            result=1
            prefix=''
            replayname='%s%s_%.2f_3bv=%d_3bvs=%.3f_%s.nvf'%(prefix,level,deltat,bbbv,bbbv/deltat,playername)
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
                if self.tracklist[i][0]<0 or self.tracklist[i][0]>100*self.row:
                    return 9
        except:
            return 11
        self.pathlist=[0]
        for i in range(len(self.tracklist)-1):
            self.pathlist.append(self.pathlist[-1]+((self.tracklist[i][0]-self.tracklist[i+1][0])**2+(self.tracklist[i][1]-self.tracklist[i+1][1])**2)**0.5/100)
        return 0

    def dealboard(self,boardlist):
        if len(boardlist)<4:
            return -1
        boardinfo=boardlist[0:4]
        boardarea=boardlist[4:]
        minenum=boardinfo[2]*256+boardinfo[3]
        column,row=boardinfo[0],boardinfo[1]
        if len(boardlist)!=4+2*minenum:
            return -1
        if min(column,row)<4 or max(column,row)>50 or minenum/(column*row)>0.5:
            return -2
        num = [0]*(self.row*self.column)
        for i in range(minenum):
            if boardarea[2*i+1]>=row or boardarea[2*i]>column or num[self.getindex(boardarea[2*i+1],boardarea[2*i])]==-1:
                return -3
            num[self.getindex(boardarea[2*i+1],boardarea[2*i])]=-1
        self.row,self.column,self.mineNum=row,column,minenum
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
                return tempturple
            self.replaynodes[0]+=1

    def getindex(self,i,j):
        return i*self.column+j


