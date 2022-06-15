from PyQt5 import QtCore, QtGui, QtWidgets
from math import *
import re
from constants import *

maxlength=500
maxtext=60
maxcountertext=100000


class variable(object):
    def __init__(self,name,vtype,strin):
        self.expstr=strin
        self.name=name
        self.vtype=vtype#1:内部 2:外部
        self.isvalid=True
        self.parameter_exe()

    def parameter_exe(self):
        if len(self.expstr)>=maxlength:
            self.expstr=self.expstr[:maxlength]
        self.option={'precision':-1,'max':999999999,'min':-999999999,'exception':0,'opacity':False}
        numdict={0:'precision',1:'max',2:'min',3:'exception',4:'opacity'}
        leftbraket,rightbraket=None,None
        for i in range(len(self.expstr)):
            if self.expstr[i]=='{':
                if leftbraket!=None:
                    self.isvalid=False
                    return
                leftbraket=i
            if self.expstr[i]=='}':
                if rightbraket!=None:
                    self.isvalid=False
                    return
                rightbraket=i
        if leftbraket==None and rightbraket==None:
            return
        if leftbraket==None or rightbraket==None or leftbraket>=rightbraket:
            self.isvalid=False
            return
        '''if self.vtype==2:
            self.expstr=self.expstr.lower()
            engs=re.findall('[a-z]+',self.expstr)
            for s in engs:
                if s not in['max','min']:
                    self.isvalid=False
                    return'''
        opstr=self.expstr[leftbraket+1:rightbraket]
        self.expstr=self.expstr[:leftbraket]
        if opstr=='':
            return
        parameters=opstr.split(',')
        for i in range(min(len(self.option),len(parameters))):
            if parameters[i]=='':
                continue
            try:
                if i ==0:
                    parameter=int(parameters[i])
                elif i in[1,2,3]:
                    parameter=float(parameters[i])
                elif i ==4:
                    parameter=bool(parameters[i])
            except:
                continue
            self.option[numdict[i]]=parameter

class Counter(object):

    preview = QtCore.pyqtSignal()
    def __init__(self,counterWindow,game):
        self.allvars=[]
        self.game=game
        for var in invars:
            variablein=variable(var[0],1,var[1])
            self.allvars.append(variablein)
        self.window=counterWindow
        self.window.setEnabled(True)
        self.window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.window.setWindowFlags(QtCore.Qt.Drawer)
        self.window.closeEvent2.connect(self.closecounter)
        self.window.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.window.customContextMenuRequested.connect(self.create_rightmenu) 
        self.window.setWindowTitle(_("Counter"))
        self.create_rightmenu()
        self.columnwidth=[100,140]
        self.lineheight=22
        self.getcountertext()
        self.linesnum=(len(self.texts)+1)//2
        sumheight=self.lineheight*self.linesnum
        self.window.setFixedSize(sum(self.columnwidth), sumheight+10)
        self.valuelabelarray=[0]*self.linesnum*2
        #gridlayout= QtWidgets.QGridLayout()
        #self.window.setLayout(gridlayout)
        for i in range(self.linesnum):
            for j in range(2):
                self.valuelabelarray[2*i+j]=QtWidgets.QLabel(self.window)
                self.valuelabelarray[2*i+j].resize=(self.columnwidth[j],self.lineheight)
                self.valuelabelarray[2*i+j].setText(' ')
                self.valuelabelarray[2*i+j].setAlignment(QtCore.Qt.AlignLeft)
                self.valuelabelarray[2*i+j].setStyleSheet("font-size:18px;font-family:Arial;")
                #valuelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
                #valuelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
                self.valuelabelarray[2*i+j].move(self.columnwidth[0]*j,self.lineheight*i)

    def getcountertext(self):
        try:
            #f=open("config/counter.txt",'r')
            f=open("counter.txt",'r')
            countertext=f.read()
            f.close()
        except:
            countertext=''
        if len(countertext)>maxcountertext:
            countertext=countertext[:maxcountertext]
        countertext=countertext.replace('\t','')
        countertext=countertext.replace('\n','')
        countertext=countertext.replace('\b','')
        self.texts=countertext.split(';')
        if len(self.texts)>maxtext:
            self.texts=self.texts[maxtext]
        
    def calvariable(self,var,status,rt,est,solvedbv):
        if status==1 and var.option['opacity']==True:
            return '-'
        try:
            value=eval(var.expstr)
            value=min(max(value,var.option['min']),var.option['max'])
        except:
            value=var.option['exception']
        if var.option['precision']>=0:
            try:
                precision=int(var.option['precision'])
                value=round(value,precision)
            except:
                pass
        return value

    def calexpression(self,exp,status,rt,est,solvedbv):
        option={'precision':-1,'max':999999999,'min':-999999999,'exception':0,'opacity':False}
        numdict={0:'precision',1:'max',2:'min',3:'exception',4:'opacity'}
        exp=exp[1:-1]
        exp_result=re.search('{(.*)}.*$',exp)
        if exp_result==None:
            expoptionstr=''
        else:
            expoptionstr=exp_result.group(1)
            exp=exp.replace(exp_result.group(0),'',1)
        variables=re.findall('<.*?>',exp)
        if variables!=None:
            for var1 in variables:
                
                var=var1[1:-1]
                if var=='':
                    var_value=0
                    exp=exp.replace(var1,'0',1)
                    continue
                var=var.lower()
                matched=False
                for cvar in self.allvars:
                    if var==cvar.name:
                        matched=True
                        if not cvar.isvalid:
                            exp=exp.replace(var1,'0',1)
                            break
                        else:
                            var_value=self.calvariable(cvar,status,rt,est,solvedbv)
                            if var_value=='-':
                                exp_value='-'
                                return exp_value
                            exp=exp.replace(var1,str(var_value),1)
                    if matched:
                        break
                if not matched:
                    exp=exp.replace(var1,'0',1)
        parameters=expoptionstr.split(',')
        for i in range(min(len(option),len(parameters))):
            if parameters[i]=='':
                continue
            try:
                if i ==0:
                    parameter=int(parameters[i])
                elif i in[1,2,3]:
                    parameter=float(parameters[i])
                elif i ==4:
                    parameter=bool(parameters[i])
            except:
                continue
            option[numdict[i]]=parameter
        exp=exp.lower()
        engs=re.findall('[a-z]+',exp)
        if engs!=None:
            for eng in engs:
                if eng not in ['max','min','log']:
                     exp_value=option['exception']
                     return str(exp_value)
        try:
            exp_value=eval(exp)
            exp_value=min(max(exp_value,option['min']),option['max'])
        except:
            exp_value=option['exception']
        if option['precision']>=0:
            try:
                precision=int(option['precision'])
                exp_value=round(exp_value,precision)
                exp_value=format(exp_value,'.%df'%(precision))
            except:
                pass
        return str(exp_value)
        
    def retranslate(self):
        self.window.setWindowTitle(_("Counter"))
        self.action_replay.setText(_('Preview replay'))
        self.action_sboard.setText(_('Save board'))
        self.action_sreplay.setText(_('Save replay'))

    def create_rightmenu(self):
        self.menu=QtWidgets.QMenu()
        self.action_replay=QtWidgets.QAction(self.window)
        self.menu.addAction(self.action_replay)
        self.action_sboard=QtWidgets.QAction(self.window)
        self.menu.addAction(self.action_sboard)
        self.action_sreplay=QtWidgets.QAction(self.window)
        self.menu.addAction(self.action_sreplay)     
        self.menu.popup(QtGui.QCursor.pos())
        self.action_sreplay.triggered.connect(self.game.savereplay)
        self.action_sboard.triggered.connect(self.game.saveboard)  
        self.action_replay.triggered.connect(self.window.getpreview)   
        self.retranslate()
        if self.game.finish:
            self.action_sboard.setEnabled(True)
            self.action_sreplay.setEnabled(True)
            self.action_replay.setEnabled(True)
        else:
            self.action_sboard.setEnabled(False)
            self.action_sreplay.setEnabled(False)
            self.action_replay.setEnabled(False)
    
    def refreshvalues(self,status):
        rt=max(0,min(self.game.replayboardinfo[5],round(self.game.intervaltime,2))) if self.game.isreplaying() else self.game.intervaltime
        solvedbv=self.game.solvedelse+self.game.solvedops
        try:
            est=rt/(solvedbv+2*self.game.solvedops)*(self.game.bbbv+2*self.game.ops)
        except:
            est=999.99
        for i in range(len(self.texts)):
            text=self.texts[i]
            exps=re.findall('\[.*?\]',text)
            if exps==None:
                self.valuelabelarray[i].setText(' '+text)
                continue
            else:
                for exp in exps:
                    expresult=self.calexpression(exp,status,rt,est,solvedbv)
                    text=text.replace(exp,expresult,1)
                self.valuelabelarray[i].setText(' '+text)
                continue                

    def closecounter(self):
        pass





                    
                
                
        
       
    
        
        
            
