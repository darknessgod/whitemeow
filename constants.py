TEXTURE_PATH = "MS-Texture/svg/"
CELL_PATH = TEXTURE_PATH + "cells/"
FACE_PATH = TEXTURE_PATH + "faces/"
ELEMENT_PATH = TEXTURE_PATH + "elements/"

defaultsettings={'showplayertag':True,'defaultplayertag':'请按F5设置标识','playername':'anonymous',
'level1name':'beg','level2name':'int','level3name':'exp','level4name':'cus','enablerec':True,
'defaultlevel':'int','timeringame':True,'showsafesquares':False,'instantclick':False,'disableright':False,
'endflagall':True}

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

class smallfuc(object):#放一些静态方法
    @staticmethod
    def linyu(i,j,r,c):
        return abs(i-r)<=1 and abs(j-c)<=1
