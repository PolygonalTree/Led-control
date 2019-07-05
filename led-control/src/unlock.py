# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unlock.ui',
# licensing of 'unlock.ui' applies.
#
# Created: Fri Jul  5 16:01:10 2019
#      by: pyside2-uic  running on PySide2 5.12.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_UnlockDialog(object):
    def setupUi(self, UnlockDialog):
        UnlockDialog.setObjectName("UnlockDialog")
        UnlockDialog.resize(314, 238)
        self.buttonBox = QtWidgets.QDialogButtonBox(UnlockDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(UnlockDialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 261, 31))
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(UnlockDialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 291, 141))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(UnlockDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), UnlockDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), UnlockDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UnlockDialog)

    def retranslateUi(self, UnlockDialog):
        UnlockDialog.setWindowTitle(QtWidgets.QApplication.translate("UnlockDialog", "Unlock", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("UnlockDialog", "Select a locked controller from the list:", None, -1))

