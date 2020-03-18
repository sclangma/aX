# -*- coding:utf-8 -*-
##########################################################################################################
# File name : contact.py
# Create date : 2020-1-8
# Modified date : 2020-1-8
#All rights reserved:北京华戍防务技术有限公司
#Author:xy
##########################################################################################################


class CContact():
    contact_type = {
        # 空中目标
        0: "Air",
        # 导弹
        1: "Missile",
        # 水面 / 地面
        2: "Surface",
        # 潜艇
        3: "Submarine",
        # 未确定的海军
        4: "UndeterminedNaval",
        # 瞄准点？？
        5: "Aimpoint",
        # 轨道目标
        6: "Orbital",
        # 固定设施
        7: "Facility_Fixed",
        # 移动设施
        8: "Facility_Mobile",
        # 鱼雷
        9: "Torpedo",
        # 水雷
        10: "Mine",
        # 爆炸
        11: "Explosion",
        # 不确定
        12: "Undetermined",
        # 空中诱饵
        13: "Decoy_Air",
        # 表面诱饵
        14: "Decoy_Surface",
        # 陆地诱饵
        15: "Decoy_Land",
        # 水下诱饵
        16: "Decoy_Sub",
        # 声纳浮标
        17: "Sonobuoy",
        # 军事设施
        18: "Installation",
        # 空军基地
        19: "AirBase",
        # 海军基地
        20: "NavalBase",
        # 移动集群
        21: "MobileGroup",
        # 激活点：瞄准点
        22: "ActivationPoint",
    }

    def __init__(self, strGuid, mozi_server,situation):
        self.mozi_server = mozi_server
        self.situation = situation
        self.strGuid = strGuid
  

    def get_contact_info(self):
        '''
        获取目标信息字典
        '''
        info_dict = {
            'type': self.get_type_description(),
            'typed': self.m_ContactType,
            'classificationlevel': self.m_IdentificationStatus,
            'name': self.strName,
            'guid': self.m_ActualUnit,
            'latitude': self.dLatitude,
            'longitude': self.dLongitude,
            'altitude': self.fCurrentAltitude_ASL,
            'heading': self.fCurrentHeading,
            'speed': self.fCurrentSpeed,
            'firingAt': [],
            'missile_defence': 0,
            'fromUnits': self.m_DetectionRecord,  # ?
            'fg': self.guid,
        }
        return info_dict
    
    def parse_area(cls, str_area):
        '''
        解析不明目标的区域
        str_area 区域点信息
        '''
        if str_area == "":
            return []
        else:
            areas = []
            points = str_area.split("@")
            for point_content in points:
                values = point_content.split("$")
                areas.append({
                    'latitude': float(values[1]),
                    'longitude': float(values[0]),
                    'altitude': float(values[2])
                })
            return areas    
    
    def contact_drop_target(self,side_name):
        '''
        放弃目标
        不再将所选目标列为探测对象。
        side_name 字符串。推演方名称或 GUID
        Hs_ContactDropTarget('红方','a5561d29-b136-448b-af5d-0bafaf218b3d')
        '''   
        lua_scrpt = "Hs_ContactDropTarget('%s','%s')"%(side_name,self.strGuid)
        self.mozi_server.sendAndRecv(lua_scrpt)
    
    def set_mark_contact(self,side_name,contact_type):
        '''
        标识目标立场
        side_name 字符串。推演方名称或 GUID
        ContactType：字符串。目标立场类型（'F'：友方，'N'：中立，'U'：非友方，'H'：敌方）
        Hs_SetMarkContact('红方','a5561d29-b136-448b-af5d-0bafaf218b3d','F')
        '''
        lua_scrpt = "Hs_SetMarkContact('%s','%s','%s')"%(side_name,self.strGuid,contact_type)
        self.mozi_server.sendAndRecv(lua_scrpt)
           
    