# -*- coding:utf-8 -*-
# TODO
##########################################################################################################
# File name : doctrine.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################

class CDoctrine():
    def __init__(self,strGuid,mozi_server,situation):
        self.mozi_server =mozi_server
        self.situation = situation
        self.strGuid = strGuid

        
    def SetDoctrineAir(self,sideName,fireState):
        '''
        设置单元的攻击条令（自动攻击(FREE)、限制开火(TIGHT)、不能开火 (HOLD)、与上级一致(INHERITED)）
        用法
        武器控制状态，对空
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_air = "0"})
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        武器控制状态，对海
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_surface = "2"})
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        武器控制状态，对潜
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_subsurface = "0"})
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        武器控制状态，对地
        ScenEdit_SetDoctrine({side = "美国"}, {weapon_control_status_land = "2"}) 
        0 - -自由开火
        1 - -谨慎开火
        2 - -限制开火
        '''            
        return self.sendAndRecv("ScenEdit_SetDoctrine({side ='%s' }, {weapon_control_status_air ='%s}'})"%(sideName,fireState))

    
    def doctrine_switch_radar(self, switch_on):
        """
        条令中，电磁管控设置，设置雷达
        :param switch_on: bool, 雷达打开或者静默，True:打开
        :return:
        """
        if switch_on:
            set_str = 'Radar=Active'
        else:
            set_str = 'Radar=Passive'

        if self.category == 'Side' or self.category == 'Mission':
            id_str = self.name
        else:
            id_str = self.guid

        cmd_str = "ScenEdit_SetEMCON('%s', '%s', '%s')" % (self.category_str, id_str, set_str)
        self.mozi_server.sendAndRecv(cmd_str)

    def doctrine_SetEMCON_Inherit(self, bTrueOrFalse):
        """
        设置电磁管控是否与上级一致
        :param bTrueOrFalse: bool，是否与上级一致
        :return:
        """
        if bTrueOrFalse:
            bTrueOrFalse = 'yes'
        elif not bTrueOrFalse:
            bTrueOrFalse = 'no'
        else:
            print('Error：bTrueOrFalse参数输入错误！')
        cmd = "Hs_SetInLineWithSuperiors('{}','{}')".format(self.guid, bTrueOrFalse)
        return self.mozi_server.sendAndRecv(cmd)
    
    def doctrine_engaging_ambiguous_targets(self, towards_ambigous_target):
        """
        接战模糊位置目标
        :param towards_ambigous_target: BehaviorTowardsAmbigousTarget
        :return:
        """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                               '{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')
        elif self.category == 'Mission':
            if towards_ambigous_target.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{engaging_ambiguous_targets=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')
        else:
            if towards_ambigous_target.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engaging_ambiguous_targets=\"inherit\"}')
            else:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')
    
       
    def doctrine_ignore_plotted_course(self, ignore_plotted_courseEnum):
        """
        攻击时忽略计划航线设置
        :param ignore_plotted_courseEnum:IgnorePlottedCourseWhenAttacking，选择枚举
        :return:
        """
        if self.category == 'Side':
            if ignore_plotted_courseEnum == 0:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_plotted_course=' + 'false' + '}')
            elif ignore_plotted_courseEnum == 1:
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_plotted_course=' + 'true' + '}')
        elif self.category == 'Mission':
            if ignore_plotted_courseEnum.value == 0:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_plotted_course=' + 'false' + '}')
            if ignore_plotted_courseEnum.value == 1:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_plotted_course=' + 'true' + '}')
            if ignore_plotted_courseEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_plotted_course=\"inherit\"}')
        else:
            if ignore_plotted_courseEnum == 0:
                return self.mozi_server.sendAndRecv("ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=false})" % self.guid)
                # return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{ignore_plotted_course=' + 'false' + '}')
            elif ignore_plotted_courseEnum == 1:
                return self.mozi_server.sendAndRecv("ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=true})" % self.guid)
                # return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{ignore_plotted_course=' + 'true' + '}')
            elif ignore_plotted_courseEnum == 2:
                return self.mozi_server.sendAndRecv("ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=\"inherit\"})" % self.guid)
              
    
    def doctrine_engage_opportunity_targets(self, engage_opportunity_targetsEnum):
            """
            接战临机出现目标
            :param engage_opportunity_targetsEnum: EngageWithContactTarget, 枚举
            :return:
            """
            if self.category == 'Side':
                if engage_opportunity_targetsEnum == 'No_Only':
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{engage_opportunity_targets=' + 'false' + '}')
                elif engage_opportunity_targetsEnum == 'Yes_AnyTarget':
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{engage_opportunity_targets=' + 'true' + '}')
            elif self.category == 'Mission':
                if engage_opportunity_targetsEnum == 'No_Only':
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{engage_opportunity_targets=' + 'false' + '}')
                elif engage_opportunity_targetsEnum == 'Yes_AnyTarget':
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{engage_opportunity_targets=' + 'true' + '}')
                elif engage_opportunity_targetsEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{engage_opportunity_targets=\"inherit\"}')
            else:
                if engage_opportunity_targetsEnum == 'No_Only':
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engage_opportunity_targets=' + 'false' + '}')
                elif engage_opportunity_targetsEnum == 'Yes_AnyTarget':
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engage_opportunity_targets=' + 'true' + '}')
                elif engage_opportunity_targetsEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{engage_opportunity_targets=\"inherit\"}')
    
    def doctrine_ignore_emcon_under_attack(self, ignore_emcon_while_under_attackEnum):
            """
            受到攻击忽略电磁管控
            :param ignore_emcon_while_under_attackEnum: IgnoreEMCONUnderAttack, 枚举
            :return:
            """
            if self.category == 'Side':
                if ignore_emcon_while_under_attackEnum == 0:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_emcon_while_under_attack=' + 'false' + '}')
                elif ignore_emcon_while_under_attackEnum == 1:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_emcon_while_under_attack=' + 'true' + '}')
            elif self.category == 'Mission':
                if ignore_emcon_while_under_attackEnum.value == 0:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{ignore_emcon_while_under_attack=' + 'false' + '}')
                if ignore_emcon_while_under_attackEnum.value == 1:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{ignore_emcon_while_under_attack=' + 'true' + '}')
                if ignore_emcon_while_under_attackEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{ignore_emcon_while_under_attack=\"inherit\"}')
            elif self.category == 'Unit':
                if ignore_emcon_while_under_attackEnum == 0:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{ignore_emcon_while_under_attack=' + 'false' + '}')
                elif ignore_emcon_while_under_attackEnum == 1:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{ignore_emcon_while_under_attack=' + 'true' + '}')
                elif ignore_emcon_while_under_attackEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{ignore_emcon_while_under_attack=\"inherit\"}')
    
    def doctrine_automatic_evasion(self, automatic_evasionEnum):
            """
            自动规避
            :param automatic_evasionEnum: AutomaticEvasion, 枚举
            :return:
            """
            if self.category == 'Side':
                if automatic_evasionEnum == 0:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{automatic_evasion=' + 'false' + '}')
                elif automatic_evasionEnum == 1:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{automatic_evasion=' + 'true' + '}')
            elif self.category == 'Mission':
                if automatic_evasionEnum.value == 0:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}',
                        '{automatic_evasion=' + 'false' + '}')
                if automatic_evasionEnum.value == 1:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}', '{automatic_evasion=' + 'true' + '}')
                if automatic_evasionEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}', '{automatic_evasion=\"inherit\"}')
            else:
                if automatic_evasionEnum == 0:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{automatic_evasion=' + 'false' + '}')
                elif automatic_evasionEnum == 1:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{automatic_evasion=' + 'true' + '}')
                elif automatic_evasionEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{automatic_evasion=\"inherit\"}')
    
    def doctrine_air_operations_tempo(self, air_operations_tempoEnum):
            """
            空战节奏
            :param air_operations_tempoEnum: AirOpsTempo, 枚举
            :return:
            """
            if self.category == 'Side':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{air_operations_tempo=' + str(air_operations_tempoEnum.value) + '}')
            elif self.category == 'Mission':
                if air_operations_tempoEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{air_operations_tempo=\"inherit\"}' )
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{air_operations_tempo='+ str(air_operations_tempoEnum.value)+'}' )
            else:
                if air_operations_tempoEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{air_operations_tempo=\"inherit\"}')
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{air_operations_tempo=' + str(air_operations_tempoEnum.value) + '}')
    
    def doctrine_fuel_state_planned(self, fuel_state_plannedEnum):
            """
            燃油状态，预先规划
            :param fuel_state_plannedEnum: FuelState, 枚举
            :return:
            """
            if self.category == 'Side':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}', '{fuel_state_planned=' + str(fuel_state_plannedEnum.value) + '}')
            elif self.category == 'Mission':
                if fuel_state_plannedEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}', '{fuel_state_planned=\"inherit\"}')
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{fuel_state_planned=' + str(fuel_state_plannedEnum.value) + '}')
            else:
                if fuel_state_plannedEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{fuel_state_planned=\"inherit\"}')
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{fuel_state_planned=' + str(
                                                                           fuel_state_plannedEnum.value) + '}')
    
    def doctrine_fuel_state_rtb(self, fuel_state_rtbEnum):
            """
            燃油状态，返航
            :param fuel_state_rtbEnum: FuelStateRTB, 枚举
            :return:
            """
            if self.category == 'Side':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')
            elif self.category == 'Mission':
                if fuel_state_rtbEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}', '{fuel_state_rtb=\"inherit\"}')
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')
            else:
                if fuel_state_rtbEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{fuel_state_rtb=\"inherit\"}')
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                '{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')
    
    def doctrine_weapon_state_planned(self, weapon_state_plannedEnum):
            """
            武器状态，预先规划
            :param weapon_state_plannedEnum:WeaponStatePlanned, 枚举
            :return:
            """
            if self.category == 'Side':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                                   '{weapon_state_planned=' + str(weapon_state_plannedEnum.value) + '}')
            elif self.category == 'Mission':
                if weapon_state_plannedEnum.value==999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{weapon_state_planned=\"inherit\"}' )
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{weapon_state_planned='+ str(weapon_state_plannedEnum.value)+'}' )
            else:
                if weapon_state_plannedEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{weapon_state_planned=\"inherit\"}')
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{weapon_state_planned=' + str(
                                                                           weapon_state_plannedEnum.value) + '}')
    
    def doctrine_weapon_state_rtb(self, weapon_state_rtbEnum):
            """
            武器状态-返航
            :param weapon_state_rtbEnum: WeaponStateRTB, 枚举
            :return:
            """
            if self.category == 'Side':
                return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                               '{weapon_state_rtb=' + str(weapon_state_rtbEnum.value) + '}')
            elif self.category == 'Mission':
                if weapon_state_rtbEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine(
                        '{side="' + self.side_name + '",mission="' + self.name + '"}', '{weapon_state_rtb=\"inherit\"}')
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{weapon_state_rtb=' + str(weapon_state_rtbEnum.value) + '}')
            else:
                if weapon_state_rtbEnum.value == 999:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{weapon_state_rtb=\"inherit\"}')
                else:
                    return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                       '{weapon_state_rtb=' + str(
                                                                           weapon_state_rtbEnum.value) + '}')
    
    def doctrine_gun_strafing(self, gun_strafingEnum):
        """
        空对地扫射
        :param gun_strafingEnum: GunStrafeGroundTargets, 枚举
        :return:
        """
        if self.category == 'Side':
            return self.mozi_server.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                           '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
        elif self.category == 'Mission':
            if gun_strafingEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{gun_strafing=\"inherit\"}')
            return self.mozi_server.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
        else:
            if gun_strafingEnum.value == 999:
                return self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{gun_strafing=\"inherit\"}')
            else:
                self.mozi_server.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                            '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
    
    # def wra_qty_salvo(self, weaponID, target_type, select_type):
    #     """
    #     武器使用规则--齐射武器数
    #     :param weaponID: 武器DBID
    #     :param target_type: WRA_WeaponTargetType
    #     :param select_type: WRAWeaponQty
    #     :return:
    #     """
    #     # if self.category == 'Side':
    #     #     ele_type = ElementType.Side
    #     # else:
    #     #     ele_type = ElementType.Facility
    #     target_type = target_type.value
    #     # value_arg = cf.get_weapon_qty_value(ele_type, weaponID, target_type, select_type)
    #     if self.category == 'Side':
    #         table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{qty_salvo="%s"})' % (
    #         self.side_name, weaponID, target_type, value_arg)
    #         return self.mozi_server.sendAndRecv(table)
    #     elif self.category == 'Mission':
    #         table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{qty_salvo="%s"})' % (
    #         self.side_name, self.name, weaponID, target_type, value_arg)
    #         return self.mozi_server.sendAndRecv(table)
    #     else:
    #         table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{qty_salvo="%s"})' % (
    #         self.guid, weaponID, target_type, value_arg)
    #         return self.mozi_server.sendAndRecv(table)
    
    # def wra_shooter_salvo(self, weaponID, target_type, select_type):
    #     """
    #     武器使用规则--齐射发射架数
    #     :param weaponID: 武器DBID
    #     :param target_type: WRA_WeaponTargetType
    #     :param select_type: WRAShooterQty
    #     :return:
    #     """
    #     if self.category == 'Side':
    #         ele_type = ElementType.Side
    #     else:
    #         ele_type = ElementType.Facility
    #     target_type = target_type.value
    #     select_type = cf.get_shooter_qty_value(ele_type, weaponID, target_type, select_type)
    #     # logging.info('shooter_salvo:%d' % select_type)
    #     if self.category == 'Side':
    #         table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{shooter_salvo="%s"})' % (
    #         self.side_name, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    #     elif self.category == 'Mission':
    #         table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{shooter_salvo="%s"})' % (
    #         self.side_name, self.name, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    #     else:
    #         table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{shooter_salvo="%s"})' % (
    #         self.guid, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    
    # def wra_firing_range(self, weaponID, target_type, select_type):
    #     """
    #     武器使用规则 - -自动开火距离
    #     :param weaponID: 武器DBID
    #     :param target_type: WRA_WeaponTargetType
    #     :param select_type: WRASelfAttackRange
    #     :return:
    #     """
    #     if self.category == 'Side':
    #         ele_type = ElementType.Side
    #     else:
    #         ele_type = ElementType.Facility
    #     target_type = target_type.value
    #     select_type = cf.get_firing_range_value(ele_type, weaponID, target_type, select_type)
    #     # logging.info('firing_range:%d' % select_type)
    #     if self.category == 'Side':
    #         table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{firing_range="%s"})' % (
    #         self.side_name, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    #     elif self.category == 'Mission':
    #         table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{firing_range="%s"})' % (
    #         self.side_name, self.name, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    #     else:
    #         table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{firing_range="%s"})' % (
    #         self.guid, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    
    # def wra_self_defence_distance(self, weaponID, target_type, select_type):
    #     """
    #     武器使用规则--自动防御距离
    #     :param weaponID: 武器DBID
    #     :param target_type: WRA_WeaponTargetType
    #     :param select_type: WRASelfDefenceRange
    #     :return:
    #     """
    #     if self.category == 'Side':
    #         ele_type = ElementType.Side
    #     else:
    #         ele_type = ElementType.Facility
    #     target_type = target_type.value
    #     select_type = cf.get_self_defence_value(ele_type, weaponID, target_type, select_type)
    #     # logging.info('defence_distance:%d' % select_type)
    #     if self.category == 'Side':
    #         table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{self_defence="%s"})' % (
    #         self.side_name, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    #     elif self.category == 'Mission':
    #         table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{self_defence="%s"})' % (
    #         self.side_name, self.name, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    #     else:
    #         table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{self_defence="%s"})' % (
    #         self.guid, weaponID, target_type, select_type)
    #         return self.mozi_server.sendAndRecv(table)
    
    def withdraw_on_damage(self, select_type):
        """
        满足如下条件时撤退 - -毁伤程度大于
        :param select_type: DamageThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_damage={}}})'.format(self.side_name,
                                                                                             select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_fuel={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_fuel={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def withdraw_on_fuel(self, select_type):
        """
        满足如下条件时撤退--燃油少于
        :param select_type: FuelQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_fuel={}}})'.format(self.side_name, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_fuel={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_fuel={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def withdraw_on_attack(self, select_type):
        """
        满足如下条件时撤退--主要攻击攻击武器至少处于
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value
            
        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_attack={}}})'.format(self.side_name,
                                                                                             select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_attack={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_attack={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def withdraw_on_defence(self, select_type):
        """
        满足如下条件时撤退--主要防御武器至少
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_defence={}}})'.format(self.side_name,
                                                                                              select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_defence={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_defence={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def deploy_on_damage(self, select_type):
        """
        满足如下条件时重新部署--毁伤程度小于
        :param select_type: DamageThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_damage={}}})'.format(self.side_name, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_damage={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_damage={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def deploy_on_fuel(self, select_type):
        """
        满足如下条件时重新部署--燃油至少处于
        :param select_type: FuelQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_fuel={}}})'.format(self.side_name, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_fuel={}}})'.format(self.side_name,
                                                                                                        self.name,
                                                                                                        select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_fuel={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def deploy_on_attack(self, select_type):
        """
        满足如下条件时重新部署--主要攻击武器处于
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_attack={}}})'.format(self.side_name, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_attack={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_attack={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)
    
    def deploy_on_defence(self, select_type):
        """
        满足如下条件时重新部署--主要防御武器处于
        :param select_type        
        : WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == 'Side':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_defence={}}})'.format(self.side_name, select_type)
            return self.mozi_server.sendAndRecv(table)
        elif self.category == 'Mission':
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_defence={}}})'.format(
                self.side_name, self.name, select_type)
            return self.mozi_server.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_defence={}}})'.format(self.guid, select_type)
            return self.mozi_server.sendAndRecv(table)

