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

        # adds tabs too the tab box
        self.tabs = []
        for items in presets.options.items():
            self.tabs.append(QWidget())
            self.tabWidget.addTab(self.tabs[-1], items[0])

        # intro tab
        self.introVBox = QVBoxLayout()
        self.tabs[0].setLayout(self.introVBox)

        self.introComboBox = QComboBox()
        self.introOnOff = QCheckBox("Add intro to every day by default")
        self.introComboBox.addItems([])
        self.introOnOff.stateChanged.connect(toggleIntroOnOff)
        self.introVBox.addWidget(self.introComboBox)
        self.introVBox.addWidget(self.introOnOff)

        # others tab
        self.otherVBox = QVBoxLayout()
        self.tabs[1].setLayout(self.otherVBox)

        self.othersLevelComboBox = QComboBox()
        self.othersLevelComboBox.addItems(constant.SWIMKIDSLIST)
        self.othersLevelComboBox.currentTextChanged.connect(levelChanged)
        self.otherVBox.addWidget(self.othersLevelComboBox)


def toggleIntroOnOff(state):
    if state == Qt.CheckState.Checked.value:
        presets.options["Intro"]["introDefault"] = True
    else:
        presets.options["Intro"]["introDefault"] = False


def levelChanged(level):
    presets.options["Others"]["defaultLevel"] = level
print(presets.options["Others"]["defaultLevel"])
