TEXTURE_PATH = "MS-Texture/svg/"
CELL_PATH = TEXTURE_PATH + "cells/"
FACE_PATH = TEXTURE_PATH + "faces/"
ELEMENT_PATH = TEXTURE_PATH + "elements/"

defaultsettings={'showplayertag':True,'defaultplayertag':'请按F5设置标识','playername':'anonymous',
'level1name':'beg','level2name':'int','level3name':'exp','level4name':'cus','enablerec':True }

class smallfuc(object):#放一些静态方法
    @staticmethod
    def linyu(i,j,r,c):
        return abs(i-r)<=1 and abs(j-c)<=1
