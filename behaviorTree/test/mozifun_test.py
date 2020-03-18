def test_getScenarioTitle(env):
    return env.scenario.getTitle()

def test_getScenarioDescribe(env):
    return env.scenario.getDescription()

def test_getScenarioGetWeather(env):
    return env.scenario.getWeather()

def test_Scenario_getCurrentTime(env):
    return env.scenario.getCurrentTime()

def test_Scenario_getSideByName(env,sidename):
    return env.scenario.getSideByName(sidename)

def test_Scenario_getSide(env,nameOrId):
    return env.scenario.getSide(nameOrId)

def test_Scenario_getPosture(env,nameOrId):
    return env.scenario.getPosture(nameOrId)

def test_Side_getContacts(env,sideNameOrId):
    a = env.scenario.getSide(sideNameOrId)
    b = a.getContacts()
    return b

def test_Side_getContact(env,sideNameOrId):
    a = env.scenario.getSide(sideNameOrId)
    b = a.getContacts()
    for k in b.keys():
        print(a.getContact(k).strName)

def test_Side_getScore(env,sideNameOrId):
    a = env.scenario.getSide(sideNameOrId)
    a.scenEdit_SetScore(340)
    # Score is to be changed in the next cycle.
    b = a.getScore()
    return b

'''
ffs = 'local a = 1100 \r\n' \
      'ScenEdit_SetScore("红方",a)'
#ffs='ScenEdit_SetScore("红方",1000)'

ffs = '''
#local a = 1100
'ScenEdit_SetScore("红方",a)'
'''
env.mozi_service.mozi_task.sendAndRecv(ffs)

'''
