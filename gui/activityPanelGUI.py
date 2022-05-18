# import constant

# import template
from templates import activityTemplates

# import GUI widgets
from gui import activityEditGUI
from gui import activityViewGUI

# partial for callback

# gui imports
from PyQt6.QtWidgets import (QWidget,  # window
                             QHBoxLayout, )  # layout management


class ActivityPanel(QWidget):
    def __init__(self, level, name="New", tp="Expanded", activity=None, *args, **kwargs):
        # variables
        self.name = name
        self.activity = activity

        # calls the super class
        super().__init__(*args, **kwargs)

        # main hbox
        self.mainHBox = QHBoxLayout()
        self.mainHBox.setContentsMargins(0, 0, 0, 0)

        # opens up expanded or collapsed view
        if tp == "Expanded":
            if activity is None:
                self.changeToExpandedView(activityTemplates.Template(level=[level]), name=name)
            else:
                self.changeToExpandedView(activity, name=name)
        else:
            if activity is None:
                self.changeToCollapsedView(activityTemplates.Template(level=[level]), name=name)
            else:
                self.changeToCollapsedView(activity, name=name)

        # sets its own layout
        self.setLayout(self.mainHBox)

    def delete(self):
        # noinspection PyTypeChecker
        self.setParent(None)

    def changeToCollapsedView(self, activity, name):
        collapsedView = activityViewGUI.ActivityView(self.delete, self.changeToExpandedView, activity, name)
        self.name = name
        self.activity = activity
        self.mainHBox.addWidget(collapsedView)

    def changeToExpandedView(self, activity, name):
        expandedView = activityEditGUI.ActivityEdit(self.delete, self.changeToCollapsedView, activity, name)
        self.name = name
        self.activity = activity
        self.mainHBox.addWidget(expandedView)

    def getData(self):
        return [self.name, self.activity]
