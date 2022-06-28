from templates import lessonPlan

# import file managers
import json


def load(filePath):
    file = open(filePath, 'r')
    fileDict = json.load(file)
    file.close()
    lesson = lessonPlan.LessonPlan()
    lesson.importJson(fileDict)
    return lesson
