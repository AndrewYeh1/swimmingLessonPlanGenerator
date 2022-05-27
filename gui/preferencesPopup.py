# import constant
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
                             QTabWidget,  # tabs
                             QCheckBox,  # check box
                             QVBoxLayout, QHBoxLayout, )  # layout management

# widgets
from gui import activityPanelGUI

# import exporters
from templates import lessonPlan


class Preferences(QWidget):
    def __init__(self):
        # calls the super class
        super().__init__()

        # creates the main layout
        self.mainHBox = QHBoxLayout()
        self.setLayout(self.mainHBox)

        # tab box
        self.tabWidget = QTabWidget()
        self.mainHBox.addWidget(self.tabWidget)

        # adds tabs to the tab box
        self.tabIntro = QWidget()
        self.tabOthers = QWidget()
        self.tabWidget.addTab(self.tabIntro, "Intro")
        self.tabWidget.addTab(self.tabOthers, "Others")

        # intro tab
        self.introVBox = QVBoxLayout()
        self.tabIntro.setLayout(self.introVBox)

        self.introComboBox = QComboBox()
        self.introOnOff = QCheckBox("Add intro to every day by default")
        self.introComboBox.addItems([])
        self.introOnOff.stateChanged.connect(toggleIntroOnOff)
        self.introVBox.addWidget(self.introComboBox)
        self.introVBox.addWidget(self.introOnOff)

        # others tab
        self.otherVBox = QVBoxLayout()
        self.tabOthers.setLayout(self.otherVBox)

        self.othersLevelComboBox = QComboBox()
        self.othersLevelComboBox.addItems(constant.SWIMKIDSLIST)
        self.othersLevelComboBox.currentTextChanged.connect(levelChanged)
        self.otherVBox.addWidget(self.othersLevelComboBox)


def toggleIntroOnOff(state):
    config = presets.getConfig()
    config["Intro"]["enabled"] = "true" if state == Qt.CheckState.Checked.value else "false"
    presets.setConfig(config)


def levelChanged(level):
    config = presets.getConfig()
    config["Others"]["defaultLevel"] = level
    presets.setConfig(config)
