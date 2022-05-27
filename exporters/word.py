import docx
from docx.enum.table import WD_TABLE_ALIGNMENT

from templates import lessonPlan


class Word:
    def __init__(self, plan: lessonPlan):
        self.plan = plan
        self.doc = docx.Document()

    def export(self):
        # creates table
        table = self.doc.add_table(rows=3, cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = "Table Grid"

        # generate header
        courseCell = table.cell(0, 0).merge(table.cell(0, 1))
        courseCell.text = self.plan.course
        # exports the word document
        self.doc.save("test.docx")

    def setFilePath(self):
        pass

    def setList(self):
        pass
