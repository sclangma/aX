# -*- coding:utf-8 -*-
import MoziService.MoZiPython as MoZiPython
import pylog
import time
# from MoziService.entitys.scenario import Scenario
from MoziService.entitys.scenario import CScenario
from websocket import create_connection
import json

from MoziService import situation_paser


def get_red_missile_info(all_info_dict):
    red_missile_info = {}
    red_missile_guid = []
    for guid in list(all_info_dict.keys()):
        item = all_info_dict[guid]
        if item["ClassName"] == "CAircraft":
            red_missile_guid.append(guid)
            red_missile_info[guid] = item
    return red_missile_info


class MoziService():
    """类功能说明"""

    def __init__(self, server_ip, port, scenario_name='', compression=5, continuous=False, connect_mode=1):
        """两个数字相加，并返回结果"""
        self.connect_mode = connect_mode
        self.mozi_task = None
        self.server_ip = server_ip
        self.server_port = port
        self.scenario_name = scenario_name
        self.compression = compression
        self.continuous = continuous
        self.websocket_connect = None
        self.all_guid = []
        self.all_info_dict = {}
        # self.red_info_dict = {}

    def load_scenario(self, plat="windows"):
        '''
        加载想定
        plat 服务器是Windows版还是Linux版
        '''

        scenario_file = self.scenario_name
        if plat == "windows":
            ret = self.mozi_task.scenEditLoadScenario(scenario_file, "false")
        else:
            ret = self.mozi_task.loadScenario(scenario_file, "Play")
        load_success = False
        for i in range(30):
            value = self.mozi_task.getScenarioIsLoad()
            if str(value) == "'Yes'":
                pylog.info("scenario load sucess")
                load_success = True
                break
            pylog.info("sleep a second")
            time.sleep(1)

        if not load_success:
            pylog.error("can not load scenario:%s" % scenario_file)
            return None
        scenario = CScenario(self.mozi_task)
        return scenario

    def update_class_dic(self, class_dic, item, key="ClassName"):
        '''
        
        '''
        # pylog.info(item)
        # pylog.info(key)
        ret = class_dic.get(item[key], "")

        if ret:
            ret.append(item)
        else:
            lt = []
            lt.append(item)
            class_dic[item[key]] = lt

    def paser_situation(self):
        '''
        
        '''
        situation_paser.paser_situation(self.all_info_dict)

    def get_entity(self, guid):
        '''
        
        '''
        return situation_paser.get_entity_from_guid(guid, self.all_info_dict, self.mozi_task)

    def init_situation(self, scenario):
        '''
        初始化态势
        '''
        scenario.situation.init_situation(self.mozi_task, scenario)
        self.all_guid = scenario.situation.all_guid
        self.all_info_dict = scenario.situation.all_info_dict
        # self.paser_situation()

    def show_side_info(self, item):
        '''
        show side info
        '''
        count = 0
        for key in item:
            pylog.info("count:%s %s:%s" % (count, key, item[key]))
            count += 1

    def update_situation(self, scenario):
        """
        更新态势
        :return:
        """
        situation_data = scenario.situation.update_situation(self.mozi_task, scenario)
        situation_paser.update_situation(situation_data, self.all_info_dict)

    def connect_mozi_server(self, websocket_server, websocket_port):
        """
        连接墨子服务器
        param ： 
        websocket_server 要连接的服务器的ip
        websocket_port 要连接的服务器的端口
        :return:
        """
        pylog.info("connect_mozi_server")
        if self.connect_mode == 1:
            self.mozi_task = MoZiPython.MoZi(self.server_ip, self.server_port)
            #
            self.ai_server = self.server_ip
            self.ai_port = self.server_port
            return True
        #
        # server_address = r"ws://%s:%d/websocket" % ('60.205.207.206', 9998)
        server_address = r"ws://%s:%d/websocket" % (websocket_server, websocket_port)
        pylog.info(server_address)
        for i in range(10):
            try:
                self.websocket_connect = create_connection(server_address)
                break
            except:
                pylog.info("can not connect to %s." % server_address)
                time.sleep(2)
                self.websocket_connect = None
        #
        if self.websocket_connect is None:
            pylog.warning("Interrupted, can not connect to %s." % server_address)
            return False
        #
        self.websocket_connect.send("{\"RequestType\":\"StartServer\"}")
        result = self.websocket_connect.recv()
        print("connect server result:%s" % result)
        jsons = json.loads(result)
        self.ai_server = jsons['IP']
        self.ai_port = jsons['AIPort']
        self.mozi_task = MoZiPython.MoZi(self.ai_server, self.ai_port)
        #
        # if platform.system() != 'Darwin':
        ## 修改客户端配置文件
        # inipath = self.client_path_init
        # conf = configparser.ConfigParser()
        # conf.read(inipath)
        # conf.set('ConnectServer', "ip", jsons['IP'])
        # conf.write(open(inipath, "r+"))
        # conf.set('ConnectServer', "port", str(jsons['Port']))
        # conf.write(open(inipath, "r+"))
        # conf.set('ConnectServer', "name", str(jsons['Federate']))
        # conf.write(open(inipath, "r+"))
        #
        return True

    def get_current_time(self):
        '''
        得到当前时间
        param :
        
        return : 时间毫秒值
        '''
        lua = "ReturnObj(ScenEdit_CurrentTime())"
        ret_time = self.mozi_task.sendAndRecv(lua)
        pylog.info("%s\n" % ret_time)
        return ret_time

    def run_simulate(self):
        '''
        设置环境启动
        param :
        return : lua执行成功/lua执行失败
        '''
        lua_str = "ReturnObj(Hs_SimRun(true))"
        ret = self.mozi_task.sendAndRecv(lua_str)
        return ret

    def set_simulate_compression(self, n_compression=4):
        '''
        设置想定推演倍速
        param ：
        
        return ： lua执行成功/lua执行失败
        '''
        lua_str = "ReturnObj(Hs_SetSimCompression(%d))" % n_compression
        ret = self.mozi_task.sendAndRecv(lua_str)
        return ret

    def set_compression_mode(self, b_mode):
        '''
        设置想定推演模式
        param： 
        b_mode ：想定模式（推演模式/编辑模式）
        '''
        lua_str = "Hs_SetSimMode(%s)" % str(b_mode).lower()
        ret = self.mozi_task.sendAndRecv(lua_str)
        return ret

    def set_run_mode(self):
        '''
        设置运行模式，智能体决策想定是否暂停
        
        '''
        if self.continuous:
            return self.mozi_task.sendAndRecv("SETPYTHONMODEL(FALSE)")
        else:
            return self.mozi_task.sendAndRecv("SETPYTHONMODEL(TRUE)")

    def suspend_simulate(self):
        '''
        设置环境暂停
        param ：
        
        return ：
        '''
        lua_str = "Hs_SimStop()"
        self.mozi_task.sendAndRecv(lua_str)

    def get_all_units_info_from_list(self, unit_list):
        '''
        获取所有单元详细信息
        param
        unit_list ： 所有单元集合
        return ： 单元详细信息集合
        '''
        if unit_list:
            unit_info_dic_list = []
            for i in range(len(unit_list)):
                lua_str = """
                unit = ScenEdit_GetUnit({guid='%s'})
                print(unit)
                """ % unit_list[i]["guid"]

                pylog.debug(lua_str, "./cmd_lua/log_lua")
                unit_info = self.mozi_task.sendAndRecv(lua_str)
                pylog.debug(unit_info, "./cmd_lua/log_lua")

                dic = self.paser_unit_info(unit_info)
                if dic and dic["name"] != "Pr.2235.0 “戈尔什科夫海军元帅”级护卫舰":
                    unit_info_dic_list.append(dic)

            return unit_info_dic_list
        else:
            return []

    def paser_unit_info(unit_info):
        '''
        解析单元信息        
        param ：
        unit_info ： 单元信息集合
        return ： 单元字典
        '''
        # pylog.info(unit_str)
        start_index = 0
        end_index = 0
        for i in range(len(unit_info)):
            if unit_info[i] == "{":
                start_index = i
            elif unit_info[i] == "}":
                end_index = i
        con = unit_info[start_index + 1: end_index]
        # pylog.info(con)
        lt = con.split("',")
        # pylog.info(lt)
        dic = {}
        for i in range(len(lt)):
            item = lt[i].strip()
            if item != "":
                item_lt = item.split("=")
                # pylog.info(item_lt)
                dic[item_lt[0].strip()] = item_lt[1].replace("'", "").replace('"', "").strip()

        return dic

    def taishi_reset(self):
        '''
        态势重置函数
        '''
        self._reset()
        time.sleep(3)
        step_interval = 30
        pylog.info("Hs_OneTimeStop:%d" % step_interval)
        self.mozi_task.sendAndRecv("Hs_OneTimeStop('Stop', %d)" % step_interval)
        self.run_simulate()
        self.create_get_situation_process()
        self.step()
