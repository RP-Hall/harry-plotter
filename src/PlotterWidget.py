# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PlotterWidget.ui'
#
# Created: Tue Mar 24 17:36:42 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(840, 514)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphicsView_3d = GLViewWidget(Form)
        self.graphicsView_3d.setObjectName(_fromUtf8("graphicsView_3d"))
        self.gridLayout.addWidget(self.graphicsView_3d, 0, 0, 2, 1)
        self.addPlotButton = QtGui.QPushButton(Form)
        self.addPlotButton.setMaximumSize(QtCore.QSize(200, 56))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.addPlotButton.setFont(font)
        self.addPlotButton.setStyleSheet(_fromUtf8(""))
        self.addPlotButton.setObjectName(_fromUtf8("addPlotButton"))
        self.gridLayout.addWidget(self.addPlotButton, 0, 1, 1, 1)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listWidget.setLineWidth(10)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.addPlotButton.setText(_translate("Form", "+", None))

from pyqtgraph.opengl import GLViewWidget
