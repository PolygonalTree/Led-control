# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui'
#
# Created: Tue Aug 19 12:48:34 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AddDialog(object):
    def setupUi(self, AddDialog):
        AddDialog.setObjectName("AddDialog")
        AddDialog.resize(371, 185)
        self.buttonBox = QtGui.QDialogButtonBox(AddDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 140, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(AddDialog)
        self.label.setGeometry(QtCore.QRect(30, 80, 81, 31))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(AddDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 101, 41))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(AddDialog)
        self.label_3.setGeometry(QtCore.QRect(120, 30, 221, 41))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtGui.QLineEdit(AddDialog)
        self.lineEdit.setGeometry(QtCore.QRect(120, 80, 211, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(AddDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddDialog)

    def retranslateUi(self, AddDialog):
        AddDialog.setWindowTitle(QtGui.QApplication.translate("AddDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddDialog", "Add a name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddDialog", "Device detected:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AddDialog", "None", None, QtGui.QApplication.UnicodeUTF8))

