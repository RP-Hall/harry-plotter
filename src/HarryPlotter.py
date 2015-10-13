# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HarryPlotter.ui'
#
# Created: Tue Mar 24 17:58:58 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(862, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 862, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuThemes = QtGui.QMenu(self.menuHelp)
        self.menuThemes.setObjectName(_fromUtf8("menuThemes"))
        self.menuHelp_2 = QtGui.QMenu(self.menubar)
        self.menuHelp_2.setObjectName(_fromUtf8("menuHelp_2"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionDraw_from_file = QtGui.QAction(MainWindow)
        self.actionDraw_from_file.setObjectName(_fromUtf8("actionDraw_from_file"))
        self.actionShow_CalC = QtGui.QAction(MainWindow)
        self.actionShow_CalC.setObjectName(_fromUtf8("actionShow_CalC"))
        self.actionNew_Tab = QtGui.QAction(MainWindow)
        self.actionNew_Tab.setObjectName(_fromUtf8("actionNew_Tab"))
        self.actionAdd_Plot = QtGui.QAction(MainWindow)
        self.actionAdd_Plot.setObjectName(_fromUtf8("actionAdd_Plot"))
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.actionAxisLabels = QtGui.QAction(MainWindow)
        self.actionAxisLabels.setObjectName(_fromUtf8("actionAxisLabels"))
        self.actionBlack = QtGui.QAction(MainWindow)
        self.actionBlack.setCheckable(True)
        self.actionBlack.setChecked(True)
        self.actionBlack.setObjectName(_fromUtf8("actionBlack"))
        self.actionWhite = QtGui.QAction(MainWindow)
        self.actionWhite.setCheckable(True)
        self.actionWhite.setChecked(False)
        self.actionWhite.setObjectName(_fromUtf8("actionWhite"))
        self.actionClose_Tab = QtGui.QAction(MainWindow)
        self.actionClose_Tab.setObjectName(_fromUtf8("actionClose_Tab"))
        self.menuFile.addAction(self.actionAdd_Plot)
        self.menuFile.addAction(self.actionNew_Tab)
        self.menuFile.addAction(self.actionClose_Tab)
        self.menuThemes.addAction(self.actionBlack)
        self.menuThemes.addAction(self.actionWhite)
        self.menuHelp.addAction(self.actionAxisLabels)
        self.menuHelp.addAction(self.menuThemes.menuAction())
        self.menuHelp_2.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuHelp_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Harry PLOTter", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Settings", None))
        self.menuThemes.setTitle(_translate("MainWindow", "Themes", None))
        self.menuHelp_2.setTitle(_translate("MainWindow", "Help", None))
        self.actionDraw_from_file.setText(_translate("MainWindow", "Draw from file...", None))
        self.actionShow_CalC.setText(_translate("MainWindow", "Hide Calulator", None))
        self.actionNew_Tab.setText(_translate("MainWindow", "New Tab", None))
        self.actionAdd_Plot.setText(_translate("MainWindow", "Add Plot", None))
        self.action_About.setText(_translate("MainWindow", "About", None))
        self.actionAxisLabels.setText(_translate("MainWindow", "Change axes specifications", None))
        self.actionBlack.setText(_translate("MainWindow", "Black", None))
        self.actionWhite.setText(_translate("MainWindow", "White", None))
        self.actionClose_Tab.setText(_translate("MainWindow", "Close Tab", None))

