# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : weapon.py
# Create date : 2020-3-10
# Modified date : 2020-3-10
# All rights reserved:北京华戍防务技术有限公司
# Author:aie
##########################################################################################################

from ..entitys.activeunit import CActiveUnit


class CUnguidedWeapon():
    '''
    动态创建非制导武器
    '''
    def __init__(self, strGuid, mozi_server, situation):
        self.mozi_server = mozi_server
        self.situation = situation
        self.strGuid = strGuid