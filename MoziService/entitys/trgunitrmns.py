from ..entitys.activeunit import CActiveUnit


class CTriggerUnitRemainsInArea():
    def __init__(self, strGuid, mozi_server, situation):
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation