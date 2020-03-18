# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : sensor.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################



class CSensor():
    '''传感器'''
    def __init__(self, strGuid, mozi_server, situation):
        self.mozi_server = mozi_server
        self.situation = situation
        self.strGuid =strGuid
