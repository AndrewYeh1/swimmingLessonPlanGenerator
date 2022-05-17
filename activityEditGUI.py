# import constant
import constant

# import template
import activityTemplates

# partial for callback
from functools import partial

# gui imports
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QThread, QModelIndex
from PyQt6.QtWidgets import (QWidget,  # window
                             QPushButton, QLabel,  # buttons and labels
                             QLineEdit, QTextEdit,  # inputs
                             QTabWidget,  # tabs
                             QScrollArea,  # scroll
                             QFrame,  # frame
                             QInputDialog,  # dialog box
                             QComboBox,  # drop down menu
                             QTreeWidget, QTreeWidgetItem,  # treeview
                             QCheckBox,  # checkbox
                             QVBoxLayout, QHBoxLayout, QGridLayout,)  # layout management


class ActivityEdit(QWidget):
    def __init__(self, deleteCallback, confirmCallback, activity, name, *args, **kwargs):
        # constants
        TYPES = ["4Ds", "Discovery", "Game"]

        # calls the super class
        super().__init__(*args, **kwargs)

        # callback function
        self.deleteCallback = deleteCallback
        self.confirmCallback = confirmCallback

        # main frame
        self.mainFrame = QFrame()
        self.mainFrame.setFrameStyle(QFrame.Shape.StyledPanel)

        # main hbox
        self.mainHBox = QHBoxLayout()

        # creates the buttons and input fields
        self.detailedViewVBox = QVBoxLayout()
        self.detailedViewNameHBox = QHBoxLayout()
        self.detailedViewTimeHBox = QHBoxLayout()
        self.detailedViewTypeHBox = QHBoxLayout()
        self.detailedViewActivityHBox = QHBoxLayout()
        self.detailedViewDescriptionHBox = QHBoxLayout()
        self.detailedViewName = QLineEdit()
        self.detailedViewNameLabel = QLabel("Name:")
        self.detailedViewTime = QLineEdit()
        self.detailedViewTimeLabel = QLabel("Time (min):")
        self.detailedViewType = QComboBox()
        self.detailedViewTypeLabel = QLabel("Type:")
        self.detailedViewActivity = QComboBox()
        self.detailedViewActivityLabel = QLabel("Activity:")
        self.detailedViewDescription = QTextEdit()
        self.detailedViewDescriptionLabel = QLabel("Notes:")

        # sets up the combo boxes
        self.detailedViewType.addItems(TYPES)

        # bottom bar
        self.bottomBarHBox = QHBoxLayout()
        self.bottomBarGrid = QGridLayout()
        self.bottomBarVBox = QVBoxLayout()
        self.detailedViewAll = QCheckBox("All")
        self.detailedViewSKSelection = []
        for i in range(1, 11):
            self.detailedViewSKSelection.append(QCheckBox(f"SK{i}"))
            self.detailedViewSKSelection[i - 1].clicked.connect(self.checkForAll)
            self.bottomBarGrid.addWidget(self.detailedViewSKSelection[i - 1], (i - 1) % 3, (i - 1) // 3)
        self.bottomBarGrid.addWidget(self.detailedViewAll, 2, 3)
        self.collapseBtn = QPushButton("Confirm")
        self.deleteBtn = QPushButton("Delete")
        self.collapseBtn.clicked.connect(self.callback)
        self.deleteBtn.clicked.connect(self.delete)
        self.detailedViewAll.clicked.connect(self.all)
        self.bottomBarVBox.addWidget(self.collapseBtn)
        self.bottomBarVBox.addWidget(self.deleteBtn)
        self.bottomBarHBox.addLayout(self.bottomBarGrid)
        self.bottomBarHBox.addLayout(self.bottomBarVBox)

        # checks the boxes that are valid
        self.setChecked(activity.level)
        self.checkForAll()

        # adds buttons and input fields to the vbox
        self.detailedViewVBox.addLayout(self.detailedViewNameHBox)
        self.detailedViewNameHBox.addWidget(self.detailedViewNameLabel, 1)
        self.detailedViewNameHBox.addWidget(self.detailedViewName, 9)
        self.detailedViewVBox.addLayout(self.detailedViewTimeHBox)
        self.detailedViewTimeHBox.addWidget(self.detailedViewTimeLabel, 1)
        self.detailedViewTimeHBox.addWidget(self.detailedViewTime, 9)
        self.detailedViewVBox.addLayout(self.detailedViewTypeHBox)
        self.detailedViewTypeHBox.addWidget(self.detailedViewTypeLabel, 1)
        self.detailedViewTypeHBox.addWidget(self.detailedViewType, 9)
        self.detailedViewVBox.addLayout(self.detailedViewActivityHBox)
        self.detailedViewActivityHBox.addWidget(self.detailedViewActivityLabel, 1)
        self.detailedViewActivityHBox.addWidget(self.detailedViewActivity, 9)
        self.detailedViewVBox.addLayout(self.detailedViewDescriptionHBox)
        self.detailedViewDescriptionHBox.addWidget(self.detailedViewDescriptionLabel, 1)
        self.detailedViewDescriptionHBox.addWidget(self.detailedViewDescription, 9)
        self.detailedViewVBox.addLayout(self.bottomBarHBox)

        # adds in frame
        self.mainFrame.setLayout(self.detailedViewVBox)
        self.mainHBox.addWidget(self.mainFrame)

        # sets its own layout
        self.setLayout(self.mainHBox)

        # fills in the input boxes if there is data
        if name is not None:
            self.detailedViewName.setText(name)
        if activity.time is not None:
            self.detailedViewTime.setText(str(activity.time))
        if activity.tp is not None:
            self.detailedViewType.setCurrentIndex(TYPES.index(activity.tp))
        if activity.activity is not None:
            self.detailedViewActivity.setCurrentText(activity.activity)

    def callback(self):
        # extracts data from input fields
        activity = self.detailedViewActivity.currentText()
        name = self.detailedViewName.text()
        time = int(self.detailedViewTime.text())
        level = self.returnChecked()
        if self.detailedViewType.currentText() == "4Ds":
            tp = 1
        elif self.detailedViewType.currentText() == "Discovery":
            tp = 2
        else:
            tp = 3
        instructions = self.detailedViewDescription.toPlainText().split("\n")
        activityToReturn = activityTemplates.Template(activity=activity, time=time, level=level, tp=tp, description=instructions)
        partial(self.confirmCallback, activityToReturn, name)()
        # noinspection PyTypeChecker
        self.setParent(None)

    def delete(self):
        self.deleteCallback()

    def returnChecked(self):
        checkedList = []
        for i, box in enumerate(self.detailedViewSKSelection):
            if box.isChecked():
                checkedList.append(i + 1)
        return checkedList

    def setChecked(self, checked: list):
        for i in checked:
            if type(i) == str:
                i = int(i[-1])
            i = i - 1
            self.detailedViewSKSelection[i].setChecked(True)

    def all(self):
        if self.detailedViewAll.isChecked():
            for i in self.detailedViewSKSelection:
                i.setChecked(True)
        else:
            for i in self.detailedViewSKSelection:
                i.setChecked(False)
        self.createActivityList()

    def checkForAll(self):
        checkedList = [i.isChecked() for i in self.detailedViewSKSelection]
        if all(checkedList):
            self.detailedViewAll.setChecked(True)
        else:
            self.detailedViewAll.setChecked(False)
        self.createActivityList()

    def createActivityList(self):
        checkedList = [i.isChecked() for i in self.detailedViewSKSelection]
        ls = []
        for index, item in enumerate(checkedList):
            if item:
                for i in constant.SWIMKIDSSKILLS[f"Swim kids {index + 1}"].keys():
                    ls.extend(constant.SWIMKIDSSKILLS[f"Swim kids {index + 1}"][i].keys())
        ls = sorted(list(dict.fromkeys(ls)))
        self.setActivityOptions(ls)

    def setActivityOptions(self, ls):
        self.detailedViewActivity.clear()
        self.detailedViewActivity.addItems(ls)
