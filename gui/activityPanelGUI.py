# import constant

# import template
from templates import activityTemplates

# import GUI widgets
from gui import activityEditGUI
from gui import activityViewGUI

# gui imports
from PyQt6.QtWidgets import (QWidget,  # window
                             QHBoxLayout, )  # layout management


class ActivityPanel(QWidget):
    def __init__(self, level, updateLessonPlan, tp="Expanded", activity=None, *args, **kwargs):
        # callback function
        self.updateLessonPlan = updateLessonPlan

        # variables
        self.activity = activity

        # calls the super class
        super().__init__(*args, **kwargs)

        # main hbox
        self.mainHBox = QHBoxLayout()
        self.mainHBox.setContentsMargins(0, 0, 0, 0)

        # sets value of activity
        self.tp = tp
        if self.activity is None:
            self.activity = activityTemplates.Template(level=[level])

        # adds the collapsed and expanded view
        self.collapsedView = activityViewGUI.ActivityView(self.delete, self.changeToExpandedView, self.activity)
        self.expandedView = activityEditGUI.ActivityEdit(self.updateActivity, self.delete,
                                                         self.changeToCollapsedView,
                                                         self.activity)
        self.mainHBox.addWidget(self.collapsedView)
        self.mainHBox.addWidget(self.expandedView)

        # opens up expanded or collapsed view
        if tp == "Expanded":
            self.collapsedView.hide()
        else:
            self.expandedView.hide()

        # sets its own layout
        self.setLayout(self.mainHBox)

    def delete(self):
        # noinspection PyTypeChecker
        self.setParent(None)
        self.updateLessonPlan()

    def changeToCollapsedView(self):
        self.collapsedView.show()
        self.expandedView.hide()
        self.tp = "Collapsed"

    def changeToExpandedView(self):
        self.collapsedView.hide()
        self.expandedView.show()
        self.tp = "Expanded"

    def updateActivity(self):
        # noinspection PyUnresolvedReferences
        self.activity = self.expandedView.getActivity()
        self.updateLessonPlan()

    def getData(self):
        return self.activity
