TEXTURE_PATH = "MS-Texture/svg/"
CELL_PATH = TEXTURE_PATH + "cells/"
FACE_PATH = TEXTURE_PATH + "faces/"
ELEMENT_PATH = TEXTURE_PATH + "elements/"
import gettext
Chinese = gettext.translation('zh_CN', localedir='locale', languages=['zh'])
English = gettext.translation('en', localedir='locale', languages=['en'])
Chinese.install()

defaultsettings={'showplayertag':True,'defaultplayertag':_('press F5 to set playertag'),'playername':'anonymous',
'level1name':'beg','level2name':'int','level3name':'exp','level4name':'cus','enablerec':True,
'defaultlevel':'int','timeringame':True,'showsafesquares':False,'instantclick':False,'disableright':False,
'endflagall':True,'failrestart':False,'failrestart_percentage':100,'language':1,'noguess':False}

invars=(#成绩指标
        ('est','est{2,,0,999.99,1}'),
        ('qg','pow(est,1.7)/self.game.bbbv{-1,,0,0,1}'),
        ('rqp','est*(est+1)/self.game.bbbv{-1,,0,0,1}'),
        ('rt','rt{2,3600,0}'),
        #局面指标
        ('bv','self.game.bbbv{-1,6400,1,1,1}'),
        ('bvdone','solvedbv{-1,6400,0,0,1}'),
        ('is','self.game.islands{-1,1000,0,0,1}'),
        ('isdone','self.game.solvedislands{-1,1000,0,0,1}'),
        ('mine','self.game.mineNum{-1,999,4,4}'),
        ('op','self.game.ops{-1,1000,0,0,1}'),
        ('opdone','self.game.solvedops{-1,1000,0,0,1}'),
        ('row','self.game.row{-1,80,4,4}'),
        ('width','self.game.column{-1,80,4,4}'),
        #操作指标
        ('ce','sum(self.game.eclicks){-1,,0,0}'),
        ('cl','sum(self.game.allclicks[0:3]){-1,,0,0}'),
        ('dce','self.game.eclicks[2]{-1,,0,0}'),
        ('dcl','self.game.allclicks[2]{-1,,0,0}'),
        ('flag','self.game.allclicks[3]{-1,999,0,0}'),
        ('lce','self.game.eclicks[0]{-1,,0,0}'),
        ('lcl','self.game.allclicks[0]{-1,,0,0}'),
        ('path','self.game.path{-1,,0,0}'),
        ('rce','self.game.eclicks[1]{-1,,0,0}'),
        ('rcl','self.game.allclicks[1]{-1,,0,0}'),
        #效率指标
        ('corr','sum(self.game.eclicks)/sum(self.game.allclicks[0:3]){-1,,0,0}'),
        ('ioe','solvedbv/sum(self.game.allclicks[0:3]){-1,,0,0,1}'),
        ('iome','solvedbv/self.game.path{-1,,0,0,1}'),
        ('thrp','solvedbv/sum(self.game.eclicks){-1,,0,0,1}'),
        #统计指标
        ('games','self.game.gamenum{-1,,0,0}'),
        ('tallrank','self.game.ranks[0]{-1,,0,0}'),
        ('ballrank','self.game.ranks[1]{-1,,0,0}'),
        ('sallrank','self.game.ranks[2]{-1,,0,0}')
        )

def adjacent(i,j,index,row,column):
    if j==0: # left edge
        if i==0: # top-left corner
            return (index+1,index+column,index+column+1)
        elif i==row-1: # bottom-left corner
            return (index-column,index-column+1,index+1)
        else:
            return (index-column,index-column+1,index+1,index+column,index+column+1)
    elif j==column-1: # right edge
        if i==0: # top-right corner
            return (index-1,index+column-1,index+column)
        elif i==row-1: # bottom-right corner
            return (index-column-1,index-column,index-1)
        else:
            return (index-column-1,index-column,index-1,index+column-1,index+column)
    else:
        if i==0: # top edge
            return (index-1,index+1,index+column-1,index+column,index+column+1)
        elif i==row-1: # bottom edge
            return (index-column-1,index-column,index-column+1,index-1,index+1)
        else:
            return (index-column-1,index-column,index-column+1,index-1,index+1,index+column-1,index+column,index+column+1)

# column 1. left down
# column 2. left up
# column 3. right down
# column 4. right up
changeMouseStatus=[[]]

class smallfuc(object):#放一些静态方法
    @staticmethod
    def linyu(i,j,r,c):
        return abs(i-r)<=1 and abs(j-c)<=1
