#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : main.py
# Create date : 2019-10-20 19:37
# Modified date : 2020-01-09 19:22
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from __future__ import division

import numpy as np
import gc

from rlmodel.ddpg import train
from rlmodel.ddpg import buffer
from .env import MoziEnv
import pylog

from . import etc
from .pic import write_final_reward
from .pic import write_loss

from .pic import write_file
from .pic import read_file
from .pic import create_needed_folder
from .pic import get_start_epoch
from .pic import get_train_step

from MoziService import MoZiPython
from .test.test01 import *
from .test.mozifun_test import *
from .bt.ctrltree import *
import random
import time

def run(train_step, start_epoch, trainer, ram, env):
    for _ep in range(int(start_epoch), etc.MAX_EPISODES):
        if not env.connect_server():
            pylog.info("can not connect to server")
            return False
        observation = env.reset()
        sum_reward = 0
        for step in range(etc.MAX_STEPS):
            state = np.float32(observation)

            if _ep % 5 == 0:
                action = trainer.get_exploitation_action(state)
            else:
                action = trainer.get_exploration_action(state)

            new_observation, reward, done, info = env.step(action)
            sum_reward += reward

            show_str = "EPISODE:%s step:%s observation:%s action:%s new_observation:%s reward:%s sum_reward:%s" % (
                _ep, step, observation, action, new_observation, reward, sum_reward)
            pylog.info(show_str)

            if done:
                new_state = None
            else:
                new_state = np.float32(new_observation)
                ram.add(state, action, reward, new_state)

            if info:
                pylog.info(info)

            observation = new_observation
            trainer.optimize(train_step)
            train_step += 1
            write_file(train_step, "%s/step.txt" % etc.OUTPUT_PATH)
            if done:
                break

        write_final_reward(sum_reward, _ep)
        gc.collect()
        if _ep % 5 == 0:
            trainer.save_model(_ep, etc.MODELS_PATH)
            write_file(_ep)


def get_ram():
    ram = buffer.MemoryBuffer(etc.MAX_BUFFER)
    return ram

'''
def main():
    create_needed_folder()

    env = MoziEnv(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)
    S_DIM = env.observation_space
    A_DIM = env.action_space
    A_MAX = env.action_max

    start_epoch = get_start_epoch()
    train_step = get_train_step()
    ram = get_ram()

    trainer = train.Trainer(S_DIM, A_DIM, A_MAX, ram, etc.device, write_loss, int(start_epoch), etc.MODELS_PATH)
    run(train_step, start_epoch, trainer, ram, env)
'''
def main():
    '''
    #jkjkjkl
    '''
    env = MoziEnv(etc.SERVER_IP, etc.SERVER_PORT, etc.SCENARIO_NAME, etc.simulate_compression)
    if not env.connect_server():
        return False
    #'''测试服务端发来的数据时，暂时注释掉
    observation = env.reset()
    state = np.float32(observation)
    #'''
    mozi = MoZiPython.MoZi(etc.SERVER_IP, 6260)


    '''
        测试添加飞机
    '''
    #plane01,plane02 = testAddAC(mozi)

    #weather = testGetWeather(mozi)
    '''
            测试行为树案例中与GUID相关的基本函数
    '''
    #btguid,btstamp = testOperateBtGUID(mozi)

    #env.scenario.situation.init_situation(mozi, env.scenario)

    '''
        运行客户端出现目标后
    '''
    #btctctsBox = testContactsBox(env,mozi)

    '''
        客户端设置了任务strike1后
    '''
    #btmssunit = testMission(mozi)

    '''
        测试DetermineUnitRTB：加个机场，选择基地，执行返航
    '''
    #btrtb = testRTB(mozi)

    '''
        测试行为树    
    '''
    #testBT()

    '''
        测试推演方信息获取
    '''
    #rn = env.red_side_name
    #cs, rs = mozi.getSideInfo(rn)
    #ropts = mozi.getSideOptions(rn)

    '''
            测试墨子行为树案例
    '''
    #mozi.sendAndRecv("ScenEdit_DeleteUnit({side='a',guid='47a0620b-f3b5-45c2-b516-c55f82f25255'})")
    '''
    env.mozi_service.run_simulate()
    stop = 0
    t01 = eval(mozi.getCurrentTime())
    merimackSelector = initializeMerimackMonitorAI(mozi, '红方', 0, '')
    while (stop == 0) :
        env.mozi_service.suspend_simulate()
        ###############
        result = updateAI(merimackSelector,mozi,env)
        ################
        t02 = eval(mozi.getCurrentTime())
        if (t02-t01)/3600 > 1 :
            stop = 1
        else:
            print('---'+str(random.random())+'---')
            print((t02-t01)/60)
            env.mozi_service.run_simulate()
            result = testLuaTable2pythonDict_2(mozi)
            for k in result['content']:
                print(result['content'][k])
            time.sleep(3)
    '''


    '''
        测试lua2python的适应性
    '''
    env.mozi_service.run_simulate()
    stop = 0
    t01 = eval(mozi.getCurrentTime())
    merimackSelector = initializeMerimackMonitorAI(mozi, '红方', 0, '')
    while (stop == 0):
        env.mozi_service.suspend_simulate()
        updateAI(merimackSelector, mozi, env)
        t02 = eval(mozi.getCurrentTime())
        if (t02 - t01) / 3600 > 1:
            stop = 1
        else:
            print('---' + str(random.random()) + '---')
            print((t02 - t01) / 60)
            env.mozi_service.run_simulate()
            #############################################
            result = testLuaTable2pythonDict_2(mozi)
            if result != None:
                for k in result['content']:
                    print(result['content'][k])
            ##################################################
            #env.scenario.get_side_byname(env.red_side_name)
            time.sleep(3)
            env.step()
            ############################################
            ### First example to fullfill getting data from situation data source in python terminal.
            #aside = env.scenario.situation.side_dic['31b4fb57-893e-4265-88ac-ced45a58e8a0']
            #acntcts = aside.get_contacts()
            #print(acntcts)
            ############################################
            #aa = test_getScenarioTitle(env)
            #print('The title of this scenario is '+aa)
            #aa = test_getScenarioDescribe(env)
            #print('The scenario is about '+aa)
            #aa = test_getScenarioGetWeather(env)
            #aa_
            #aa = test_Scenario_getCurrentTime(env)
            #print(aa)
            #sidename = '红方'
            #aa = test_Scenario_getSideByName(env,sidename)
            #aa
            #nameOrId = '红方'
            #aa = test_Scenario_getSide(env, nameOrId)
            #aa
            nameOrId = '红方'
            #aa = test_Scenario_getPosture(env, nameOrId)
            #print(aa)
            #acntcts = test_Side_getContacts(env, nameOrId)
            #acntcts
            #test_Side_getContact(env, nameOrId)

            #ascore = test_Side_getScore(env, nameOrId)
            #print(ascore)

            #  测试添加单元
            #a = env.scenario.getSide('红方')
            #a.addAircarft('attack', '316', '768', '32.9', '45.4', '3000.0', '300')
            #a.addAircarft('attack', '316', '768', '32.9', '45.4')
            #a.addAircarft('attack', '7', '14531', '32.9', '45.4', '3000.0')
            #a.addSubmarine('sub1', '23', '29.15', '49.45',300)
            #a.addShip('ship1', '37', 29.16, 49.46, 30)
            #a.addFacility('fac1', 43, 32.4, 45.1, 90)
            print(1)
    mozi.__dict__.update()
    testEnd()


    '''
    测试服务端发来的数据
    '''
    '''
    import json
    mozi.loadScenario('cuss', "false")
    for i in range(30):
        value = mozi.getScenarioIsLoad()
        if str(value) == "'Yes'":
            print("scenario load sucess")
            break
        print("sleep a second")
        time.sleep(1)

    env.mozi_service.suspend_simulate()
    env._set_duration_interval()
    env.mozi_service.set_run_mode()
    env.mozi_service.set_simulate_compression(env.simulate_compression)
    env.mozi_service.set_compression_mode(False)
    mozi_server = env.mozi_service.mozi_task
    load_success = False
    for i in range(20):
        load_result = mozi_server.sendAndRecv("Isload")
        if load_result == "True":
            load_success = True
            break
        time.sleep(1)
    if not load_success:
        print("Interrupted, the situation object can not be created!")
    stop = 0
    while(stop==0):
        #env.mozi_service.suspend_simulate()
        mozi.simStop()
        situation_str = mozi_server.sendAndRecv("GetAllState")
        situation_dict = json.loads(situation_str)
        # env.mozi_service.m
        tt=mozi.getCurrentTime()
        print(tt)
        time.sleep(3)
        #env.mozi_service.run_simulate()
        mozi.simRun()
    '''



main()
