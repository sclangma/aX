# by aie

#upvalues: mozi, env
#need to use mozi
#need to use env
from behaviorTree.bt.basic import *
from behaviorTree.bt.detail import *

def OffensiveConditionalCheck(mozi,env):
    redside = env.scenario.getSide(env.red_side_name)
    contactstotal = redside.getContacts().__len__()
    unitstotal = redside.getAircrafts().__len__()
    if contactstotal == 0:
        return False
    if contactstotal <= unitstotal:
        return True
    else:
        return False

def addAircraftAction(mozi,env):
    redside = env.scenario.getSide(env.red_side_name)
    contactstotal = redside.getContacts().__len__()
    if contactstotal == 0:
        return False
    ac = redside.prepAircraft()
    ac.strName = 'attack'
    ac.iDBID = 316
    ac.iLoadoutDBID = 768
    ac.dLatitude = 32.9
    ac.dLongitude = 45.4
    ac.fCurrentHeading = 300
    ac.fCurrentAlt = 3000.0
    redside.addAircraft(ac)
    return True

def attackMissionCreateAction(mozi,env):
    redside = env.scenario.getSide(env.red_side_name)

    contacts = redside.getContacts()
    airs = redside.getAircrafts()
    if len(contacts)==0 or len(airs)==0 :
        return False
    targets = {k:v for k,v in contacts.items() if k==sorted(contacts)[0]}
    redside.setMarkContacts(targets, 'U')

    strkmssn = redside.prepStirkeMission()
    strkmssn.strName = 'strike2'
    strkmssn.m_Category = 'land'
    mssnSitu = redside.getStrikeMssns()
    if {k:v for k,v in mssnSitu.items() if v.strName=='strike2'}.__len__() == 0:
        redside.addStrikeMission(strkmssn)
    strkmssn.assignTargets(targets)
    airs = redside.getAircrafts()
    strkmssn.assignUnits(airs)

def attackMissionUpdateAction(mozi,env):
    redside = env.scenario.getSide(env.red_side_name)
    airs = redside.getAircrafts()
    airsOnMssn = {k:v for k,v in airs.items() if v.strActiveUnitStatus.find('正在执行任务')>0}
    contacts = redside.getContacts()
    if airsOnMssn.__len__()==0:
        return False
    if len(contacts) == 0 or len(airs) == 0:
        return False
    target =contacts[sorted(contacts)[0]]
    m = 0
    for k,v in airsOnMssn.items() :
        dist = redside.getRange(v,target)
        if dist < 30 :
            v.switchRadar('Active')
        else:
            m = m+1

    if m == airsOnMssn.__len__():
        return False
    else:
        return True

