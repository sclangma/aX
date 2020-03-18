# -*- coding:utf-8 -*-

import time
import json
import traceback
import logging

from MoziService.entitys.global_util import *
from MoziService.entitys.element import Element
import MoziService.entitys.commonfunction as cf

loop_request_count = 3


class DoctrineOperator(Element):
    '''条令'''
    def __init__(self, guid, name, side_name, category, element_type):
        Element.__init__(self, guid, name, side_name, element_type)
        self._mozi_task = None
        self.doctrine = None
        self.category = category
        self.category_str = selector2str[self.category]

    def get_actions_space(self):
        """
        获取行动空间:
        推演方，任务，编队，实体共用：
        ['deploy_on_attack', 'deploy_on_damage', 'deploy_on_defence', 'deploy_on_fuel','doctrine_SetEMCON_Inherit', 'doctrine_air_operations_tempo',
        'doctrine_automatic_evasion', 'doctrine_engage_opportunity_targets', 'doctrine_engaging_ambiguous_targets', 'doctrine_fuel_state_planned',
        'doctrine_fuel_state_rtb', 'doctrine_gun_strafing', 'doctrine_ignore_emcon_under_attack', 'doctrine_ignore_plotted_course', 'doctrine_switch_radar',
         'doctrine_weapon_control_status_air', 'doctrine_weapon_control_status_land', 'doctrine_weapon_state_planned', 'doctrine_weapon_state_rtb', 'get_actions_space',
          'set_mozi_interface', 'withdraw_on_attack', 'withdraw_on_damage', 'withdraw_on_defence', 'withdraw_on_fuel', 'wra_firing_range', 'wra_qty_salvo',
          'wra_self_defence_distance', 'wra_shooter_salvo']
        推演方：
        ['doctrine_SetEMCON_Inherit']
        :return:
        """
        return []

    def set_mozi_interface(self, mozi_task):
        self._mozi_task = mozi_task

    def get_server_json_data(self, lua_cmd, request_count=loop_request_count):
        """
        传入lua命令，在服务器生成json字符串，返回python结构体
        :param lua_cmd: str, lua命令语句
        :param request_count: int, 调用不成功时的最大调用次数
        :return:
        """
        for i in range(request_count):
            ret_str = self._mozi_task.sendAndRecv(lua_cmd)
            if ret_str.startswith("new exception") or ret_str.startswith("脚本"):
                time.sleep(0.1)
                logging.info("lua execute wrong, lua:%s, return:%s" % (lua_cmd, ret_str))
            else:
                try:
                    return json.loads(ret_str)
                except:
                    traceback.print_exc()
        return None

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

        if self.category == SelectorCategory.Side or self.category == SelectorCategory.Mission:
            id_str = self.name
        else:
            id_str = self.guid

        cmd_str = "ScenEdit_SetEMCON('%s', '%s', '%s')" % (self.category_str, id_str, set_str)
        self._mozi_task.sendAndRecv(cmd_str)

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
        return self._mozi_task.sendAndRecv(cmd)

    def doctrine_engaging_ambiguous_targets(self, towards_ambigous_target):
        """
        接战模糊位置目标
        :param towards_ambigous_target: BehaviorTowardsAmbigousTarget
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                               '{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if towards_ambigous_target.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{engaging_ambiguous_targets=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')
        else:
            if towards_ambigous_target.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engaging_ambiguous_targets=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engaging_ambiguous_targets=' + str(towards_ambigous_target.value) + '}')

    def doctrine_weapon_control_status_air(self, weapon_control_status_airEnum):
        """
        武器控制状态，对空
        :param weapon_control_status_airEnum: WeaponControlStatus, 状态枚举类型
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{weapon_control_status_air=' + str(weapon_control_status_airEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if weapon_control_status_airEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{weapon_control_status_air=\"inherit\"}')
            return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{weapon_control_status_air=' + str(weapon_control_status_airEnum.value) + '}')
        else:
            if weapon_control_status_airEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{weapon_control_status_air=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{weapon_control_status_air=' + str(weapon_control_status_airEnum.value) + '}')

    def doctrine_weapon_control_status_land(self, weapon_control_status_landEnum):
        """
        武器控制状态，对地
        :param weapon_control_status_landEnum:  WeaponControlStatus, 状态枚举类型
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{weapon_control_status_land=' + str(weapon_control_status_landEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if weapon_control_status_landEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{weapon_control_status_land=\"inherit\"}')
            return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{weapon_control_status_land=' + str(weapon_control_status_landEnum.value) + '}')
        else:
            if weapon_control_status_landEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{weapon_control_status_land=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{weapon_control_status_land=' + str(weapon_control_status_landEnum.value) + '}')

    def doctrine_ignore_plotted_course(self, ignore_plotted_courseEnum):
        """
        攻击时忽略计划航线设置
        :param ignore_plotted_courseEnum:IgnorePlottedCourseWhenAttacking，选择枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            if ignore_plotted_courseEnum == IgnorePlottedCourseWhenAttacking.No:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_plotted_course=' + 'false' + '}')
            elif ignore_plotted_courseEnum == IgnorePlottedCourseWhenAttacking.Yes:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_plotted_course=' + 'true' + '}')
        elif self.category == SelectorCategory.Mission:
            if ignore_plotted_courseEnum.value == 0:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_plotted_course=' + 'false' + '}')
            if ignore_plotted_courseEnum.value == 1:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_plotted_course=' + 'true' + '}')
            if ignore_plotted_courseEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_plotted_course=\"inherit\"}')
        else:
            if ignore_plotted_courseEnum == IgnorePlottedCourseWhenAttacking.No:
                return self._mozi_task.sendAndRecv("ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=false})" % self.guid)
                # return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{ignore_plotted_course=' + 'false' + '}')
            elif ignore_plotted_courseEnum == IgnorePlottedCourseWhenAttacking.Yes:
                return self._mozi_task.sendAndRecv("ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=true})" % self.guid)
                # return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{ignore_plotted_course=' + 'true' + '}')
            elif ignore_plotted_courseEnum == IgnorePlottedCourseWhenAttacking.Inherit:
                return self._mozi_task.sendAndRecv("ScenEdit_SetDoctrine({guid='%s'},{ignore_plotted_course=\"inherit\"})" % self.guid)
                # return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                #                                                   '{ignore_plotted_course=\"inherit\"}')

    def doctrine_engage_opportunity_targets(self, engage_opportunity_targetsEnum):
        """
        接战临机出现目标
        :param engage_opportunity_targetsEnum: EngageWithContactTarget, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            if engage_opportunity_targetsEnum == EngageWithContactTarget.No_Only:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{engage_opportunity_targets=' + 'false' + '}')
            elif engage_opportunity_targetsEnum == EngageWithContactTarget.Yes_AnyTarget:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{engage_opportunity_targets=' + 'true' + '}')
        elif self.category == SelectorCategory.Mission:
            if engage_opportunity_targetsEnum == EngageWithContactTarget.No_Only:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{engage_opportunity_targets=' + 'false' + '}')
            elif engage_opportunity_targetsEnum == EngageWithContactTarget.Yes_AnyTarget:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{engage_opportunity_targets=' + 'true' + '}')
            elif engage_opportunity_targetsEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{engage_opportunity_targets=\"inherit\"}')
        else:
            if engage_opportunity_targetsEnum == EngageWithContactTarget.No_Only:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engage_opportunity_targets=' + 'false' + '}')
            elif engage_opportunity_targetsEnum == EngageWithContactTarget.Yes_AnyTarget:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{engage_opportunity_targets=' + 'true' + '}')
            elif engage_opportunity_targetsEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{engage_opportunity_targets=\"inherit\"}')

    def doctrine_ignore_emcon_under_attack(self, ignore_emcon_while_under_attackEnum):
        """
        受到攻击忽略电磁管控
        :param ignore_emcon_while_under_attackEnum: IgnoreEMCONUnderAttack, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            if ignore_emcon_while_under_attackEnum == IgnoreEMCONUnderAttack.No:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_emcon_while_under_attack=' + 'false' + '}')
            elif ignore_emcon_while_under_attackEnum == IgnoreEMCONUnderAttack.Ignore_EMCON_While_Under_Attack:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{ignore_emcon_while_under_attack=' + 'true' + '}')
        elif self.category == SelectorCategory.Mission:
            if ignore_emcon_while_under_attackEnum.value == 0:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_emcon_while_under_attack=' + 'false' + '}')
            if ignore_emcon_while_under_attackEnum.value == 1:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_emcon_while_under_attack=' + 'true' + '}')
            if ignore_emcon_while_under_attackEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{ignore_emcon_while_under_attack=\"inherit\"}')
        elif self.category == SelectorCategory.Unit:
            if ignore_emcon_while_under_attackEnum == IgnoreEMCONUnderAttack.No:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{ignore_emcon_while_under_attack=' + 'false' + '}')
            elif ignore_emcon_while_under_attackEnum == IgnoreEMCONUnderAttack.Ignore_EMCON_While_Under_Attack:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{ignore_emcon_while_under_attack=' + 'true' + '}')
            elif ignore_emcon_while_under_attackEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{ignore_emcon_while_under_attack=\"inherit\"}')

    def doctrine_automatic_evasion(self, automatic_evasionEnum):
        """
        自动规避
        :param automatic_evasionEnum: AutomaticEvasion, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            if automatic_evasionEnum == AutomaticEvasion.No:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{automatic_evasion=' + 'false' + '}')
            elif automatic_evasionEnum == AutomaticEvasion.Yes:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{automatic_evasion=' + 'true' + '}')
        elif self.category == SelectorCategory.Mission:
            if automatic_evasionEnum.value == 0:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}',
                    '{automatic_evasion=' + 'false' + '}')
            if automatic_evasionEnum.value == 1:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{automatic_evasion=' + 'true' + '}')
            if automatic_evasionEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{automatic_evasion=\"inherit\"}')
        else:
            if automatic_evasionEnum == AutomaticEvasion.No:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{automatic_evasion=' + 'false' + '}')
            elif automatic_evasionEnum == AutomaticEvasion.Yes:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{automatic_evasion=' + 'true' + '}')
            elif automatic_evasionEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{automatic_evasion=\"inherit\"}')

    def doctrine_air_operations_tempo(self, air_operations_tempoEnum):
        """
        空战节奏
        :param air_operations_tempoEnum: AirOpsTempo, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{air_operations_tempo=' + str(air_operations_tempoEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if air_operations_tempoEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{air_operations_tempo=\"inherit\"}' )
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{air_operations_tempo='+ str(air_operations_tempoEnum.value)+'}' )
        else:
            if air_operations_tempoEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{air_operations_tempo=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{air_operations_tempo=' + str(air_operations_tempoEnum.value) + '}')

    def doctrine_fuel_state_planned(self, fuel_state_plannedEnum):
        """
        燃油状态，预先规划
        :param fuel_state_plannedEnum: FuelState, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}', '{fuel_state_planned=' + str(fuel_state_plannedEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if fuel_state_plannedEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{fuel_state_planned=\"inherit\"}')
            return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{fuel_state_planned=' + str(fuel_state_plannedEnum.value) + '}')
        else:
            if fuel_state_plannedEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{fuel_state_planned=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{fuel_state_planned=' + str(
                                                                       fuel_state_plannedEnum.value) + '}')

    def doctrine_fuel_state_rtb(self, fuel_state_rtbEnum):
        """
        燃油状态，返航
        :param fuel_state_rtbEnum: FuelStateRTB, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}','{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if fuel_state_rtbEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{fuel_state_rtb=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')
        else:
            if fuel_state_rtbEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{fuel_state_rtb=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                            '{fuel_state_rtb=' + str(fuel_state_rtbEnum.value) + '}')

    def doctrine_weapon_state_planned(self, weapon_state_plannedEnum):
        """
        武器状态，预先规划
        :param weapon_state_plannedEnum:WeaponStatePlanned, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                               '{weapon_state_planned=' + str(weapon_state_plannedEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if weapon_state_plannedEnum.value==999:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{weapon_state_planned=\"inherit\"}' )
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{side="'+self.side_name+'",mission="'+self.name+'"}','{weapon_state_planned='+ str(weapon_state_plannedEnum.value)+'}' )
        else:
            if weapon_state_plannedEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                               '{weapon_state_planned=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{weapon_state_planned=' + str(
                                                                       weapon_state_plannedEnum.value) + '}')

    def doctrine_weapon_state_rtb(self, weapon_state_rtbEnum):
        """
        武器状态-返航
        :param weapon_state_rtbEnum: WeaponStateRTB, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                           '{weapon_state_rtb=' + str(weapon_state_rtbEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if weapon_state_rtbEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{weapon_state_rtb=\"inherit\"}')
            return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{weapon_state_rtb=' + str(weapon_state_rtbEnum.value) + '}')
        else:
            if weapon_state_rtbEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{weapon_state_rtb=\"inherit\"}')
            else:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                                   '{weapon_state_rtb=' + str(
                                                                       weapon_state_rtbEnum.value) + '}')

    def doctrine_gun_strafing(self, gun_strafingEnum):
        """
        空对地扫射
        :param gun_strafingEnum: GunStrafeGroundTargets, 枚举
        :return:
        """
        if self.category == SelectorCategory.Side:
            return self._mozi_task.setconIntendedTargetDoctrine('{side="' + self.side_name + '"}',
                                                           '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
        elif self.category == SelectorCategory.Mission:
            if gun_strafingEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine(
                    '{side="' + self.side_name + '",mission="' + self.name + '"}', '{gun_strafing=\"inherit\"}')
            return self._mozi_task.setconIntendedTargetDoctrine(
                '{side="' + self.side_name + '",mission="' + self.name + '"}',
                '{gun_strafing=' + str(gun_strafingEnum.value) + '}')
        else:
            if gun_strafingEnum.value == 999:
                return self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}','{gun_strafing=\"inherit\"}')
            else:
                self._mozi_task.setconIntendedTargetDoctrine('{guid="' + self.guid + '"}',
                                                            '{gun_strafing=' + str(gun_strafingEnum.value) + '}')

    def wra_qty_salvo(self, weaponID, target_type, select_type):
        """
        武器使用规则--齐射武器数
        :param weaponID: 武器DBID
        :param target_type: WRA_WeaponTargetType
        :param select_type: WRAWeaponQty
        :return:
        """
        if self.category == SelectorCategory.Side:
            ele_type = ElementType.Side
        else:
            ele_type = ElementType.Facility
        target_type = target_type.value
        value_arg = cf.get_weapon_qty_value(ele_type, weaponID, target_type, select_type)
        # logging.info('qty_salvo:%d' % value_arg)
        if self.category == SelectorCategory.Side:
            table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{qty_salvo="%s"})' % (
            self.side_name, weaponID, target_type, value_arg)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{qty_salvo="%s"})' % (
            self.side_name, self.name, weaponID, target_type, value_arg)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{qty_salvo="%s"})' % (
            self.guid, weaponID, target_type, value_arg)
            return self._mozi_task.sendAndRecv(table)

    def wra_shooter_salvo(self, weaponID, target_type, select_type):
        """
        武器使用规则--齐射发射架数
        :param weaponID: 武器DBID
        :param target_type: WRA_WeaponTargetType
        :param select_type: WRAShooterQty
        :return:
        """
        if self.category == SelectorCategory.Side:
            ele_type = ElementType.Side
        else:
            ele_type = ElementType.Facility
        target_type = target_type.value
        select_type = cf.get_shooter_qty_value(ele_type, weaponID, target_type, select_type)
        # logging.info('shooter_salvo:%d' % select_type)
        if self.category == SelectorCategory.Side:
            table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{shooter_salvo="%s"})' % (
            self.side_name, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{shooter_salvo="%s"})' % (
            self.side_name, self.name, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{shooter_salvo="%s"})' % (
            self.guid, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)

    def wra_firing_range(self, weaponID, target_type, select_type):
        """
        武器使用规则 - -自动开火距离
        :param weaponID: 武器DBID
        :param target_type:WRA_WeaponTargetType
        :param select_type: WRASelfAttackRange
        :return:
        """
        if self.category == SelectorCategory.Side:
            ele_type = ElementType.Side
        else:
            ele_type = ElementType.Facility
        target_type = target_type.value
        select_type = cf.get_firing_range_value(ele_type, weaponID, target_type, select_type)
        # logging.info('firing_range:%d' % select_type)
        if self.category == SelectorCategory.Side:
            table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{firing_range="%s"})' % (
            self.side_name, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{firing_range="%s"})' % (
            self.side_name, self.name, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{firing_range="%s"})' % (
            self.guid, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)

    def wra_self_defence_distance(self, weaponID, target_type, select_type):
        """
        武器使用规则--自动防御距离
        :param weaponID: 武器DBID
        :param target_type: WRA_WeaponTargetType
        :param select_type: WRASelfDefenceRange
        :return:
        """
        if self.category == SelectorCategory.Side:
            ele_type = ElementType.Side
        else:
            ele_type = ElementType.Facility
        target_type = target_type.value
        select_type = cf.get_self_defence_value(ele_type, weaponID, target_type, select_type)
        # logging.info('defence_distance:%d' % select_type)
        if self.category == SelectorCategory.Side:
            table = 'HS_SetDoctrineWRA({side="%s", WEAPON_ID="%s" , target_type="%s"},{self_defence="%s"})' % (
            self.side_name, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'HS_SetDoctrineWRA({side="%s", MISSION="%s",WEAPON_ID="%s" , target_type="%s"},{self_defence="%s"})' % (
            self.side_name, self.name, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'HS_SetDoctrineWRA({guid="%s", WEAPON_ID="%s" , target_type="%s"},{self_defence="%s"})' % (
            self.guid, weaponID, target_type, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_damage={}}})'.format(self.side_name,
                                                                                             select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_fuel={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_fuel={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_fuel={}}})'.format(self.side_name, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_fuel={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_fuel={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_attack={}}})'.format(self.side_name,
                                                                                             select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_attack={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_attack={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{withdraw_on_defence={}}})'.format(self.side_name,
                                                                                              select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{withdraw_on_defence={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{withdraw_on_defence={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_damage={}}})'.format(self.side_name, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_damage={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_damage={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_fuel={}}})'.format(self.side_name, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_fuel={}}})'.format(self.side_name,
                                                                                                        self.name,
                                                                                                        select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_fuel={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

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

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_attack={}}})'.format(self.side_name, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_attack={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_attack={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

    def deploy_on_defence(self, select_type):
        """
        满足如下条件时重新部署--主要防御武器处于
        :param select_type: WeaponQuantityThreshold
        :return:
        """
        if select_type.value == 999:
            select_type = '\"inherit\"'
        else:
            select_type = select_type.value

        if self.category == SelectorCategory.Side:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\"}},{{deploy_on_defence={}}})'.format(self.side_name, select_type)
            return self._mozi_task.sendAndRecv(table)
        elif self.category == SelectorCategory.Mission:
            table = 'ScenEdit_SetDoctrine({{side=\"{}\",mission=\"{}\"}},{{deploy_on_defence={}}})'.format(
                self.side_name, self.name, select_type)
            return self._mozi_task.sendAndRecv(table)
        else:
            table = 'ScenEdit_SetDoctrine({{guid=\"{}\",}},{{deploy_on_defence={}}})'.format(self.guid, select_type)
            return self._mozi_task.sendAndRecv(table)

