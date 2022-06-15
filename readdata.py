import pickle
import copy
from constants import *

class readdata(object):

    def __init__(self):
        self.dict1={'Flag':0,'NF':3}
        self.dict2={'BEG':0,'INT':1,'EXP':2}
        self.stats=[]
        self.titledict={'Day':0,'Month':1,'Year':2,'Hour':3,'Min':4,'Sec':5,'Rtime':6,'3bv':7,'Mode':8,'Level':9,'Style':10,'Lcl':11,'Rcl':12,'Dcl':13,'Leff':14,'Reff':15,'Deff':16,'Ops':17,'Isls':18,'Path':19}
        self.length=len(self.titledict)
        self.records=[]
        initrecord=[999.99,0,999.999,999.999,0]
        for i in range(6):
            tmp=[*initrecord]
            self.records.append(tmp)
        self.numrt=self.titledict['Rtime']
        self.numbbbv=self.titledict['3bv']
        #nummode=self.titledict['Mode']
        self.numlevel=self.titledict['Level']
        self.numstyle=self.titledict['Style']
        self.numlcl=self.titledict['Lcl']
        self.numrcl=self.titledict['Rcl']
        self.numdcl=self.titledict['Dcl']

    def readstats(self):
        try:
            file=open('stats.dat','rb')
            self.stats=pickle.load(file)
        except FileNotFoundError:
            self.stats=[]

    def writestats(self):
        file=open('stats.dat','wb')
        pickle.dump(self.stats,file)
        file.close()

    def addtostats(self,inputlist):
        if len(inputlist)==self.length:
            self.stats.append(inputlist)

    def clearstats(self):
        self.stats=[]

    def getrecords(self):
        for s in self.stats:
            tmp=self.judgerecord(s)

    def judgerecord(self,s):
        breakrecord=[0,0,0,0,0]
        if s[self.numlevel] in['BEG','INT','EXP']:
            recordindex=self.dict1[s[self.numstyle]]+self.dict2[s[self.numlevel]]
            if s[self.numrt]<self.records[recordindex][0]:
                self.records[recordindex][0]=s[self.numrt]
                breakrecord[0]=1
            bvs=s[self.numbbbv]/s[self.numrt]
            if bvs>self.records[recordindex][1]:
                self.records[recordindex][1]=bvs
                breakrecord[1]=1
            qg=s[self.numrt]**1.7/s[self.numbbbv]
            if qg<self.records[recordindex][2]:
                self.records[recordindex][2]=qg
                breakrecord[2]=1
            rqp=(1+s[self.numrt])/bvs
            if rqp<self.records[recordindex][3]:
                self.records[recordindex][3]=rqp
                breakrecord[3]=1
            ioe=s[self.numbbbv]/(s[self.numlcl]+s[self.numrcl]+s[self.numdcl])
            if ioe>self.records[recordindex][4]:
                self.records[recordindex][4]=ioe
                breakrecord[4]=1
        return breakrecord

    def picklereplay(self,file):
        replay=pickle.load(file)
        return replay
        
class readsettings(object):

    def __init__(self):
        self.settings={}

    def readsettings(self):
        try:
            file=open('settings.dat','rb')
            self.settings=pickle.load(file)
        except FileNotFoundError:
            self.settings=copy.deepcopy(defaultsettings)
            self.writesettings()
        if len(self.settings)!=len(defaultsettings):
            self.settings=copy.deepcopy(defaultsettings)
            self.writesettings()
            

    def writesettings(self):
        file=open('settings.dat','wb')
        if self.settings!={}:
            pickle.dump(self.settings,file)
        else:
            pickle.dump(defaultsettings,file)
        file.close()
