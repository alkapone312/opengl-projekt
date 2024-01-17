class LightPool:
    def __init__(self, dirLights = [], pointLights = [], spotLights = []):
        self.dirLights = dirLights
        self.pointLights = pointLights
        self.spotLights = spotLights

    def getDirLights(self):
        return self.dirLights
    
    def getPointLights(self):
        return self.pointLights
    
    def getSpotLights(self):
        return self.spotLights