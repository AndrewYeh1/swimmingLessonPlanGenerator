# GUI imports
from PyQt6.QtWidgets import QFileDialog

# import exporters
from exporters import docs, pdf, word

# import templates
from templates import lessonPlan


class ExportGUI(QFileDialog):
    def __init__(self):
        # calls the super class
        super().__init__()

        # lesson
        self.lesson = None

    def giveLesson(self, lesson: lessonPlan.LessonPlan):
        self.lesson = lesson

    def export(self):
        fileTypes = "Word (*.docx);;PDF (*.pdf)"
        filePath = self.getSaveFileName(self, "Save to file", "New Lesson", fileTypes)
        if filePath[1] == "Word (*.docx)":
            exporter = word.Word(self.lesson, filePath[0])
            exporter.export()
        if filePath[1] == "PDF (*.pdf)":
            pass
