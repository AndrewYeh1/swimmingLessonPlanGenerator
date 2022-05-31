# import json
import json

# import templates
from templates import activityTemplates


class LessonPlan:
    def __init__(self, dayList=None, wsi="", course="", location=""):
        self.wsi = wsi
        self.course = course
        self.location = location
        if dayList is None:
            self.dayList = []
        else:
            self.dayList = dayList

    def getPreview(self):
        pass

    def getActivityAmt(self):
        activityDict = {}
        for day in self.dayList:
            for activity in day:
                if activity.activity not in activityDict:
                    activityDict[activity.activity] = 1
                else:
                    activityDict[activity.activity] += 1
        return activityDict

    def getAllActivities(self):
        activityList = []
        for day in self.dayList:
            for activity in day:
                if activity.name not in [i.name for i in activityList]:
                    activityList.append(activity)
        return activityList

    def toJson(self):
        jsonDayList = []
        for i, day in enumerate(self.dayList):
            jsonDayList.append([])
            for activity in day:
                jsonDayList[i].append(activity.toDict())
        jsonDict = {
            "wsi": self.wsi,
            "course": self.course,
            "location": self.location,
            "dayList": jsonDayList
        }
        jsonString = json.dumps(jsonDict)
        return jsonString

    def importJson(self, jsonDict):
        self.wsi = jsonDict["wsi"]
        self.course = jsonDict["course"]
        self.location = jsonDict["location"]
        for i, day in enumerate(jsonDict["dayList"]):
            self.dayList.append([])
            for activityDict in day:
                activity = activityTemplates.Template()
                activity.importDict(activityDict)
                self.dayList[i].append(activity)
