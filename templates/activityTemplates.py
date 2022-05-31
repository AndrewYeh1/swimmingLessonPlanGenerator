from internalData import constant


class Template:
    def __init__(self, name="", activity=None, time=0, level=None, tp=1, description=None):
        self.name = name
        self.activity = activity
        self.time = time
        if level is None:
            self.level = []
        else:
            self.level = level
        self.tp = constant.TYPE[tp]
        if description is None:
            self.description = []
        else:
            self.description = description

    def getSteps(self):
        return self.description

    def addSteps(self, step: str):
        self.description.append(step)

    def removeStep(self, index=-1):
        self.description.pop(index)

    def validForLevel(self, level):
        return level in self.level

    def toDict(self):
        return {
            "name": self.name,
            "activity": self.activity,
            "time": self.time,
            "level": self.level,
            "tp": self.tp,
            "description": self.description
        }

    def importDict(self, activityDict):
        self.name = activityDict["name"]
        self.activity = activityDict["activity"]
        self.time = activityDict["time"]
        self.level = activityDict["level"]
        self.tp = activityDict["tp"]
        self.description = activityDict["description"]
