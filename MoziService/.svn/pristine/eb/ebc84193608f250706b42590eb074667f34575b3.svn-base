# -*- coding:utf-8 -*-

import time
import json
import traceback
from abc import ABCMeta, abstractmethod

from MoziService.entitys.global_util import *


class Element(object):
    __metaclass__ = ABCMeta

    """
    元素类 飞机，舰船等作战单元，武器、传感器、天气实体，触发器对象等的基类
    """
    def __init__(self, guid, name, side_name, element_type):
        self.guid = guid
        self.name = name
        self.side_name = side_name
        self.type = element_type

    def delete_sub_object(self):
        """
        当删除本元素时，删除子对象
        返回需要先删除的子对象guid列表
        :return:
        """
        return []


