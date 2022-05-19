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
                             QVBoxLayout, QHBoxLayout, )  # layout management

# widgets
from gui import activityPanelGUI

# import exporters
from templates import lessonPlan


class IntroGUI(QWidget):
    def __init__(self):
        # calls the super class
        super().__init__()

        # creates the main layout
        self.mainVBox = QVBoxLayout()
        self.setLayout(self.mainVBox)

    def toggle(self):
        pass
