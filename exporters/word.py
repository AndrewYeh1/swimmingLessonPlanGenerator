import docx
from docx.shared import Inches


class Word:
    def __init__(self, activityList):
        self.activityList = activityList
        self.doc = docx.Document()

    def export(self):
        table = self.doc.add_table(rows=1, cols=4)
        table.autofit = False
        table.style = "Table Grid"
        # generate header
        cell = table.cell(0, 0)
        cell.text = "Hello"
        cell = table.cell(0, 1)
        cell.text = "Hi"
        # exports the word document
        self.doc.save("test.docx")

    def setFilePath(self):
        pass

    def setList(self):
        pass
