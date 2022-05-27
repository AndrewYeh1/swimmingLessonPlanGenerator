# import templates
from templates import activityTemplates


class LessonPlan:
    def __init__(self, dayList=None, wsi="", date="", course="", location="", time=60, lessonNum=0):
        self.wsi = wsi
        self.date = date
        self.course = course
        self.location = location
        self.time = time
        self.lessonNum = lessonNum
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
                if activity[1].activity not in activityDict:
                    activityDict[activity[1].activity] = 1
                else:
                    activityDict[activity[1].activity] += 1
        return activityDict
