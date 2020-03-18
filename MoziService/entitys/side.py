#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##########################################################################################################
# File name : side.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################
from abc import ABCMeta, abstractmethod
import re
import logging

from ..entitys.mission import CMission
from ..entitys.activeunit import CActiveUnit
from .mission import CMission
from .aircraft import CAircraft
from .mssnstrike import CStrikeMission

########################################################################
class CSide():
    '''方'''

    #----------------------------------------------------------------------
    def __init__(self, strGuid,mozi_server, situation):
        """Constructor"""
        self.mozi_server = mozi_server
        self.situation = situation
        self.strGuid = strGuid  # Guid      #changed by aie

    #################################################################
    '''获取函数区'''
    #################################################################

    def get_all_unitinfo(self):
        '''
        获取本方所有实体的信息
        通过本方单元字典拼接而成
        update 去重合并
        '''
        all_unitinfo = {}
        all_unitinfo.update(self.aircrafts)
        all_unitinfo.update(self.ships)
        all_unitinfo.update(self.satellites)
        all_unitinfo.update(self.submarines)
        all_unitinfo.update(self.weapons)
        all_unitinfo.update(self.facilitys)
        return all_unitinfo
        

    def scenEdit_getScore(self,side_name,mozi_server):
        '''
        获取方的分数  
        param: 
        side_name ：要获取的方的分数
        mozi_server ：调用服务器的基础类
        return ：60(分数)
        
        '''
        lua_str = '''ret = ScenEdit_GetScore("%s")
                print(ret)
                ''' % (side_name)
        return float(self.mozi_server.sendAndRecv(lua_str))

    
   
    #def scenEdit_SetScore(self,sideName,score):
    def scenEdit_SetScore(self, score):         #changed by aie
        '''
        设置指定阵营的分数
        LUA_ScenEdit_SetScore  (side, score, reason)
        ScenEdit_GetScore("PlayerS        ide", 20)
        '''
        #return self.mozi_server.sendAndRecv("ReturnObj(ScenEdit_SetScore('{}',{}))".format(self.strName,score))
        return self.mozi_server.sendAndRecv("ScenEdit_SetScore('{}',{})".format(self.strName, score))  #changed by aie

    def initial_units(self):
        """
        创建实体、任务
        :return:
        """
        pass

    def set_simulate_time(self, str_simulate_time):
        '''
        设置环境时间
        '''
        self.simulate_time = str_simulate_time


    def getUnits(self):
        units = {}
        units.update(self.situation.submarine_dic)
        units.update(self.situation.ship_dic)
        units.update(self.situation.facility_dic)
        units.update(self.situation.aircraft_dic)
        sideUnits = {}
        for k, v in units.items():
            if v.m_Side == self.strGuid:
                sideUnits.update({k:v})
        return sideUnits

    def getAircrafts(self):
        aircrafts = {}
        aircrafts = {k:v for k,v in self.situation.aircraft_dic.items() if v.m_Side == self.strGuid}
        return aircrafts


    def getMissions(self):
        mssns = {}
        mssns.update(self.situation.mssnpatrol_dic)
        mssns.update(self.situation.mssnstrike_dic)
        mssns.update(self.situation.mssnsupport_dic)
        mssns.update(self.situation.mssncargo_dic)
        mssns.update(self.situation.mssnferry_dic)
        mssns.update(self.situation.mssnmining_dic)
        mssns.update(self.situation.mssnmnclrng_dic)
        sideMssns = {}
        for k, v in mssns.items():
            if v.strName == self.strGuid:
                sideMssns.update({k:v})
        return sideMssns

    def getMission(self,nameOrID):
        mssns = self.getMissions()
        if nameOrID in mssns:
            return mssns[nameOrID]
        for k, v in mssns.items():
            if v.strName == nameOrID:
                return v
        return None

    def getStrikeMission(self,nameOrID):
        mssns = self.getMissions()
        if nameOrID in mssns:
            return mssns[nameOrID]
        for k, v in mssns.items():
            if v.m_Category == 0:
                if v.strName == nameOrID:
                    return v
        return None


    def get_mission_by_name(self, mission_name):
        """
        通过任务名获取任务对象
        :return:
        """
        if mission_name in self.missions:
            return self.missions[mission_name]
        else:
            return None

    def __units_parser(self, units_return_str):
        """
        解析返回的实体字符串
        :param units_return_str: str, lua执行后返回的实体单元字符串
        :return: dict, {guid: name}  例：{"fj-2f":"su-27", "er-2j":"su-35"}
        """
        pass


    def get_units(self):
        """
        获取本方所有实体guid，name
        :return: dict, {guid: name}  例：{"fj-2f":"su-27", "er-2j":"su-35"}
        """
        lua_arg = "print(VP_GetSide({side = '%s'}).units)" % self.strName
        return self.mozi_server.sendAndRecv(lua_arg)

    def get_unit_byguid(self, guid):
        """
        获取实体
        :param guid: str, 实体guid/
        :return: Unit, 作战单元
        """
        if self.units:
            if guid in self.units:
                return self.units[guid]
            else:
                self.initial_units()
                if guid in self.units:
                    return self.units[guid]
                else:
                    return None
        else:
            if guid in self.aircrafts:
                return self.aircrafts[guid]
            if guid in self.facilitys:
                return self.facilitys[guid]
            if guid in self.weapons:
                return self.weapons[guid]
            return None

    def get_contact(self, contact_guid):
        """
        获取情报对象
        :param contact_guid:  情报对象guid, 非实际单元guid
        :return:
        """
        if contact_guid in self.contacts:
            return self.contacts[contact_guid]
        else:
            return None


    def getContacts(self):
        # reconstructed by aie
        if self.m_ContactList == '':
            return {}
        else:
            indx = self.m_ContactList.split('@')
            contacts = {}
            for k in indx:
                contacts[k] = self.situation.contact_dic[k]
        return contacts
        """
        获取本方当前已知的所有情报实体
        :return: dict, {'guid':'name'}
        """
        #lua_arg = "print(VP_GetSide({side = '%s'}).contacts)" % self.strName
        #return self.mozi_server.sendAndRecv(lua_arg)

    def getContact(self, nameOrId):
        '''
        by aie
        '''
        a = self.getContacts()
        if a == {}:
            return None
        if nameOrId in a:
            return a[nameOrId]
        for k,v in a.items():
            if v.strName == nameOrId :
                return v[nameOrId]
        return None

    def getStrikeMssns(self):
        return {k:v for k,v in self.situation.mssnstrike_dic.items() if v.m_Side == self.strGuid}

    def getRange(self,objA,objB):
        cmd = "ReturnObj(Tool_Range('{}','{}'))".format(objA.strGuid, objB.strGuid)
        self.situation.throwIntoPool(cmd)
        return eval(self.mozi_server.sendAndRecv(cmd))

    def getScore(self):
        return self.iTotalScore

    def get_elevation(self, coord_point):
        """
        获取某点（纬经度）
        :param coord_point: tuple, (float, float) (lat, lon)
        :return: int, 地形高程数据
        """
        lua_cmd = "ReturnObj(World_GetElevation ({latitude='%lf',longitude='%lf'}))" % (coord_point[0], coord_point[1])
        return int(self.mozi_server.sendAndRecv(lua_cmd))

    def reference_point_add(self, points):
        """
        添加一个或多个参考点
        :param points: tuple, 或list,  参考点列表,例:(40.2, 49.6) 或 [(40, 39.0), (41, 39.0)]，其中纬度值在前，经度值在后
                                                或者 (40.2, 49.6, 'RP002') 或 [(40, 39.0, 'RP1'), (41, 39.0, 'RP2')]，已传入参考点命名
        :return:
        ['point_name1','point_name2']点集名称
        """
        if not points:
            return None

        points_name = None
        if isinstance(points, tuple):
            # 判断参数是否元组
            if len(points) == 2:
                points_name = "RP_AUTO_CREATE%d" % self.__reference_point_index_increment
                self.__reference_point_index_increment += 1
                self.pointname2location[points_name] = points
            elif len(points) == 3:
                points_name = points[2]
                self.pointname2location[points_name] = points[0:2]
            else:
                return None
            self.mozi_server.addReferencePoint(side=self.strName, pointName=points_name,
                                             lat=points[0], lon=points[1],highlighted='true')
        elif isinstance(points, list):
            # 判断参数是否参考点列表
            points_name = []
            for point in points:
                if isinstance(point, tuple):
                    p_name = self.reference_point_add(point)
                    if p_name is not None:
                        points_name.append(p_name)
        return points_name

    def set_reference_point(self, rp_name, new_coord):
        """
        设置参考点的位置
        :param rp_name: str, 参考点名称
        :param new_coord: tuple, 新的经纬度位置 (lat, lon)
        :return:
        """
        set_str = "ScenEdit_SetReferencePoint({{side='{}',name='{}', lat={}, lon={}}})".format(self.strName, rp_name, new_coord[0], new_coord[1])
        self.pointname2location[rp_name] = new_coord
        return self.mozi_server.sendAndRecv(set_str)

    def delete_reference_point(self, rp_name):
        """
        删除参考点
        :param rp_name:  str, 参考点名称
        :return:
        """
        set_str = 'ScenEdit_DeleteReferencePoint({name="%s",side="%s"})'%(rp_name, self.strName)
        del self.pointname2location[rp_name]
        return self.mozi_server.sendAndRecv(set_str)

    #################################################################
    '''处置函数区'''
    #################################################################
    def prepAircraft(self):
        strGuid = 'prep'
        ac = CAircraft(strGuid, self.mozi_server, self.situation)
        ac.m_Side = self.strGuid
        return ac

    def prepStirkeMission(self):
        strGuid = 'prep'
        mssn = CStrikeMission(strGuid,self.mozi_server,self.situation)
        mssn.m_Side = self.strGuid
        return mssn


    #################################################################
    '''处置函数区'''
    #################################################################

    def addSubmarine(self, name, dbid, latitude, longitude, heading=0):
        cmd = "ScenEdit_AddUnit({type = 'Submarine', name = '%s', heading = %s," \
              " dbid = %s, side = '%s', Latitude=%s,Longitude=%s})" % (
            name, heading, dbid, self.strGuid, latitude, longitude)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def addShip(self, name, dbid, latitude, longitude, heading=0):
        cmd = "ScenEdit_AddUnit({type = 'Ship', name = '%s', heading = %s," \
              " dbid = %s, side = '%s', Latitude=%s,Longitude=%s})" % (
            name, heading, dbid, self.strGuid, latitude, longitude)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def addFacility(self, name, dbid, latitude, longitude, heading=0):
        cmd = "ScenEdit_AddUnit({type = 'Facility', name = '%s', heading = %s," \
              " dbid = %s, side = '%s', Latitude=%s,Longitude=%s})" % (
            name, heading, dbid, self.strGuid, latitude, longitude)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)


    def addAircraft(self, ac):
        cmd = "ScenEdit_AddUnit({type = 'Aircraft', side = '%s', name = '%s', dbid = %s, loadoutid = %s," \
              " Latitude=%s,Longitude=%s, Altitude=%s, heading = %s})" % (
            self.strGuid, ac.strName, ac.iDBID, ac.iLoadoutDBID, ac.dLatitude, ac.dLongitude, ac.fCurrentAlt, ac.fCurrentHeading)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def addSatellite(self, Type, name, dbid, loadoutid, latitude, longitude, altitude, heading):
        cmd = "ScenEdit_AddUnit({type = '%s', name = '%s', loadoutid = %s, heading = %s," \
              " dbid = %s, side = '%s', Latitude=%s,Longitude=%s, Altitude=%s})" % (
            Type, name, loadoutid, heading, dbid, self.strGuid, latitude, longitude, altitude)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def addUnit(self, Type, name, dbid, loadoutid, latitude, longitude, altitude, heading):
        cmd = "ScenEdit_AddUnit({type = '%s', name = '%s', loadoutid = %s, heading = %s," \
              " dbid = %s, side = '%s', Latitude=%s,Longitude=%s, Altitude=%s})" % (
            Type, name, loadoutid, heading, dbid, self.strGuid, latitude, longitude, altitude)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def setMarkContacts(self, contacts, mark):
        #TODO aie
        '''cntcts = "{'"
        for k in contacts.keys():
            cntcts = cntcts + k + "','"
        cntcts = cntcts + '}'
        cntcts = cntcts.replace(",'}",'}')
        cmd = "Hs_SetMarkContact('{}', {{}}, '{}')".format(self.strGuid, cntcts, mark)
        self.situation.throwIntoPool(cmd)
        '''
        results = ''
        for k,v in contacts.items():
            cmd = "Hs_SetMarkContact('{}', '{}', '{}')".format(self.strGuid, v.strGuid, mark)
            self.situation.throwIntoPool(cmd)
            ret = self.mozi_server.sendAndRecv(cmd)
            results = results + ret
        return results

    def addMission(self, missionName, model, detailed):
        cmd = "ScenEdit_AddMission('{}','{}','{}',{})".format(self.strName, missionName, model, detailed)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def deleteMission(self, mission):
        cmd = "ScenEdit_DeleteMission ('{}','{}')".format(self.strGuid, mission)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def addStrikeMission(self,mssn):
        cmd = "ScenEdit_AddMission('{}','{}','strike',{{type='{}'}})".format(self.strName, mssn.strName, mssn.m_Category)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def add_prosecution_zone(self, mission_name, point_list):
        """
        增加巡逻任务的警戒区
        :param mission_name: str, 任务名
        :param point_list: list, list, 参考点列表,例:[(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)]，其中纬度值在前，经度值在后，(40, 39.0)中,latitude = 40, longitude = 39.0
                            或者[(40, 39.0, 'RP1'), (41, 39.0, 'RP2'), (41, 40.0, 'RP3'), (40, 40.0, 'RP4')]
                            或者['RP1', 'RP2'，'RP3'，'RP4']，传入参考点名称要求提前创建好参考点
        :return:
        """
        self.mozi_server.setMission(self.strName, mission_name,
                                    '{' + self.__get_zone_str(point_list).replace('Zone', 'prosecutionZone') + '}')


    def create_strike_mission(self, name, mission_type):
        """
        创建打击任务
        :param name: str, 任务名
        :param mission_type: MissionStrikeType, 打击任务类型，对空打击，对地打击等
        :return: Mission, 任务实体
        """
        pass

    def create_support_mission(self, name, point_list):
        """
        创建支援任务, 例子：
            create_support_mission('空中支援', [(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)])
        :param name: str, 任务名
        :param point_list: list, 参考点列表,例:[(40, 39.0), (41, 39.0), (41, 40.0), (40, 40.0)]，其中纬度值在前，经度值在后，(40, 39.0)中,latitude = 40, longitude = 39.0
                            或者[(40, 39.0, 'RP1'), (41, 39.0, 'RP2'), (41, 40.0, 'RP3'), (40, 40.0, 'RP4')]
                            或者['RP1', 'RP2'，'RP3'，'RP        4']，传入参考点名称要求提前创建好参考点
        :return: Mission, 任务实体
        """
        pass

    def __save_mission(self, mission_name, mission_return_str, mission_category):
        """
        保存任务到本方，方便以后调用
        :param mission_name: 任务名
        :param mission_return_str: 任务调用返回值
        :return: Mission, Mission实例
        """
        pass

    def delete_mission(self, mission_name):
        """
        删除任务
        :param mission_name: str, 任务名称
        :return:
        """
        lua = 'print(ScenEdit_DeleteMission("%s", "%s"))' % (self.strName, mission_name)
        self.mozi_server.sendAndRecv(lua)
        del self.missions[mission_name]


    def zone_remove(self, zone_guid):
        """
        删除禁航区或封锁区域
        :param zone_guid: str, 区域的guid
        :return:
        """
        return self.mozi_server.removeZone(self.strName, zone_guid)

    def zone_add_no_navigate(self, reference_points, **kwargs):
        """
        定义禁航区
        :param reference_points:list, 参考点列表
        :param kwargs:  Isactive：int 是否启用1='true', 0='false'
                        Affects：int 选定区域应用于(0=Aircraft飞机；Submarine潜艇；1=Facility地面单元；Ship水面舰艇)
                        Locked：int 是否区域已锁定1='true', 0=  'false' (只有禁航区才需要设置)
        :return:str, zone guid
        """
        point_names = self.reference_point_add(reference_points)
        point_count = len(point_names)
        if not point_count:
            return None

        area_description = 'Area={"'
        for name in point_names[: point_count-1]:
            area_description += name + '","'
        name = point_names[-1]
        area_description += name + '"}'

        table_arg = '{'
        table_arg += ('Description="禁航区' + str(self.__zone_index_increment)) + '",' + area_description + '}'
        self.__zone_index_increment += 1
        zone_guid = self.mozi_server.addZone(self.strName, '0', table_arg)
        if len(kwargs) > 0:
            self.zone_set(zone_guid, kwargs)
        else:
            self.zone_set(zone_guid, Isactive=1, Affects=0, Locked=0)
        return zone_guid

    def zone_add_exclusion(self, reference_points, **kwargs):
        """
        定义封锁区
        :param reference_points:list, 参考点列表
        :param kwargs:  Isactive：int 是否启用1='true', 0='false'
                        Affects：int 选定区域应用于(0=Aircraft飞机；Submarine潜艇；1=Facility地面单元；Ship水面舰艇)
                        Locked：int 是否区域已锁定1='true', 0=  'false' (只有禁航区才需要设置)
        :return:str, zone guid
        """
        point_names = self.reference_point_add(reference_points)
        point_count = len(point_names)
        if not point_count:
            return None

        area_description = 'Area={"'
        for name in point_names[: point_count - 1]:
            area_description += name+'","'
        name = point_names[-1]
        area_description += name+'"}'

        table_arg = '{'
        table_arg += ('Description="封锁区' + str(self.__zone_index_increment)) + '",' + area_description + '}'
        self.__zone_index_increment += 1
        zone_guid = self.mozi_server.addZone(self.strName, '1', table_arg)
        if len(kwargs) > 0:
            self.zone_set(zone_guid, kwargs)
        else:
            self.zone_set(zone_guid, Isactive=1, Affects=0, Locked=0)
        return zone_guid

    def zone_set(self, zone_guid, **kwargs):
        """
        修改禁航区和封锁区
        :param zone_guid: 禁航区和封锁区的guid
        :param kwargs:  Area：list 添加地图中选择的参考点(向区域列表中添加)(暂不支持,想要修改点请先删除再新建)
                        Description: string 名字
                        Isactive：int 是否启用1='true', 0='false'
                        Affects：int 选定区域应用于(0=Aircraft飞机；Submarine潜艇；1=Facility地面单元；Ship水面舰艇)
                        Locked：int 是否区域已锁定1='true', 0='false' (只有禁航区才需要设置)
                        MarkAs： int 2=非友方，3=敌方（封锁区才有的设置）
                        RPVISIBLE: int 1=true 0=false
        :return:
        """
        table = '{'
        for key, value in kwargs.items():
            if key == 'Isactive':
                if value == 1:
                    table += ',Isactive=true'
                elif value == 0:
                    table += ',Isactive=false'
            if key == 'Affects':
                if value == 0:
                    table += ',Affects={"Aircraft"}'
                elif value == 1:
                    table += ', Affects={"Ship"}'
            if key == 'MarkAs':
                if value == 2:
                    table += ', MarkAs=2'
                elif value == 3:
                    table += ', MarkAs=3'
            if key == 'RPVISIBLE':
                if value == 1:
                    table += ",RPVISIBLE=true"
                elif value == 0:
                    table += ",RPVISIBLE=false"
            if key == 'Locked':
                if value == 1:
                    table += ', Locked=true'
                elif value == 0:
                    table += ', Locked=false'
        if table[1] == ',':
            table = table.replace(',', '', 1)
        table += '}'
        return self.mozi_server.setZone(self.strName, zone_guid, table)

    def group_add(self, list_unit_guid):
        """
        将多个单元作为一个编队
        :param list_unit_guid: list, 例：['2abc947e-8352-4639-9184-641706730018','640a7c08-a17a-4fba-b055        -07b568f22df5']
        :return:
        """
        list_unit_guid = str(list_unit_guid).replace('[', '{').replace(']', '}')
        return self.mozi_server.scenEdit_AddGroup(list_unit_guid)



    def group_add_unit(self, group_guid, unit_guid):
        """
        编队添加一个单元
        :param group_guid: 编队guid
        :param unit_guid: 作战单元guid
        :return:
        """
        table = '{guid="' + unit_guid + '",group="' + group_guid + '"}'
        lua_scrpt = "ScenEdit_SetUnit({})".format(table)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    
    def air_group_out(self, air_guid_list):
        """
        编组出动
        :param air_guid_list:  list, 飞机的guid，  例子：['71136bf2-58ba-4013-92f5-2effc99d2wds','71136bf2-58ba-4013-92f5-2effc99d2fa0']
        :return:
        """
        table = str(air_guid_list).replace('[', '{').replace(']', '}')
        lua_scrpt = "Hs_LUA_AirOpsGroupOut('{}',{})".format(self.strName, table)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def hold_position_all_unit(self, is_hold):
        """
        保持所有单元阵位，所有单元停止机动，留在原地
        :param is_hold: bool
        :return:
        """
        return self.mozi_server.sendAndRecv("Hs_HoldPositonAllUnit('{}',{})".format(self.strName, str(is_hold).lower()))


    def scenEdit_setEvent(self, eventName, model):
        '''
        #创建和设置事件 eventname为事件名称 
        #eventTableMode为{mode='add',IsActive = false, IsRepeatable=true, Probability =100,IsShown = false} 
        # mode 是类型 添加删除修改之类的 isactive 是否激活  IsRepeatable 是否重复 Probability概率 IsShown是否显示
        返回乱执行是否成功 （string）
        '''        
        return self.mozi_server.sendAndRecv("ScenEdit_SetEvent ('%s',{mode='%s'})" % (eventName,model))
    

    def scenEdit_setAction(self, actionTableMode):
        '''
        创建动作和设置动作
        actionTableMode 为{Description='想定结束',mode='add',type='endscenario'}
        Description 动作名称 mode 操作类型 类似有添加删除 type为类型 有想定结束单元移动等
        返回乱执行是否成功 （string）
        '''        
        return self.mozi_server.sendAndRecv(" ScenEdit_SetAction({})".format(actionTableMode))        
    
    
    
    def scenEditSetTrigger(self, triggerTableMode):
        '''
        创建和设置触发器
        triggerTableMode 为 {Description='航母被摧毁',mode='add',type= "unitdestroyed",TargetFilter={TARGETSIDE="中国",TARGETTYPE="Ship"}}
        Description 触发器名称 mode 操作类型同上 type触发器类型 类似有单元被摧毁 单元被毁伤之类的 
        TargetFilter={TARGETSIDE="中国",TARGETTYPE="Ship"} 是单元被毁伤和单元被摧毁的 TARGETSIDE为单元所在方  TARGETTYPE 为类型还有子类型参数
        返回乱执行是否成功 （string）
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_SetTrigger ({})".format(triggerTableMode))        
        
        
    

    def scenEdit_setEventTrigger(self, eventName, mode , name , replacedby = None):
        '''
        为事件添加触发器
        eventName 事件名称
        triggername 触发器名称
        mode 操作类型
        返回乱执行是否成功 （string）
        '''
        lua_scrpt =''
        if replacedby == None :
            lua_scrpt =  "ScenEdit_SetEventTrigger('%s', {mode = '%s',name = '%s'})" % (eventName,mode,name)
        else:
            lua_scrpt = "ScenEdit_SetEventTrigger('%s', {mode = '%s',name = '%s' ,replacedby= ''})" % (eventName,mode,name,replacedby)
        return self.mozi_server.sendAndRecv(lua_scrpt)
                
                
                

    def scenEditSetEventAction(self, eventName, mode ,name):
        '''
        为事件添加动作
        eventName 事件名称
        actionName 动作器名称
        mode 操作类型
        返回乱执行是否成功 （string）
        '''
        lua_scrpt = "ScenEdit_SetEventAction('%s', {mode = '%s',name = '%s'})" % (eventName,mode,name)
        return self.mozi_server.sendAndRecv(lua_scrpt)         
          
    def addUnit(self, type, name, dbid, latitude, longitude):
        ''' 
        添加单元 complate
        '''
        lua_scrpt = ("ReturnObj(ScenEdit_AddUnit({side = '%s', type = '%s', name = '%s', dbid = %s, latitude = %s, longitude = %s}))"
                     % (self.strName,type,name,dbid,latitude,longitude))
        result =  self.mozi_server.sendAndRecv(lua_scrpt)
      


    def addAirToFacility(self,type, name, dbid,loadoutid ,baseUnitGuid ):
        '''
        往机场，码头添加单元       
        '''
        self.mozi_server.sendAndRecv("ReturnObj(ScenEdit_AddUnit({ type = '%s', unitname = '%s',side='%s', dbid = %s, loadoutid = %s, base = '%s'}))"
                         %(type,name,self.strName,dbid,loadoutid,baseUnitGuid))


    def delete_allUnit(self):
        '''
        删除本方所有单元
        '''        
        return self.mozi_server.sendAndRecv("Hs_DeleteAllUnits({})".format(self.strName))


    def setEMCON(self, objectType, objectName, emcon):
        '''
        设置选定对象的 EMCON
        objectType 对象类型 'Side' / 'Mission' / 'Group' / 'Unit'
        objectName 对象名称 'Side Name or ID' / 'Mission Name or ID' / 'Group Name or ID' / 'Unit Name or ID'
        emcon 传感器类型和传感器状态 'Radar/Sonar/OECM=Active/Passive;' / 'Inherit'
        例 ：
        ScenEdit_SetEMCON(['Side' / 'Mission' / 'Group' / 'Unit'], ['Side Name or ID' / 'Mission Name or ID' / 
        'Group Name or ID' / 'Unit Name or ID'], ['Radar/Sonar/OECM=Active/Passive;' / 'Inherit'])
        '''        
        return self.mozi_server.sendAndRecv("ScenEdit_SetEMCON('{}','{}','{}')".format(objectType,objectName,emcon))                          
                          
    
    def addReferencePoint(self, pointName, lat, lon, highligted):
        '''
        添加参考点
        pointName 参考点名称
        lat 纬度
        lon 经度
        '''
        return self.mozi_server.sendAndRecv("ScenEdit_AddReferencePoint({side='%s', name='%s', lat=%s, lon=%s, highlighted=%s})"%(self.strName, pointName, lat, lon,highligted))
                                        
                                                          
   
          
    def deployMine(self, mineType, mineCount, area):
        '''
        给某一方添加雷
        mineType 类型
        mineCount 数量
        area table类型 布雷区域
        '''
        return self.mozi_server.sendAndRecv("Hs_DeployMine('{}','{}',{},{})".format(self.strName,mineType,mineCount,area))
    
                         
    def addOn_flyZone(self, description, area):
        '''
        添加禁航区
        description 禁航区名称
        area 区域 area={"RP-112","RP-113","RP-114","RP-115"}
        '''
        return self.mozi_server.sendAndRecv(
            "Hs_AddZone('%s', {Description = '%s', Area = %s})"%(self.strName,description,area))    


    def cloneETAC(self, table):
        '''
        克隆事件、触发器、条件、动作
        table  {CLONETRIGGER = '", triggerGuid, "'} { CLONEEVENT = '", eventGuid, "' } 
        { CLONECONDITION = '", conditionGuid, "' }     { CLONEACTION = '", actionGuid, "' }
        '''        
        return self.mozi_server.sendAndRecv("Hs_CloneETAC({})".format(table))
    

    def reset_allSide_scores(self):
        '''
        重置所有推演方分数
        '''        
        return self.mozi_server.sendAndRecv("Hs_ResetAllSideScores()")


    def reset_doctrine(self, GUID, LeftMiddleRight, EnsembleWeaponEMCON):
        '''
        Hs_ResetDoctrine 重置条令
        GUID 为要设置的推演方、任务、单元、编组 GUID
        LeftMiddleRight Left：重置作战条令，Middle 重置关联的作战单元，Right 重置关联的使命任务
        EnsembleWeaponEMCON Ensemble：总体，EMCON 电磁管控设置，Weapon 武器使用规则
        '''        
        return self.mozi_server.sendAndRecv("Hs_ResetDoctrine('{}','{}','{}')".format(GUID,LeftMiddleRight,EnsembleWeaponEMCON))
    
    

    def set_new_sideNaem(self, sideNewIdOrName):
        '''
        推演方重命名
        sideNewIdOrName 新名称
        '''        
        return self.mozi_server.sendAndRecv("setNewSideNaem('{}','{}')".format(self.strName,sideNewIdOrName))