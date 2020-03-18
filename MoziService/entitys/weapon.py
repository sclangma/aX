# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : weapon.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

from ..entitys.activeunit import CActiveUnit


class CWeapon():
    '''武器'''
    def __init__(self, strGuid, mozi_server, situation):
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation

    def delete_sub_object(self):
        """
        删除时删除子对象
        :return:
        """
        del_list = []
        if self.doctrine is not None:
            del_list.append(self.doctrine.guid)
            del self.doctrine

        del_list.extend(self.way_points.keys())
        del self.way_points
        del_list.extend(list(self.sensors.keys()))
        del self.sensors
        return del_list

    def get_summary_info(self):
        """
        获取精简信息, 提炼信息进行决策
        :return: dict
        """
        info_dict = {
            "guid": self.guid,
            "DBID": self.iDBID,
            "subtype": "0",
            "facilityTypeID": "",
            "name": self.strName,
            "side": self.side_name,
            "proficiency": "",  # ?
            "latitude": self.dLatitude,
            "longitude": self.dLongitude,
            "altitude": self.fAltitude_AGL,
            "course": self.get_way_points_info(),
            "heading": self.fCurrentHeading,
            "speed": self.fCurrentSpeed,
            "throttle": self.m_CurrentThrottle,
            "autodetectable": self.bAutoDetectable,
            "unitstate": self.strActiveUnitStatus,  # ?
            "fuelstate": "",
            "weaponstate": -1,  # ?
            "mounts": self.get_mounts_info(),
            "targetedBy": self.get_target_by_info(),
            "target": self.m_PrimaryTargetGuid,
            "shooter": self.m_FiringUnitGuid,
            "type": "Weapon",
            "fuel": -1,  # ?
            "damage": -1,  # ?
            "sensors": self.get_sensors_info(),
            "weaponsValid": self.get_valid_weapons()
        }
        return info_dict


    def weapon_auto_detectable(self,isAutoDetectable):
        '''
        单元自动探测到
        isAutoDetectable：是否探测到 true?false complate
        '''
        super().unit_auto_detectable(isAutoDetectable)
        

    def unitTargetSimBreakOff(self, Type, side, targetGuid, unitGuid, distance):
        '''
        武器距离目标多少公里后暂停
        type:类型
        side：推演方
        targetGuid：目标guid
        weaponDBID:武器的BDID
        distance:距离（公里） complate
        '''
        weaponTargetSimBreakOff = "Hs_WeaponTargetSimBreakOff('%s', {SIDE = '%s', CONTACTGUID = '%s', ACTIVEUNITGUID = '%s', DISTANCE = %s})"% (
            Type,side,targetGuid,self.strGuid,distance)
        return self.sendAndRecv(weaponTargetSimBreakOff)        