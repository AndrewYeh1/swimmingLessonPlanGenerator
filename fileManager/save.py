from templates import lessonPlan


def save(lesson: lessonPlan, filePath):
    file = open(filePath, 'w')
    file.write(lesson.toJson())
    file.close()
