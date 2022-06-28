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
                             QFileDialog,  # file dialog
                             QVBoxLayout, QHBoxLayout)  # layout management

# widgets
from gui import activityPanelGUI
from gui import lessonPlanHeaderGUI

# windows
from gui import preferencesPopup

# import exporters
from templates import lessonPlan

# import file managers
from fileManager import load
import json


class LoadGUI(QFileDialog):
    def __init__(self):
        # calls the super class
        super().__init__()

    def load(self):
        self.setNameFilter("*.lspn")
        filePath = self.getOpenFileName()
        if filePath[0] != '':
            return load.load(filePath[0])
