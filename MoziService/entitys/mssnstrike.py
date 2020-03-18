from ..entitys.activeunit import CActiveUnit


class CStrikeMission():
    def __init__(self, strGuid, mozi_server, situation):
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation
        self.strName = None
        self.m_Side = None
        self.m_Category = None
        self.m_MissionClass = None
        self.m_StartTime = None
        self.m_EndTime = None
        self.m_MissionStatus = None
        self.m_AssignedUnits = None
        self.m_UnassignedUnits = None
        self.m_StrikeType = None
        self.m_MinimumContactStanceToTrigger = None
        self.m_FlightSize = None
        self.m_Bingo = None
        self.m_MinAircraftReq_Strikers = None
        self.iMinResponseRadius = None
        self.iMaxResponseRadius = None
        self.m_RadarBehaviour = None
        self.bUseRefuel = None
        self.m_UseRefuel = None
        self.bUseFlightSizeHardLimit = None
        self.bUseAutoPlanner = None
        self.bOneTimeOnly = None
        self.m_GroupSize = None
        self.bUseGroupSizeHardLimit = None
        self.bPrePlannedOnly = None
        self.m_Doctrine = None
        self.m_SpecificTargets = None
        self.m_strSideWayGUID = None
        self.m_strSideWeaponWayGUID = None
        self.m_EscortFlightSize = None
        self.m_MinAircraftReqEscorts = None
        self.m_MaxAircraftToFlyEscort = None
        self.iEscortResponseRadius = None
        self.m_EscortFlightSizeNo = None
        self.m_MinAircraftReqEscortsNo = None
        self.m_MaxAircraftToFlyEscortNo = None
        self.bUseFlightSizeHardLimitEscort = None
        self.m_EscortGroupSize = None
        self.bUseGroupSizeHardLimitEscort = None
        self.m_Doctrine_Escorts = None
        self.m_strContactWeaponWayGuid = None
        self.iEmptySlots = None



    def assignTargets(self,targets):
        trgts = "{'"
        for k in targets.keys():
            trgts = trgts + k + "','"
        trgts = trgts + '}'
        trgts = trgts.replace(",'}", '}')
        cmd = "ScenEdit_AssignUnitAsTarget({}, '{}')".format(trgts,self.strName)
        self.situation.throwIntoPool(cmd)
        return self.mozi_server.sendAndRecv(cmd)

    def assignUnits(self,units):
        results = ''
        for k,v in units.items():
            cmd = "ScenEdit_AssignUnitToMission('{}', '{}')".format(v.strGuid, self.strName)
            self.situation.throwIntoPool(cmd)
            ret = self.mozi_server.sendAndRecv(cmd)
            results = results + ',' + ret

        return results


    def assignUnit(self):
        1
