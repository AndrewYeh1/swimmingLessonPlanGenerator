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
                             QSizePolicy,  # sizing of button
                             QVBoxLayout, QHBoxLayout, QGridLayout)  # layout management


class LessonPlanHeader(QWidget):
    def __init__(self):
        # calls the super class
        super().__init__()

        # main vbox layout
        self.mainGrid = QGridLayout()

        # creates the labels and input fields
        self.courseLabel = QLabel("Course:")
        self.wsiNameLabel = QLabel("WSI name:")
        self.locationLabel = QLabel("Location:")
        self.courseInput = QLineEdit()
        self.wsiNameInput = QLineEdit()
        self.locationInput = QLineEdit()
        self.wsiNameInput.setText(presets.getConfig()["Personal"]["wsiName"])
        self.locationInput.setText(presets.getConfig()["Personal"]["location"])

        # adds the widgets to the grid
        self.mainGrid.addWidget(self.courseLabel, 0, 0)
        self.mainGrid.addWidget(self.wsiNameLabel, 1, 0)
        self.mainGrid.addWidget(self.locationLabel, 4, 0)
        self.mainGrid.addWidget(self.courseInput, 0, 1)
        self.mainGrid.addWidget(self.wsiNameInput, 1, 1)
        self.mainGrid.addWidget(self.locationInput, 4, 1)

        # sets its own layout
        self.setLayout(self.mainGrid)
