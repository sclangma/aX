# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : scenario.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

from ..entitys.situation import CSituation
from ..entitys.side import CSide


class CScenario():
    '''想定'''
    def __init__(self, mozi_server):
        self.mozi_server = mozi_server
        # 态势
        self.situation = CSituation(mozi_server)

        # 类名
        self.ClassName = "CCurrentScenario"
        # GUID
        self.strGuid = ""
        # 标题
        self.strTitle = ""
        # 想定文件名
        self.strScenFileName = ""
        # 描述
        self.strDescription = ""
        # 当前时间
        self.m_Time = ""
        # 是否是夏令时
        self.bDaylightSavingTime = False
        # 当前想定第一次启动的开始时间
        self.m_FirstTimeRunDateTime = ""
        # 用不上
        self.m_FirstTimeLastProcessed = 0.0
        # 用不上
        self.m_grandTimeLastProcessed = 0.0
        # 夏令时开始时间（基本不用）
        self.strDaylightSavingTime_Start = 0.0
        # 夏令结束时间（基本不用）
        self.strDaylightSavingTime_End = 0.0
        # 想定开始时间
        self.m_StartTime = ""
        # 想定持续时间
        self.m_Duration = ""
        # 想定精细度
        self.sMeta_Complexity = 1
        # 想定困难度
        self.sMeta_Difficulty = 1
        # 想定发生地
        self.strMeta_ScenSetting = ""
        # 想定精细度的枚举类集合
        self.strDeclaredFeatures = ""
        # 想定的名称
        self.strCustomFileName = ""
        # 编辑模式剩余时间
        self.iEditCountDown = 0
        # 推演模式剩余时间
        self.iStartCountDown = 0
        # 暂停剩余时间
        self.iSuspendCountDown = 0
        # 获取推演的阶段模式
        self.m_CurrentStage = 0
        #推演方
        self.m_sides={}

    #################################################################
    '''获取函数区'''
    #################################################################

    def getTitle(self):
        '''
        by aie
        '''
        return self.strTitle

    def getDescription(self):
        '''
        by aie
        '''
        return self.strDescription

    def getWeather(self):
        '''
        by aie
        '''
        return self.situation.weather

    def getCurrentTime(self):
        '''
        by aie
        '''
        return self.m_Time

    def getSideByName(self, sidename):
        '''
        by aie
        '''
        sides = self.situation.side_dic
        for k,v in sides.items():
            if v.strName == sidename:
                return v
        print("The side doesn't exist.")
        return None

    def getSide(self, nameOrID):
        '''
        by aie
        '''
        sides = self.situation.side_dic
        if nameOrID in sides:
            return sides[nameOrID]
        for k,v in sides.items():
            if v.strName == nameOrID:
                return v
        return None

    def getPosture(self, nameOrID):
        '''
        by aie
        '''
        a = self.getSide(nameOrID)
        if a == None:
            print("The side doesn't exist.")
            return None
        sides = self.situation.side_dic
        if nameOrID in sides:
            return sides[nameOrID].m_PosturesDictionary
        for k, v in sides.items():
            if v.strName == nameOrID:
                return v.m_PosturesDictionary
        return None

    #################################################################
    '''处置函数区'''
    #################################################################

    def addSide(self,name):
        cmd = "HS_LUA_AddSide({side='%s'})" % (name)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def removeSide(self,name):
        cmd = "ScenEdit_RemoveSide({side='%s'})" % (name)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def setSidePosture(self, sideAName, sideBName, relation):
        '''
        设置对抗关系 complate
        :param sideAName:
        :param sideBName:
        :param relation:：字符串。立场编码（'F'-友好，'H'-敌对，'N'-中立，'U'-非友）
        :return:
        '''
        cmd = "ScenEdit_SetSidePosture('{}','{}','{}')".format(sideAName, sideBName, relation)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)


    #################################################################
    '''查验函数区'''
    #################################################################

    def isSide(self,name):
        '''
        判断是否存在方
        '''
        n = 0
        for k, v in self.situation.side_dic.items():
            if v.strName == name:
                n = 1
                return True
        if n == 0:
            return False
