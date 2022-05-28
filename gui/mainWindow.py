# import constant
import exporters.word
from internalData import constant, presets

# import data
from internalData import data

# PyQt6 gui imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget,  # window
                             QPushButton, QLabel,  # buttons and labels
                             QLineEdit,  # inputs
                             QScrollArea,  # scroll
                             QComboBox,  # drop down menu
                             QTreeWidget, QTreeWidgetItem,  # treeview
                             QSplitter,  # advanced layout management
                             QMenu, QMenuBar,  # top bar
                             QVBoxLayout, QHBoxLayout)  # layout management

# widgets
from gui import activityPanelGUI
from gui import lessonPlanHeaderGUI

# windows
from gui import preferencesPopup

# import exporters
from templates import lessonPlan

# import file managers
from fileManager import load, save


class MainWindow(QWidget):
    def __init__(self, app):
        # calls the super class
        super().__init__()

        # variables
        self.selectedActivity = None
        self.lesson = lessonPlan.LessonPlan()

        # gets the app for further use
        self.app = app

        # popups
        self.preferencesWindow = preferencesPopup.Preferences()

        # sets the window title
        self.setWindowTitle(constant.TITLE)

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
        self.settingsMenu.addAction("Preferences", self.preferences)
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

        # creates the header area for the lesson plan
        self.headerBtnOpen = QPushButton("Show")
        self.headerBtnClose = QPushButton("Hide")
        self.headerBtnOpen.clicked.connect(self.openHeader)
        self.headerBtnClose.clicked.connect(self.closeHeader)
        self.header = lessonPlanHeaderGUI.LessonPlanHeader()
        self.lessonPlanVBoxContainer.addWidget(self.headerBtnOpen)
        self.lessonPlanVBoxContainer.addWidget(self.headerBtnClose)
        self.lessonPlanVBoxContainer.addWidget(self.header)
        if presets.getConfig()["GUI"]["showHeader"] == "true":
            self.openHeader()
        else:
            self.closeHeader()

        # creates the scroll area for the list of activities in the lesson
        self.lessonPlanScrollArea = QScrollArea()
        self.lessonPlanWidget = QWidget()
        self.lessonPlanVBox = QVBoxLayout()
        self.lessonPlanWidget.setLayout(self.lessonPlanVBox)
        self.lessonPlanVBox.setAlignment(Qt.AlignmentFlag.AlignTop)
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

        # populates the level overview with the default level
        self.levelSelect.setCurrentText(presets.getConfig()["Others"]["defaultLevel"])
        self.updateLevelOverview(presets.getConfig()["Others"]["defaultLevel"])

        # set initial ratio of the two sides of the window
        self.mainBodySplitter.setSizes([100, 200])

        # adds the intro if it is on
        if presets.getConfig()["Intro"]["enabled"] == "true":
            self.addIntro()

    def updateLevelOverview(self, LEVEL):
        # clears the old list
        self.levelOverviewTreeView.clear()
        if hasattr(self, "activityOverviewTreeView"):
            self.activityOverviewTreeView.clear()
        # adds the new items
        self.addSectionToOverview("Fitness activities", LEVEL)
        self.addSectionToOverview("Skills and water safety", LEVEL)
        self.addSectionToOverview("Swimming", LEVEL)
        # adds the amount of times each skill was taught to the overview
        self.setOverviewTaught()
        # expands everything
        self.levelOverviewTreeView.expandAll()
        # sets the level of the lesson plan header
        if presets.getConfig()["GUI"]["linkCourseToMain"] == "true":
            self.header.courseInput.setText(LEVEL)

    def addSectionToOverview(self, ACTIVITY, LEVEL):
        # adds to the treeview
        activities = constant.SWIMKIDSSKILLS[LEVEL][ACTIVITY].keys()
        topLevel = QTreeWidgetItem([ACTIVITY])
        for i in activities:
            item = QTreeWidgetItem([i])
            topLevel.addChild(item)
        self.levelOverviewTreeView.addTopLevelItem(topLevel)

    def updateLessonPlan(self):
        self.saveDay()
        self.reformat()
        self.setOverviewTaught()

    def setOverviewTaught(self):
        # amount of times each skill is taught
        activityTimesDict = self.lesson.getActivityAmt()
        for i in range(self.levelOverviewTreeView.topLevelItemCount()):
            for j in range(self.levelOverviewTreeView.topLevelItem(i).childCount()):
                activity = self.levelOverviewTreeView.topLevelItem(i).child(j).text(0)
                num = f"{0 if activityTimesDict.get(activity) is None else activityTimesDict[activity]}/3"
                self.levelOverviewTreeView.topLevelItem(i).child(j).setText(1, num)

    def activitySelected(self, ITEM):
        ACTIVITY = ITEM.text(0)
        if ACTIVITY not in ["Fitness activities", "Skills and water safety", "Swimming"]:
            self.selectedActivity = ACTIVITY
            LEVEL = int(self.levelSelect.currentText()[-1])
            levelSpecific = []
            nonLevelSpecific = []
            for i in data.ACTIVITIES[ACTIVITY]:
                if i.validForLevel(LEVEL):
                    levelSpecific.append([i.name, i])
                else:
                    nonLevelSpecific.append([i.name, i])
            # clears the old list
            self.activityOverviewTreeView.clear()
            # adds new entries
            self.addSectionToActivity(levelSpecific, "Level specific")
            self.addSectionToActivity(nonLevelSpecific, "Other levels")

    def addSectionToActivity(self, ACTIVITIES, NAME):
        topLevel = QTreeWidgetItem([NAME])
        for i in ACTIVITIES:
            item = QTreeWidgetItem([i[0], i[1].tp, str(i[1].time) + " min"])
            topLevel.addChild(item)
        self.activityOverviewTreeView.addTopLevelItem(topLevel)
        if NAME == "Level specific":
            topLevel.setExpanded(True)

    def addIntro(self):
        newActivity = activityPanelGUI.ActivityPanel(
            data.intro.level,
            self.updateLessonPlan,
            activity=data.intro,
            name="Intro",
            tp="Collapsed"
        )
        self.lessonPlanVBox.insertWidget(self.lessonPlanVBox.count() - 1, newActivity)
        self.updateLessonPlan()

    def activityDetails(self, ACTIVITY):
        if ACTIVITY.text(0) not in ["Level specific", "Other levels"]:
            activitySection = data.ACTIVITIES[self.selectedActivity]
            activity = activitySection[[i.name for i in activitySection].index(ACTIVITY.text(0))]
            newActivity = activityPanelGUI.ActivityPanel(
                activity.level,
                self.updateLessonPlan,
                activity=activity
            )
            self.lessonPlanVBox.insertWidget(self.lessonPlanVBox.count() - 1, newActivity)
            self.updateLessonPlan()

    def newActivity(self):
        newActivity = activityPanelGUI.ActivityPanel(self.levelSelect.currentText(), self.updateLessonPlan)
        self.lessonPlanVBox.insertWidget(self.lessonPlanVBox.count() - 1, newActivity)
        self.updateLessonPlan()

    def deleteActivity(self, item):
        # noinspection PyTypeChecker
        self.lessonPlanVBox.itemAt(self.lessonPlanVBox.indexOf(item)).widget().setParent(None)

    def next(self):
        if self.dayNumInt < self.dayTotalInt:
            # changes the day
            self.changeDay(self.dayNumInt + 1)
            # changes day number
            self.dayNumInt += 1
        self.dayNum.setText(str(self.dayNumInt))

    def previous(self):
        if self.dayNumInt > 1:
            # changes the day
            self.changeDay(self.dayNumInt - 1)
            # changes day number
            self.dayNumInt -= 1
        self.dayNum.setText(str(self.dayNumInt))

    def changeDay(self, day):
        self.saveDay()
        self.clearDay()
        self.loadDay(day)

    def clearDay(self):
        for i in reversed(range(self.lessonPlanVBox.count() - 1)):
            # noinspection PyTypeChecker
            self.lessonPlanVBox.itemAt(i).widget().setParent(None)

    def saveDay(self):
        li = []
        for i in range(self.lessonPlanVBox.count() - 1):
            li.append(self.lessonPlanVBox.itemAt(i).widget())
        self.lessonPlanList[self.dayNumInt] = li

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

    def openHeader(self):
        self.header.show()
        self.headerBtnClose.show()
        self.headerBtnOpen.hide()

    def closeHeader(self):
        self.header.hide()
        self.headerBtnOpen.show()
        self.headerBtnClose.hide()

    def getHeader(self, lesson: lessonPlan):
        lesson.wsi = self.header.wsiNameInput.text()
        lesson.course = self.header.courseInput.text()
        lesson.location = self.header.locationInput.text()
        return lesson

    def save(self):
        self.saveDay()
        save.save(self.reformat())

    def load(self):
        self.saveDay()
        load.load(self.reformat())

    def support(self):
        pass

    def terms(self):
        pass

    def weighting(self):
        pass

    def preferences(self):
        self.preferencesWindow.show()

    def word(self):
        self.saveDay()
        wordExporter = exporters.word.Word(self.lesson)
        wordExporter.export()

    def docs(self):
        pass

    def reformat(self):
        lesson = lessonPlan.LessonPlan()
        for key in self.lessonPlanList:
            lesson.dayList.append([])
            for activity in self.lessonPlanList[key]:
                lesson.dayList[-1].append(activity.getData())
        lesson = self.getHeader(lesson)
        self.lesson = lesson
