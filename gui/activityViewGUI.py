# partial for callback
from functools import partial

# import constant

# gui imports
from PyQt6.QtWidgets import (QWidget,  # window
                             QPushButton, QLabel,  # buttons and labels
    # inputs
    # tabs
    # scroll
    # frame
    # dialog box
    # drop down menu
    # treeview
    # checkbox
                             QHBoxLayout, )  # layout management


class ActivityView(QWidget):
    def __init__(self, deleteCallback, toggleCallback, activity, name, *args, **kwargs):
        # calls the super class
        super().__init__(*args, **kwargs)

        # gets activity and name
        self.name = name
        self.activity = activity

        # gets the callback function
        self.deleteCallback = deleteCallback
        self.toggleCallback = toggleCallback

        # main hbox
        self.mainHBox = QHBoxLayout()

        # display fields
        self.timeLabel = QLabel()
        self.nameLabel = QLabel()
        self.expandBtn = QPushButton("Expand")
        self.deleteBtn = QPushButton("Delete")

        # connects buttons to functions
        self.expandBtn.clicked.connect(self.expand)
        self.deleteBtn.clicked.connect(self.delete)

        # adds fields to the hbox
        self.mainHBox.addWidget(self.timeLabel)
        self.mainHBox.addWidget(self.nameLabel)
        self.mainHBox.addWidget(self.expandBtn)
        self.mainHBox.addWidget(self.deleteBtn)

        # adds data to fields
        if self.name is not None:
            self.nameLabel.setText(self.name)
        if self.activity.time is not None:
            self.timeLabel.setText(str(self.activity.time) + " min")

        # sets its own layout
        self.setLayout(self.mainHBox)

    def expand(self):
        partial(self.toggleCallback, self.activity, self.name)()
        # noinspection PyTypeChecker
        self.setParent(None)

    def delete(self):
        self.deleteCallback()
