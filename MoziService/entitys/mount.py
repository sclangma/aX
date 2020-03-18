# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : mount.py
# Create date : 2020-1-8
# -*- coding:utf-8 -*-
##########################################################################################################
# File name : magazine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CMount():
    '''挂载'''
    #def __init__(self, guid, name, parentPlatform):    # changed by aie
    def __init__(self, strGuid,mozi_server, situation):
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation

