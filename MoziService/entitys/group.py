# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : group.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

from ..entitys.activeunit import CActiveUnit


class CGroup(CActiveUnit):
    def __init__(self, strGuid, mozi_server, situation):
        CActiveUnit.mozi_server = mozi_server
        self.situation = situation
        self.strGuid =strGuid

    def delete_sub_object(self):
        """
        删除时删除子对象
        :return:
        """
        del_list = list(self.way_points.keys())
        for guid, point in self.way_points.items():
            del_list.extend(point.delete_sub_object())
        del self.way_points

        if self.doctrine is not None:
            del_list.append(self.doctrine.guid)
            del self.doctrine
        return del_list
    
    
    def removeUnitFromGroup(self, unitId):
        '''
        将单元移除编组
        unitId 单元ID
        '''
        return self.mozi_server.sendAndRecv("Hs_RemoveUnitFromGroup('{}')".format(unitId))
 

    def scenEdit_AddGroup(self, unitGuidList):
        '''
        将单元添加到新建的组
        unitGuidList：单元的 guid，guid 之间用逗号分隔
        用法：
        Hs_ScenEdit_AddGroup({'613f00e1-4fd9-4715-a672-7ec5c22486cb','431337a9-987e-46b6-8cb8-2f92b9b80335','0bc3        1a3c-096a-4b8e-a
        23d-46f7ba3b06b3'})
        '''
        res =  self.mozi_server.sendAndRecv("ReturnObj(Hs_ScenEdit_AddGroup({}))".format(unitGuidList))
        return res.split('\r\n')[5].split('=')[1].split(',')[0].replace(',','').replace('\'','').replace(' ','').s  
 
   
    def groupFormation(self, table):
        '''
        编组设置队形
        table 编组队形参数 {"2","686b0f99-533a-432c-9c24-e31e92d69afd","45","5",true}
        '''           
        return self.mozi_server.sendAndRecv("Hs_GroupFormation({})".format(table))