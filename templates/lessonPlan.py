# import json
import json

# import templates
from templates import activityTemplates


class LessonPlan:
    def __init__(self, dayList=None, wsi="", course="", location="", dateList=None):
        self.wsi = wsi
        self.course = course
        self.location = location
        if dayList is None:
            self.dayList = {}
        else:
            self.dayList = dayList
        if dateList is None:
            self.dateList = {}
        else:
            self.dateList = dateList

    def getTotalTime(self, day):
        totalTime = 0
        for activity in self.dayList[day]:
            totalTime += activity.time
        return totalTime

    def getActivityAmt(self):
        activityDict = {}
        for day in self.dayList:
            for activity in self.dayList[day]:
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
        jsonDayDict = {}
        for i in self.dayList.items():
            jsonDayDict[i[0]] = []
            for j in i[1]:
                jsonDayDict[i[0]].append(j.toDict())
        jsonDict = {
            "wsi": self.wsi,
            "course": self.course,
            "location": self.location,
            "dayList": jsonDayDict
        }
        jsonString = json.dumps(jsonDict)
        return jsonString

    def importJson(self, jsonDict):
        self.wsi = jsonDict["wsi"]
        self.course = jsonDict["course"]
        self.location = jsonDict["location"]
        for i in jsonDict["dayList"].items():
            self.dayList[int(i[0])] = []
            for j in i[1]:
                activity = activityTemplates.Template()
                activity.importDict(j)
                self.dayList[int(i[0])].append(activity)
