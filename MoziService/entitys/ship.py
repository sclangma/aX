#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################################################################################
# File name : ship.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
# All rights reserved:北京华戍防务技术有限公司
# Author:xy
##########################################################################################################
# File name : ship.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

import re
from ..entitys.activeunit import CActiveUnit

class CShip(CActiveUnit):
    '''
    水面舰艇
    '''

    # ----------------------------------------------------------------------
    def __init__(self, strGuid, mozi_server, situation):
        """
        初始化函数
        """
        super().__init__()
        self.mozi_server = mozi_server
        self.situation = situation
        self.strGuid = strGuid


    def ship_manual_pick_war(self, target_guid, weapon_dbid, weapon_num):
        '''
        手动开火函数
        作者：解洋
        fire_unit_guid:开火单元guid
        target_guid : 目标guid
        weapon_dbid : 武器的dbid
        weapon_num : 武器数量        
        return :
        lua执行成功/lua执行失败
        '''
        self.strGuid = self.guid
        return super().manual_pick_war(target_guid, weapon_dbid, weapon_num)

    def ship_set_up_throttleI(self):
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

    def ship_set_down_throttleI(self):
        '''
        降油门
        '''
        throttle_str = ""
        if self.m_CurrentThrottle == Throttle.Loiter:
            throttle_str = "FullStop"
        if self.m_CurrentThrottle == Throttle.Full:
            throttle_str = "Loiter"
        if self.m_CurrentThrottle == Throttle.Flank:
            throttle_str = "Full"
        if self.m_CurrentThrottle == Throttle.Cruise:
            throttle_str = "Flank"
        super().set_throttle(throttle_str)

    def ship_ops_singleout(self, base_guid):
        '''
        设置在基地内单机出动
        base_guid : 飞机所在机场的guid
        return :
        lua执行成功/lua执行失败
        '''
        self.strGuid = self.guid
        return super().unitops_singleout(base_guid, self.guid)

    def ship_set_rader_shutdown(self, trunoff):
        '''
        设置雷达开关机
        '''
        return super().set_rader_shutdown(trunoff)

    def ship_set_sonar_shutdown(self, trunoff):
        '''
        设置声纳开关机
        '''
        return super().set_sonar_shutdown(trunoff)

    def ship_set_OECM_shutdown(self, trunoff):
        '''
        设置干扰开关机
        '''
        super().set_OECM_shutdown(trunoff)

    def ship_set_desired_height(self, desired_height):
        """
        设置单元的期望高度
        :param desired_height: 期望高度值, 海拔高度：m
        :return:
        """
        return super().set_desired_height(desired_height)

    def ship_return_to_base(self):
        '''
        返回基地
        '''
        self.strGuid = self.guid
        return super().return_to_base()

    def ship_plotted_course(self, course_list):
        """
        航线规划  lat 纬度， lon 经度
        :param course_list: list, [(lat, lon)], 例子：[(40, 39.0), (41, 39.0)]
        :return:
        """
        self.strGuid = self.guid
        return super().plotted_course(course_list)

    def ship_drop_active_sonobuoy(self, sideName, deepOrShallow):
        '''
        投放主动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        return super().drop_active_sonobuoy(sideName, deepOrShallow)

    def ship_drop_passive_sonobuoy(self, sideName, deepOrShallow):
        '''
        投放被动声呐
        sidename 方的名称        
        deepOrShallow 投放深浅 例: dedp ，shallow
        '''
        return super().drop_passive_sonobuoy(sideName, deepOrShallow)

    def ship_attack_auto(self, contact_guid):
        """
        自动攻击目标
        :param contact_guid: 目标guid
        :retu    rn:
        """
        return super().attack_auto(contact_guid)
