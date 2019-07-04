# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui',
# licensing of 'add.ui' applies.
#
# Created: Thu Jul  4 10:48:00 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddDialog(object):
    def setupUi(self, AddDialog):
        AddDialog.setObjectName("AddDialog")
        AddDialog.resize(371, 185)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 140, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(AddDialog)
        self.label.setGeometry(QtCore.QRect(30, 80, 81, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 101, 41))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AddDialog)
        self.label_3.setGeometry(QtCore.QRect(120, 30, 221, 41))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(AddDialog)
        self.lineEdit.setGeometry(QtCore.QRect(120, 80, 211, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(AddDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddDialog)

    def retranslateUi(self, AddDialog):
        AddDialog.setWindowTitle(QtWidgets.QApplication.translate("AddDialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("AddDialog", "Add a name:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("AddDialog", "Device detected:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("AddDialog", "None", None, -1))

