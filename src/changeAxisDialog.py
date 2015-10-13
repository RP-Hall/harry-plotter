# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changeAxisDialog.ui'
#
# Created: Tue Mar 24 17:57:42 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(270, 269)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_x_title = QtGui.QLabel(Dialog)
        self.label_x_title.setGeometry(QtCore.QRect(40, 30, 91, 17))
        self.label_x_title.setObjectName(_fromUtf8("label_x_title"))
        self.label_y_title = QtGui.QLabel(Dialog)
        self.label_y_title.setGeometry(QtCore.QRect(40, 122, 91, 17))
        self.label_y_title.setObjectName(_fromUtf8("label_y_title"))
        self.label_x_unit = QtGui.QLabel(Dialog)
        self.label_x_unit.setGeometry(QtCore.QRect(40, 70, 71, 17))
        self.label_x_unit.setObjectName(_fromUtf8("label_x_unit"))
        self.label_y_unit = QtGui.QLabel(Dialog)
        self.label_y_unit.setGeometry(QtCore.QRect(40, 162, 71, 17))
        self.label_y_unit.setObjectName(_fromUtf8("label_y_unit"))
        self.lineEdit_x_title = QtGui.QLineEdit(Dialog)
        self.lineEdit_x_title.setGeometry(QtCore.QRect(120, 27, 113, 27))
        self.lineEdit_x_title.setObjectName(_fromUtf8("lineEdit_x_title"))
        self.lineEdit_x_unit = QtGui.QLineEdit(Dialog)
        self.lineEdit_x_unit.setGeometry(QtCore.QRect(121, 63, 113, 27))
        self.lineEdit_x_unit.setObjectName(_fromUtf8("lineEdit_x_unit"))
        self.lineEdit_y_unit = QtGui.QLineEdit(Dialog)
        self.lineEdit_y_unit.setGeometry(QtCore.QRect(121, 156, 113, 27))
        self.lineEdit_y_unit.setObjectName(_fromUtf8("lineEdit_y_unit"))
        self.lineEdit_y_title = QtGui.QLineEdit(Dialog)
        self.lineEdit_y_title.setGeometry(QtCore.QRect(120, 117, 113, 27))
        self.lineEdit_y_title.setObjectName(_fromUtf8("lineEdit_y_title"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Axes specifications", None))
        self.label_x_title.setText(_translate("Dialog", "X axis title", None))
        self.label_y_title.setText(_translate("Dialog", "Y axis title", None))
        self.label_x_unit.setText(_translate("Dialog", "X axis unit", None))
        self.label_y_unit.setText(_translate("Dialog", "Y axis unit", None))

