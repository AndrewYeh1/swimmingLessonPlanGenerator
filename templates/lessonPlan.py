# import templates
from templates import activityTemplates

# import file exporters
from exporters import docs, word


class LessonPlan:
    def __init__(self, dayList=None):
        if dayList is None:
            self.dayList = []
        else:
            self.dayList = dayList

    def exportToWord(self):
        wordExporter = word.Word(self.dayList)
        wordExporter.export()

    def exportToDocs(self):
        pass

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
