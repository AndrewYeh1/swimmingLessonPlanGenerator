import PyPDF4


class PDF:
    def __init__(self, activityList):
        self.activityList = activityList
        self.pdf = PyPDF4.PdfFileWriter()

    def export(self):
        pass

    def setFilePath(self):
        pass

    def setList(self):
        pass
