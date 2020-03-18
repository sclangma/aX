# -*- coding:utf-8 -*-
##########################################################################################################
# File name : satellite.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################
from MoziService.entitys.activeunit import CActiveUnit


class CSatellite(CActiveUnit):
    '''
    卫星类
    '''
    def __init__(self, strGuid, mozi_server, situation):
        super().__init__()
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation
        
    def sate_set_rader_shutdown(self,trunoff):
        '''
        设置雷达开关机
        trunoff 开关机 true 开机  false 关机
        '''
        return super().set_rader_shutdown(trunoff)

    def sate_set_sonar_shutdown(self,trunoff):
        '''
        设置声纳开关机
        trunoff 开关机 true 开机  false 关机
        '''
        return super().set_sonar_shutdown(trunoff)

    def sate_set_OECM_shutdown(self,trunoff):
        '''
        设置干扰开关机
        trunoff 开关机 true 开机  false 关机
        '''
        return super().set_OECM_shutdown(trunoff)