from ..entitys.activeunit import CActiveUnit


class CNoNavZone():
    def __init__(self, strGuid, mozi_server, situation):
        self.strGuid = strGuid
        self.mozi_server = mozi_server
        self.situation = situation