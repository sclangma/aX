#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : aircraft.py
# Create date : 2019-11-06 19:38
# Modified date : 2019-12-25 16:09
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from .commonfunction import parse_weapons_record
from .loadout import CLoadout
from ..entitys.activeunit import CActiveUnit
from ..entitys import database as db


class CAircraft(CActiveUnit):
    '''飞机'''

    def __init__(self, strGuid, mozi_server, situation):
        '''飞机'''
        super().__init__()
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation
        self.strName = None
        self.fAltitude_AGL = None
        self.iAltitude_ASL = None
        self.m_Side = None
        self.strUnitClass = None
        self.dLatitude = None
        self.dLongitude = None
        self.fCurrentHeading = None
        self.fCurrentSpeed = None
        self.fCurrentAltitude_ASL = None
        self.fPitch = None
        self.fRoll = None
        self.fDesiredAltitude = None
        self.fDesiredSpeed = None
        self.m_MaxThrottle = None
        self.fMaxSpeed = None
        self.fMinSpeed = None
        self.fCurrentAlt = None
        self.fDesiredAlt = None
        self.bDesiredAltitudeOverride = None
        self.bDesiredSpeedOverride = None
        self.fMaxAltitude = None
        self.fMinAltitude = None
        self.iDBID = None
        self.bIsOperating = None
        self.m_ParentGroup = None
        self.m_DockedUnits = None
        self.m_DockFacilitiesComponent = None
        self.m_DockAircrafts = None
        self.m_AirFacilitiesComponent = None
        self.m_CommDevices = None
        self.m_Engines = None
        self.m_Sensors = None
        self.m_Mounts = None
        self.strDamageState = None
        self.iFireIntensityLevel = None
        self.iFloodingIntensityLevel = None
        self.m_AssignedMission = None
        self.m_Doctrine = None
        self.m_UnitWeapons = None
        self.m_HostActiveUnit = None
        self.strActiveUnitStatus = None
        self.strFuelState = None
        self.m_WayPoints = None
        self.m_ProficiencyLevel = None
        self.bIsEscortRole = None
        self.m_CurrentThrottle = None
        self.bIsCommsOnLine = None
        self.bIsIsolatedPOVObject = None
        self.bTerrainFollowing = None
        self.bIsRegroupNeeded = None
        self.bHoldPosition = None
        self.bAutoDetectable = None
        self.m_Cargo = None
        self.dFuelPercentage = None
        self.m_AITargets = None
        self.m_CommLink = None
        self.m_NoneMCMSensors = None
        self.iDisturbState = None
        self.iMultipleMissionCount = None
        self.m_MultipleMissionGUIDs = None
        self.m_Magazines = None
        self.bObeysEMCON = None
        self.m_BearingType = None
        self.m_Bearing = None
        self.m_Distance = None
        self.bSprintAndDrift = None
        self.strDockAircraft = None
        self.m_Category = None
        self.m_Type = None
        self.m_CurrentHostUnit = None
        self.iLoadoutDBID = None
        self.m_LoadoutGuid = None
        self.strAirOpsConditionString = None
        self.strFinishPrepareTime = None
        self.strQuickTurnAroundInfo = None
        self.fHoverSpeed = None
        self.fLowSpeed = None
        self.fCruiseSpeed = None
        self.fMilitarySpeed = None
        self.fAddForceSpeed = None
        self.m_MaintenanceLevel = None
        self.fFuelConsumptionCruise = None
        self.fAbnTime = None
        self.iFuelRecsMaxQuantity = None
        self.iCurrentFuelQuantity = None
        self.bQuickTurnaround_Enabled = None
        self.bIsAirRefuelingCapable = None
        self.strShowTankerHeader = None
        self.m_ShowTanker = None
        self.m_bProbeRefuelling = None
        self.m_bBoomRefuelling = None
        self.strWayPointName = None
        self.strWayPointDescription = None
        self.WayPointDTG = None
        self.WayPointTTG = None
        self.WayPointFuel = None

    def get_loadout_info(self):
        pass

    def air_delete_sub_object(self):
        """
        当删除本元素时，删除子对象
        返回需要先删除的子对象guid列表
        :return:
        """
        del_list = self.delete_sub_object()  # guid 列表  sensors.keys()， mounts.keys()

        if self.loadout is not None:
            del_list.append(self.loadout.guid)
            del self.loadout
        return del_list

    def air_get_loadout_info(self):
        """
        获取挂载方案的武器信息
        :return:
        """
        if self.loadout is None:
            return ""
        else:
            info = [{
                "loadout_name": self.loadout.strName,
                "loadout_guid": self.loadout.guid,
                "loadout_dbid": self.loadout.iDBID,
                "loadout_weapons": parse_weapons_record(self.loadout.m_LoadRatio)
            }]
        return info

    def air_get_valid_weapons(self):
        """
        获取飞机有效的武器
        :return:
        """
        info = {}
        # mount.values 可能是不同的mount，mount_obj.strWeapon,说明mount_obj 是一个对象
        for mount_obj in self.mounts.values():
            if (mount_obj.strWeaponFireState == "就绪" or "秒" in mount_obj.strWeaponFireState) \
                    and mount_obj.m_ComponentStatus <= 1:
                mount_weapons = parse_weapons_record(mount_obj.m_LoadRatio)
                for w_record in mount_weapons:
                    w_dbid = w_record['wpn_dbid']
                    if db.check_weapon_attack(w_dbid):
                        if w_dbid in info:
                            info[w_dbid] += w_record['wpn_current']
                        else:
                            info[w_dbid] = w_record['wpn_current']
        if self.loadout is not None:
            mount_weapons = parse_weapons_record(self.loadout.m_LoadRatio)
            for w_record in mount_weapons:
                w_dbid = w_record['wpn_dbid']
                if db.check_weapon_attack(w_dbid):
                    if w_dbid in info:
                        info[w_dbid] += w_record['wpn_current']
                    else:
                        info[w_dbid] = w_record['wpn_current']
        return info

    def air_get_summary_info(self):
        """
        获取精简信息, 提炼信息进行决策
        :return: dict
        """
        info_dict = {
            # "guid": self.guid,
            "guid": self.strGuid,
            "DBID": self.iDBID,
            "subtype": str(self.m_Type),
            "facilityTypeID": "",
            "name": self.strName,
            # "side": self.side_name,
            "proficiency": self.m_ProficiencyLevel,  # ?
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "altitude_asl": self.iAltitude_ASL,
            # "course": self.get_way_points_info(),
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,  # ?
            "fuelstate": self.strFuelState,  # ?
            "weaponstate": -1,  # ?
            "mounts": self.get_mounts_info(),
            "targetedBy": self.get_target_by_info(),
            "pitch": self.fPitch,
            "roll": self.fRoll,
            "yaw": self.fCurrentHeading,  # ?
            "loadout": self.get_loadout_info(),
            "type": "Aircraft",
            "fuel": self.iCurrentFuelQuantity,  # ?
            "damage": self.strDamageState,  # ?
            "sensors": self.get_sensors_info(),
            "weaponsValid": self.get_valid_weapons()
        }
        return info_dict

    def get_status_type(self):
        """
        获取飞机状态
        :return: int
        """
        if self.strAirOpsConditionString in (1, 2, 4, 8, 9, 18, 23, 24, 26):
            # 在基地可马上部署飞行任务
            return 'validToFly'
        elif self.strAirOpsConditionString in (0, 13, 14, 15, 16, 19, 20, 21, 22):
            # 在空中可部署巡逻，进攻，航路规划
            return 'InAir'
        elif self.strAirOpsConditionString in (5, 10, 11, 17, 25):
            # 在空中返航或降落
            return 'InAirRTB'
        else:
            return 'WaitReady'

    def switchRadar(self, emcon):
        cmd = "ScenEdit_SetEMCON('{}','{}','Radar={}')".format('Unit', self.strGuid, emcon)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def air_set_waypoint(self, side_name, guid, longitude, latitude):
        '''
        设置飞机下一个航路点
        :param strGuid:
        :param longitude:
        :param latitude:
        :return:
        '''
        lua_str = "ScenEdit_SetUnit({side= '%s', guid='%s', course={ { Description = ' ', TypeOf = 'ManualPlottedCourseWaypoint', longitude = %s, latitude = %s } } })" % (
            side_name, guid, longitude, latitude)
        return self.mozi_server.sendAndRecv(lua_str)

    def air_autoattack_target(self, target_guid):
        '''
        自动攻击
        target_guid 目标guid
        '''
        guid = self.strGuid
        ret = self.mozi_server.sendAndRecv("ScenEdit_AttackContact ('%s', '%s', {mode=0})" % (guid, target_guid))
        return ret

    def air_get_guid_from_name(self, target_name, all_info_dict):
        '''
        查找飞机guid通过飞机名称
        target_name : 要查找的单元名称
        all_info_dict : 单元字典
        
        return :
        '25368-sddssfas-sddsdwe-5dsacdc'/False
        '''
        for guid in all_info_dict:
            item = all_info_dict[guid]
            name = item.get("strName", "")
            class_name = item["ClassName"]
            if class_name != "CContact":
                if name == target_name:
                    return guid
        return False

    def air_check_is_exist_target(self, target_name, all_info_dict):
        '''
        检查目标是否存在
        param ：
        target_name ：目标名称
        all_info_dict ：所有单元信息字典
        return : true（存在）/false（不存                                                                                                                                                                                                                                                                                                                                                                                        ）
        '''
        ret = self.get_guid_from_name(target_name, all_info_dict)
        if ret:
            return True
        return False

    def air_manual_pick_war(self, target_guid, weapon_dbid, weapon_num):
        '''
        飞机手动开火函数
        作者：解洋
        target_guid : 目标guid
        weapon_dbid : 武器的dbid
        weapon_num : 武器数量        
        return :
        lua执行成功/lua执行失败
        '''
        self.strGuid = self.guid
        return super().manual_pick_war(target_guid, weapon_dbid, weapon_num)

    def air_set_up_throttleI(self):
        '''
        升油门
        '''

        self.strGuid = self.guid
        throttle_str = ""
        if self.m_CurrentThrottle == 0:
            throttle_str = "Loiter"
        elif self.m_CurrentThrottle == 1:
            throttle_str = "Full"
        elif self.m_CurrentThrottle == 2:
            throttle_str = "Flank"
        elif self.m_CurrentThrottle == 3:
            throttle_str = "Cruise"
        else:
            return None
        return super().set_throttle(throttle_str)

    def air_set_down_throttleI(self):
        '''
        降油门
        '''
        throttle_str = ""
        if self.m_CurrentThrottle == 1:
            throttle_str = "FullStop"
        if self.m_CurrentThrottle == 2:
            throttle_str = "Loiter"
        if self.m_CurrentThrottle == 3:
            throttle_str = "Full"
        if self.m_CurrentThrottle == 4:
            throttle_str = "Flank"
        return super().set_throttle(throttle_str)

    def air_ops_singleout(self, base_guid):
        '''
        设置在基地内飞机单机出动
        base_guid : 飞机所在机场的guid
        return :
        lua执行成功/lua执行失败
        '''
        return super().unitops_singleout(base_guid, self.guid)

    def air_set_rader_shutdown(self, trunoff):
        '''
        设置雷达开关机
        guid : 要设置单元唯一标识（guid）
        '''
        self.strGuid = self.guid
        return super().set_rader_shutdown(trunoff)

    def set_air_desired_height(self, desired_height):
        """
        设置单元的期望高度
        :param desired_height: 期望高度值, 海拔高度：m
        :return:
        """
        self.strGuid = self.guid
        return super().set_desired_height(desired_height)

    def air_return_to_base(self):
        '''
        飞机返回基地
        '''
        self.strGuid = self.guid
        return super().return_to_base()

    def air_plotted_course(self, course_list):
        """
        飞机航线规划
        :param course_list: list, [(lat, lon)], 例子：[(40, 39.0), (41, 39.0)]
        :return:
        """
        return super().plotted_course(course_list)

    def air_deploy_dipping_sonar(self):
        '''
        部署吊放声呐
        '''
        zz = self.mozi_server
        self.strGuid = self.guid
        return self.mozi_server.sendAndRecv("Hs_DeployDippingSonar('{}')".format(self.strGuid))

    def air_assign_unitList_to_missionEscort(self, mission_name):
        """
        将单元分配为某打击任务的护航任务
        :param mission_name: 任务名称
        """
        self.strGuid = self.guid
        return super().assign_unitList_to_missionEscort(mission_name)

    def air_drop_active_sonobuoy(self, sideName, deepOrShallow):
        '''
        投放主动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: deep ，shallow
        '''
        self.strGuid = self.guid
        return super().drop_active_sonobuoy(sideName, deepOrShallow)

    def air_drop_passive_sonobuoy(self, sideName, deepOrShallow):
        '''
        投放被动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        self.strGuid = self.guid
        return super().drop_passive_sonobuoy(sideName, deepOrShallow)

    def setAirborneTime(self, unitNameOrId, hour, minute, scond):
        '''
        设置留空时间
        unitNameOrId 单元
        hour 小时
        minute 分钟
        scond 秒
        '''
        lua_scrpt = "Hs_SetAirborneTime('{}',{},{},{})".format(unitNameOrId, hour, minute, scond)
        return self.mozi_server.sendAndRecv(lua_scrpt)

    def timeToReady(self, time):
        '''
        Hs_ScenEdit_TimeToReady 空中任务设置出动准备时间
        time 时间
        '''
        self.strGuid = self.guid
        return self.mozi_server.sendAndRecv("Hs_ScenEdit_TimeToReady({},{})".format(time, self.strGuid))
