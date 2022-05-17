# import constant
import constant

# import data
import data

# PyQt6 gui imports
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QThread, QModelIndex
from PyQt6.QtWidgets import (QWidget,  # window
                             QPushButton, QLabel,  # buttons and labels
                             QLineEdit, QPlainTextEdit,  # inputs
                             QTabWidget,  # tabs
                             QScrollArea,  # scroll
                             QFrame,  # frame
                             QInputDialog,  # dialog box
                             QComboBox,  # drop down menu
                             QTreeWidget, QTreeWidgetItem,  # treeview
                             QCheckBox,  # checkbox
                             QSplitter,  # advanced layout management
                             QMenu, QMenuBar,  # top bar
                             QVBoxLayout, QHBoxLayout, QGridLayout,)  # layout management

# widgets
import activityEditGUI
import activityViewGUI
import activityPanelGUI

# import exporters
import lessonPlan


class MainWindow(QWidget):
    def __init__(self, app):
        # calls the super class
        super().__init__()

        # variables
        self.selectedActivity = None

        # constants
        TITLE = "City of edmonton lesson plan generator"

        # gets the app for further use
        self.app = app

        # sets the window title
        self.setWindowTitle(TITLE)

        # main body hbox and splitter
        self.mainBodyHBox = QHBoxLayout()
        self.mainBodySplitter = QSplitter()
        self.mainBodyHBox.addWidget(self.mainBodySplitter)

        # sets the window's main layout
        self.setLayout(self.mainBodyHBox)

        # left side vbox
        self.leftSideWidget = QWidget()
        self.leftSideVBox = QVBoxLayout()
        self.leftSideWidget.setLayout(self.leftSideVBox)
        self.mainBodySplitter.addWidget(self.leftSideWidget)

        # top menu bar
        self.topBar = QMenuBar(self)
        self.fileMenu = QMenu("File")
        self.exportMenu = QMenu("Export")
        self.helpMenu = QMenu("Help")
        self.settingsMenu = QMenu("Settings")
        self.fileMenu.addAction("Save", self.save)
        self.fileMenu.addAction("Load", self.load)
        self.exportMenu.addAction("Export to word", self.word)
        self.exportMenu.addAction("Export to google docs", self.docs)
        self.helpMenu.addAction("Support", self.support)
        self.helpMenu.addAction("Terms and conditions", self.terms)
        self.settingsMenu.addAction("Weighting", self.weighting)
        self.settingsMenu.addAction("Auto save", self.autoSave)
        self.topBar.addMenu(self.fileMenu)
        self.topBar.addMenu(self.exportMenu)
        self.topBar.addMenu(self.helpMenu)
        self.topBar.addMenu(self.settingsMenu)
        self.mainBodyHBox.setMenuBar(self.topBar)

        # sets up the combo box and skills area
        # level select area vbox
        self.levelSelectAreaVbox = QVBoxLayout()
        self.leftSideVBox.addLayout(self.levelSelectAreaVbox)

        # level select combo box
        self.levelSelect = QComboBox()
        for i in range(1, 11):
            self.levelSelect.addItem(f"Swim kids {i}")
        self.levelSelect.currentTextChanged.connect(self.updateLevelOverview)
        self.levelSelectAreaVbox.addWidget(self.levelSelect)

        # level skills overview
        self.levelOverviewTreeView = QTreeWidget()
        self.levelSelectAreaVbox.addWidget(self.levelOverviewTreeView)
        self.levelOverviewTreeView.setHeaderLabels(["Activity", "Taught"])
        self.levelOverviewTreeView.itemClicked.connect(self.activitySelected)

        # sets up the ideas area
        # list of possible activities
        self.activityOverviewTreeView = QTreeWidget()
        self.activityOverviewTreeView.setHeaderLabels(["Activity", "Type", "Time"])
        self.activityOverviewTreeView.itemClicked.connect(self.activityDetails)
        self.leftSideVBox.addWidget(self.activityOverviewTreeView)

        # sets up the current lesson plan area
        # sets up the lesson plan area containers
        self.lessonPlanWidgetContainer = QWidget()
        self.lessonPlanVBoxContainer = QVBoxLayout()
        self.lessonPlanWidgetContainer.setLayout(self.lessonPlanVBoxContainer)
        self.mainBodySplitter.addWidget(self.lessonPlanWidgetContainer)

        # creates the scroll area for the list of activities in the lesson
        self.lessonPlanScrollArea = QScrollArea()
        self.lessonPlanWidget = QWidget()
        self.lessonPlanVBox = QVBoxLayout()
        self.lessonPlanWidget.setLayout(self.lessonPlanVBox)
        self.lessonPlanVBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lessonPlanScrollArea.setWidgetResizable(True)
        self.lessonPlanScrollArea.setWidget(self.lessonPlanWidget)

        # adds the scroll area to the layout
        self.lessonPlanVBoxContainer.addWidget(self.lessonPlanScrollArea)

        # adds add new blank to scroll area
        self.newBtn = QPushButton("New")
        self.newBtn.setMinimumHeight(50)
        self.newBtn.clicked.connect(self.newActivity)
        self.lessonPlanVBox.addWidget(self.newBtn)

        # adds the page controls under the scroll area
        self.lessonPlanList = {}
        self.lessonPlanControlsHBox = QHBoxLayout()
        self.nextBtn = QPushButton("->")
        self.nextBtn.clicked.connect(self.next)
        self.previousBtn = QPushButton("<-")
        self.previousBtn.clicked.connect(self.previous)
        self.dayNumInt = 1
        self.dayTotalInt = 10
        self.dayNum = QLineEdit(str(self.dayNumInt))
        self.dayNum.textEdited.connect(self.dayNumChanged)
        self.daySlashLabel = QLabel("/")
        self.dayTotal = QLineEdit(str(self.dayTotalInt))
        self.dayTotal.textEdited.connect(self.dayTotalChanged)

        # sets up the page controls
        self.dayNum.setMaximumWidth(20)
        self.daySlashLabel.setMaximumWidth(5)
        self.dayTotal.setMaximumWidth(20)
        self.nextBtn.setMaximumWidth(50)
        self.previousBtn.setMaximumWidth(50)
        self.lessonPlanControlsHBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lessonPlanControlsHBox.addWidget(self.previousBtn)
        self.lessonPlanControlsHBox.addWidget(self.dayNum)
        self.lessonPlanControlsHBox.addWidget(self.daySlashLabel)
        self.lessonPlanControlsHBox.addWidget(self.dayTotal)
        self.lessonPlanControlsHBox.addWidget(self.nextBtn)
        self.lessonPlanVBoxContainer.addLayout(self.lessonPlanControlsHBox)

        # populates the level overview
        self.updateLevelOverview("Swim kids 1", False)

        # set initial ratio of the two sides of the window
        self.mainBodySplitter.setSizes([100, 200])


    def updateLevelOverview(self, LEVEL, clear=True):
        # amount of times each skill is taught
        self.saveDay(self.dayNumInt, False)
        activityTimesDict = self.reformat().getActivityAmt()
        # clears the old list
        self.levelOverviewTreeView.clear()
        if hasattr(self, "activityOverviewTreeView") and clear:
            self.activityOverviewTreeView.clear()
        # adds the new items
        self.addSectionToOverview("Fitness activities", LEVEL)
        self.addSectionToOverview("Skills and water safety", LEVEL)
        self.addSectionToOverview("Swimming", LEVEL)
        # expands everything
        self.levelOverviewTreeView.expandAll()

    def addSectionToOverview(self, ACTIVITY, LEVEL):
        # amount of times each skill is taught
        self.saveDay(self.dayNumInt, False)
        activityTimesDict = self.reformat().getActivityAmt()
        # adds to the treeview
        activities = constant.SWIMKIDSSKILLS[LEVEL][ACTIVITY].keys()
        topLevel = QTreeWidgetItem([ACTIVITY])
        for i in activities:
            item = QTreeWidgetItem([
                i,
                f"{0 if activityTimesDict.get(i) is None else activityTimesDict[i]}/3"]
            )
            topLevel.addChild(item)
        self.levelOverviewTreeView.addTopLevelItem(topLevel)

    def activitySelected(self, ITEM):
        ACTIVITY = ITEM.text(0)
        if ACTIVITY not in ["Fitness activities", "Skills and water safety", "Swimming"]:
            self.selectedActivity = ACTIVITY
            LEVEL = int(self.levelSelect.currentText()[-1])
            levelSpecific = []
            nonLevelSpecific = []
            for key in data.ACTIVITIES[ACTIVITY].keys():
                value = data.ACTIVITIES[ACTIVITY][key]
                if value.validForLevel(LEVEL):
                    levelSpecific.append([key, value])
                else:
                    nonLevelSpecific.append([key, value])
            # clears the old list
            self.activityOverviewTreeView.clear()
            # adds new entries
            self.addSectionToActivity(levelSpecific, "Level specific")
            self.addSectionToActivity(nonLevelSpecific, "Others")

    def addSectionToActivity(self, ACTIVITIES, NAME):
        topLevel = QTreeWidgetItem([NAME])
        for i in ACTIVITIES:
            item = QTreeWidgetItem([i[0], i[1].tp, str(i[1].time) + " min"])
            topLevel.addChild(item)
        self.activityOverviewTreeView.addTopLevelItem(topLevel)
        if NAME == "Level specific":
            topLevel.setExpanded(True)

    def activityDetails(self, ACTIVITY):
        if ACTIVITY.text(0) not in ["Level specific", "Others"]:
            newActivity = activityPanelGUI.ActivityPanel(
                data.ACTIVITIES[self.selectedActivity][ACTIVITY.text(0)].level,
                activity=data.ACTIVITIES[self.selectedActivity][ACTIVITY.text(0)],
                name=ACTIVITY.text(0)
            )
            self.lessonPlanVBox.insertWidget(self.lessonPlanVBox.count() - 1, newActivity)
            self.updateLevelOverview(self.levelSelect.currentText(), False)

    def newActivity(self):
        newActivity = activityPanelGUI.ActivityPanel(self.levelSelect.currentText())
        self.lessonPlanVBox.insertWidget(self.lessonPlanVBox.count() - 1, newActivity)
        self.updateLevelOverview(self.levelSelect.currentText(), False)

    def deleteActivity(self, item):
        # noinspection PyTypeChecker
        self.lessonPlanVBox.itemAt(self.lessonPlanVBox.indexOf(item)).widget().setParent(None)

    def next(self):
        if self.dayNumInt < self.dayTotalInt:
            # saves the day plan
            self.saveDay(self.dayNumInt, True)
            # changes day number
            self.dayNumInt += 1
            # finds the new day plan
            self.loadDay(self.dayNumInt)
        self.dayNum.setText(str(self.dayNumInt))

    def previous(self):
        if self.dayNumInt > 1:
            # saves the day plan
            self.saveDay(self.dayNumInt, True)
            # changes day number
            self.dayNumInt -= 1
            # finds the new day plan
            self.loadDay(self.dayNumInt)
        self.dayNum.setText(str(self.dayNumInt))

    def saveDay(self, day, delete):
        li = []
        for i in reversed(range(self.lessonPlanVBox.count() - 1)):
            li.append(self.lessonPlanVBox.itemAt(i).widget())
            if delete:
                # noinspection PyTypeChecker
                self.lessonPlanVBox.itemAt(i).widget().setParent(None)
        self.lessonPlanList[day] = li

    def loadDay(self, day):
        if self.lessonPlanList.__contains__(day):
            for i in self.lessonPlanList[day]:
                self.lessonPlanVBox.insertWidget(self.lessonPlanVBox.count() - 1, i)

    def dayNumChanged(self, txt):
        if not txt == "":
            if int(txt) > self.dayTotalInt:
                # sets the day number
                self.dayNumInt = self.dayTotalInt
            else:
                # sets the day number
                self.dayNumInt = int(txt)
            self.dayNum.setText(str(self.dayNumInt))

    def dayTotalChanged(self, txt):
        if not txt == "":
            self.dayTotalInt = int(txt)

        else:
            self.dayTotalInt = 0

    def save(self):
        pass

    def load(self):
        pass

    def support(self):
        pass

    def terms(self):
        pass

    def weighting(self):
        pass

    def autoSave(self):
        pass

    def word(self):
        lesson = self.reformat()
        lesson.exportToWord()

    def docs(self):
        pass

    def reformat(self):
        lesson = lessonPlan.LessonPlan()
        for key in self.lessonPlanList:
            lesson.dayList.append([])
            for activity in self.lessonPlanList[key]:
                lesson.dayList[-1].append(activity.getData())
        print(lesson.dayList)
        return lesson
