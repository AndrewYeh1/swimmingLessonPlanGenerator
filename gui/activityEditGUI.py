# import constant
from internalData import constant

# import template
from templates import activityTemplates

# gui imports
from PyQt6.QtWidgets import (QWidget,  # window
                             QPushButton, QLabel,  # buttons and labels
                             QLineEdit, QTextEdit,  # inputs
                             QFrame,  # frame
                             QComboBox,  # drop down menu
                             QCheckBox,  # checkbox
                             QVBoxLayout, QHBoxLayout, QGridLayout,)  # layout management


class ActivityEdit(QWidget):
    def __init__(self, activityChanged, deleteCallback, confirmCallback, activity, *args, **kwargs):
        # constants
        TYPES = constant.TYPE

        # calls the super class
        super().__init__(*args, **kwargs)

        # callback function
        self.deleteCallback = deleteCallback
        self.confirmCallback = confirmCallback

        # main frame
        self.mainFrame = QFrame()
        self.mainFrame.setFrameStyle(QFrame.Shape.StyledPanel)

        # main hbox
        self.mainHBox = QHBoxLayout()

        # creates the buttons and input fields
        self.mainVBox = QVBoxLayout()
        self.nameHBox = QHBoxLayout()
        self.timeHBox = QHBoxLayout()
        self.typeHBox = QHBoxLayout()
        self.activityHBox = QHBoxLayout()
        self.descriptionHBox = QHBoxLayout()
        self.formationHBox = QHBoxLayout()
        self.equipmentHBox = QHBoxLayout()
        self.nameInput = QLineEdit()
        self.nameLabel = QLabel("Name:")
        self.timeInput = QLineEdit()
        self.timeLabel = QLabel("Time (min):")
        self.typeInput = QComboBox()
        self.typeLabel = QLabel("Type:")
        self.activityInput = QComboBox()
        self.activityLabel = QLabel("Activity:")
        self.descriptionInput = QTextEdit()
        self.descriptionLabel = QLabel("Notes:")
        self.formationInput = QLineEdit()
        self.formationLabel = QLabel("Formation:")
        self.equipmentInput = QLineEdit()
        self.equipmentLabel = QLabel("Equipment:")

        # sets up the combo boxes
        self.typeInput.addItems(TYPES)

        # bottom bar
        self.bottomBarHBox = QHBoxLayout()
        self.bottomBarGrid = QGridLayout()
        self.bottomBarVBox = QVBoxLayout()
        self.allCheckBox = QCheckBox("All")
        self.skSelection = []
        for i in range(1, 11):
            self.skSelection.append(QCheckBox(f"SK{i}"))
            self.skSelection[i - 1].clicked.connect(self.checkForAll)
            self.bottomBarGrid.addWidget(self.skSelection[i - 1], (i - 1) % 3, (i - 1) // 3)
        self.bottomBarGrid.addWidget(self.allCheckBox, 2, 3)
        self.collapseBtn = QPushButton("Confirm")
        self.deleteBtn = QPushButton("Delete")
        self.collapseBtn.clicked.connect(self.callback)
        self.deleteBtn.clicked.connect(self.delete)
        self.allCheckBox.clicked.connect(self.all)
        self.bottomBarVBox.addWidget(self.collapseBtn)
        self.bottomBarVBox.addWidget(self.deleteBtn)
        self.bottomBarHBox.addLayout(self.bottomBarGrid)
        self.bottomBarHBox.addLayout(self.bottomBarVBox)

        # checks the boxes that are valid
        self.setChecked(activity.level)
        self.checkForAll()

        # adds buttons and input fields to the vbox
        self.mainVBox.addLayout(self.nameHBox)
        self.nameHBox.addWidget(self.nameLabel, 1)
        self.nameHBox.addWidget(self.nameInput, 9)
        self.mainVBox.addLayout(self.timeHBox)
        self.timeHBox.addWidget(self.timeLabel, 1)
        self.timeHBox.addWidget(self.timeInput, 9)
        self.mainVBox.addLayout(self.typeHBox)
        self.typeHBox.addWidget(self.typeLabel, 1)
        self.typeHBox.addWidget(self.typeInput, 9)
        self.mainVBox.addLayout(self.activityHBox)
        self.activityHBox.addWidget(self.activityLabel, 1)
        self.activityHBox.addWidget(self.activityInput, 9)
        self.mainVBox.addLayout(self.descriptionHBox)
        self.descriptionHBox.addWidget(self.descriptionLabel, 1)
        self.descriptionHBox.addWidget(self.descriptionInput, 9)
        self.mainVBox.addLayout(self.formationHBox)
        self.formationHBox.addWidget(self.formationLabel, 1)
        self.formationHBox.addWidget(self.formationInput, 9)
        self.mainVBox.addLayout(self.equipmentHBox)
        self.equipmentHBox.addWidget(self.equipmentLabel, 1)
        self.equipmentHBox.addWidget(self.equipmentInput, 9)
        self.mainVBox.addLayout(self.bottomBarHBox)

        # adds in frame
        self.mainFrame.setLayout(self.mainVBox)
        self.mainHBox.addWidget(self.mainFrame)

        # sets its own layout
        self.setLayout(self.mainHBox)

        # fills in the input boxes if there is data
        if activity.name is not None:
            self.nameInput.setText(activity.name)
        if activity.time is not None:
            self.timeInput.setText(str(activity.time))
        if activity.tp is not None:
            self.typeInput.setCurrentIndex(TYPES.index(activity.tp))
        if activity.activity is not None:
            self.activityInput.setCurrentText(activity.activity)
        if activity.description is not None:
            self.descriptionInput.setText("\n".join(activity.description))

        # causes changes to the text box to callback
        self.nameInput.textChanged.connect(activityChanged)
        self.timeInput.textChanged.connect(activityChanged)
        self.typeInput.currentTextChanged.connect(activityChanged)
        self.activityInput.currentTextChanged.connect(activityChanged)
        self.descriptionInput.textChanged.connect(activityChanged)
        self.formationInput.textChanged.connect(activityChanged)
        self.equipmentInput.textChanged.connect(activityChanged)

    def callback(self):
        self.confirmCallback()

    def getActivity(self):
        # extracts data from input fields
        name = self.nameInput.text()
        activity = self.activityInput.currentText()
        if self.timeInput.text().isnumeric():
            time = int(self.timeInput.text())
        else:
            time = 0
        level = self.returnChecked()
        if self.typeInput.currentText() == "4Ds":
            tp = 1
        elif self.typeInput.currentText() == "Discovery":
            tp = 2
        else:
            tp = 3
        instructions = self.descriptionInput.toPlainText().split("\n")
        formation = self.formationInput.text()
        equipment = self.equipmentInput.text()
        activityToReturn = activityTemplates.Template(name=name, activity=activity, time=time, level=level, tp=tp,
                                                      description=instructions, formation=formation, equipment=equipment)
        return activityToReturn

    def delete(self):
        self.deleteCallback()

    def returnChecked(self):
        checkedList = []
        for i, box in enumerate(self.skSelection):
            if box.isChecked():
                checkedList.append(i + 1)
        return checkedList

    def setChecked(self, checked: list):
        for i in checked:
            if type(i) == str:
                i = int(i[-1])
            i = i - 1
            self.skSelection[i].setChecked(True)

    def all(self):
        if self.allCheckBox.isChecked():
            for i in self.skSelection:
                i.setChecked(True)
        else:
            for i in self.skSelection:
                i.setChecked(False)
        self.createActivityList()

    def checkForAll(self):
        checkedList = [i.isChecked() for i in self.skSelection]
        if all(checkedList):
            self.allCheckBox.setChecked(True)
        else:
            self.allCheckBox.setChecked(False)
        self.createActivityList()

    def createActivityList(self):
        checkedList = [i.isChecked() for i in self.skSelection]
        ls = []
        for index, item in enumerate(checkedList):
            if item:
                for i in constant.SWIMKIDSSKILLS[f"Swim kids {index + 1}"].keys():
                    ls.extend(constant.SWIMKIDSSKILLS[f"Swim kids {index + 1}"][i].keys())
        ls = sorted(list(dict.fromkeys(ls)))
        ls.append("Other")
        self.setActivityOptions(ls)

    def setActivityOptions(self, ls):
        self.activityInput.clear()
        self.activityInput.addItems(ls)
