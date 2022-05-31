# GUI imports
from PyQt6.QtWidgets import QFileDialog

# import exporters
from templates import lessonPlan


class SaveGUI(QFileDialog):
    def __init__(self):
        # calls the super class
        super().__init__()

        # lesson
        self.lesson = None

    def giveLesson(self, lesson: lessonPlan.LessonPlan):
        self.lesson = lesson

    def save(self):
        fileTypes = "LP (*.lspn)"
        filePath = self.getSaveFileName(self, "Save Lesson Plan", "New Lesson Plan", fileTypes)
        if filePath[0] != '':
            file = open(filePath[0], 'w')
            file.write(self.lesson.toJson())
            file.close()
