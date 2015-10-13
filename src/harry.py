#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import traceback
import json
from ast import literal_eval
from PyQt4 import QtGui, QtCore
from HarryPlotter import Ui_MainWindow
from PlotterWidget import Ui_Form
from plotBox import Ui_Dialog
import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as gl
import itemWidget
import parser
import re
import sys
from Graph import Graph
from random import randint
import os.path
import time
import changeAxisDialog

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

class ListItem(itemWidget.Ui_Form):
	def __init__(self, item, callingTabWidgetUI, parentItem, graph=None):
		super(ListItem, self).__init__()
		self.item = item
		self.callingTabWidgetUI = callingTabWidgetUI
		self.parentItem = parentItem
		self.graph = graph
	def additional(self):
		QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.closePressed)
	def closePressed(self):
		if self.callingTabWidgetUI.plotType==2:
			self.callingTabWidgetUI.w.removeItem(self.item)
		else :
			self.callingTabWidgetUI.graphicsView_3d.removeItem(self.item)
		#for item in self.callingTabWidgetUI.legend.items:
		#	if item[1].text == self.graph.name:
		#		print dir(self.callingTabWidgetUI.legend)
		self.callingTabWidgetUI.legend.removeItem(self.graph.name)
		#		break
		self.callingTabWidgetUI.listWidget.takeItem(self.callingTabWidgetUI.listWidget.row(self.parentItem))
		
	def getJson(self):
		json = "{"
		json = json + "\"name\":\""+str(self.graph.name)+"\""
		json = json + ", \"expr\":\""+str(self.graph.expr)+"\""
		json = json + ", \"dim\":\""+str(self.graph.dim)+"\""
		json = json + ", \"filename\":\""+str(self.graph.filename)+"\""
		json = json + ", \"xMin\":\""+str(self.graph.xMin)+"\""
		json = json + ", \"xMax\":\""+str(self.graph.xMax)+"\""
		json = json + ", \"yMin\":\""+str(self.graph.yMin)+"\""
		json = json + ", \"yMax\":\""+str(self.graph.yMax)+"\""
		json = json + ", \"plotType\":\""+str(self.graph.plotType)+"\""
		#json = json + ", \"color\":\""+str(self.graph.color)+"\""
		json = json + ", \"lineType\":\""+str(self.graph.lineType)+"\""
		json = json + ", \"lineWidth\":\""+str(self.graph.lineWidth)+"\""
		json = json + ", \"colString\":\""+str(self.graph.colString)+"\""
		json = json + ", \"opacity\":\""+str(self.graph.opacity)+"\""
		json = json + "}"
		return json


class PlotBox(Ui_Dialog):
	templates = [
	    ['Normal Distribution','1/(sqrt(2*pi)*$sigma$)*e^(-((x-$mean$)^2)/(2*$sigma$^2))','2D','sigma','mean'],
	    ['Parabolic equation','$a$*x^2 + $b$','2D','a','b'],
	    ['Paraboloid','$c$*(x^2/$a$^2 + y^2/$b$^2)','3D','a','b','c'],
	    ['Half ellipsoid','sqrt($c$-($a$*x^2+$b$*y^2))','3D','a','b','c'],
	    ['Ellipse','sqrt($c$*($a$*$a$-x*x))','2D','a','c'],
	    ['Hyperbolic Equation','sqrt($c$*($a$*$a$+x*x))','2D','a','c'],
	    ['Semi-Circle','sqrt($a$*$a$-x*x)','2D','a'],
	    ['Line','$m$*x+$c$','2D','m','c'],
	    ['Plane','$c$-$a$*x-$b$*y','3D','a','b','c'],
	    ['Witch of Agnesi','($a$^3)/(x*x+$a$*$a$)','2D','a'],
	    ['Half Butterfly Function','((x^2)-(x^6))^(0.1666)','2D']   
	]
	def __init__(self, callingTabWidgetUI, graph=None, filename=None):
		super(PlotBox,self).__init__()
		self.exprIndexText = ""
		self.DialogBox = None
		self.callingTabWidgetUI = callingTabWidgetUI
		self.graph = graph
		self.filename = filename
		if filename:
			self.isFileSelected = True
		else:
			self.isFileSelected = False

	def show2DSettings(self):
		self.radioButton.setChecked(True)

		self.lineEdit_x_min_3d.setEnabled(True)
		self.lineEdit_x_max_3d.setEnabled(True)
		
		self.lineEdit_y_min_3d.setEnabled(False)
		self.lineEdit_y_max_3d.setEnabled(False)

		self.lineTypeComboBox.setEnabled(True)
		self.opacityComboBox.setEnabled(False)
		self.exprDimLabel.setText("Y = ")
		

	def show3DSettings(self):
		self.radioButton_2.setChecked(True)

		self.lineEdit_x_min_3d.setEnabled(True)
		self.lineEdit_x_max_3d.setEnabled(True)
		
		self.lineEdit_y_min_3d.setEnabled(True)
		self.lineEdit_y_max_3d.setEnabled(True)
		
		self.lineTypeComboBox.setEnabled(False)
		self.opacityComboBox.setEnabled(True)
		self.exprDimLabel.setText("Z = ")

	def additional(self, box):
		self.DialogBox = box
		self.DialogBox.resize(470, 671)

		self.expr.setFocus()

		self.lineTypeComboBox.clear()
		solid = QtCore.QString("Solid")
		dashed = QtCore.QString("Dashed")
		dotted = QtCore.QString("Dotted")
		self.isSlided = False
		self.lineTypeComboBox.addItem(solid)
		self.lineTypeComboBox.addItem(dashed)
		self.lineTypeComboBox.addItem(dotted)
		self.lineTypeComboBox.setEnabled(True)

		self.opacityComboBox.clear()
		additive = QtCore.QString("additive")
		translucent = QtCore.QString("translucent")
		opaque = QtCore.QString("opaque")
		self.opacityComboBox.addItem(additive)
		self.opacityComboBox.addItem(translucent)
		self.opacityComboBox.addItem(opaque)
		self.opacityComboBox.setEnabled(False)

		self.connectBasicButtons()
		self.box = box
		self.fileNameRemoveButton.setStyleSheet('QPushButton {color: red;}')

		#For expression templates
		self.model = QtGui.QStandardItemModel(self.tempListView)
		self.tempListView.clicked.connect(self.clicked)
		#self.tempListView.doubleClicked.connect(self.doubleClicked)

		for template in self.templates:
			item = QtGui.QStandardItem(template[0])
			item.setEditable(False)
			self.model.appendRow(item)
		
		self.tempListView.setModel(self.model)

		self.constantsTableWidget.setFixedWidth(211)
		self.constantsTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		#expression templates

		if self.graph:
			self.lineEdit.setText(str(self.graph.name))
			self.doubleSpinBox.setValue(float(self.graph.lineWidth))

			pT = str(self.graph.lineType)
			if pT == "Dashed":
				self.lineTypeComboBox.setCurrentIndex(1)
			elif pT == "Dotted":
				self.lineTypeComboBox.setCurrentIndex(2)
			else:
				self.lineTypeComboBox.setCurrentIndex(0)

			oP = str(self.graph.opacity)
			if oP == "translucent":
				self.opacityComboBox.setCurrentIndex(1)
			elif oP == "opaque":
				self.opacityComboBox.setCurrentIndex(2)
			else:
				self.opacityComboBox.setCurrentIndex(0)

			if self.graph.expr:
				self.plotTypeWidget.setVisible(False)
				self.expr.setText(str(self.graph.expr))
				self.lineEdit_x_min_3d.setText(str(self.graph.xMin))
				self.lineEdit_x_max_3d.setText(str(self.graph.xMax))
				self.fileNameWidget.setVisible(False)
				self.radioButton.setChecked(True)
				self.lineTypeComboBox.setEnabled(True)
				self.opacityComboBox.setEnabled(False)
				if self.graph.dim == 3:
					self.exprDimLabel.setText("Z = ")
					self.lineEdit_y_min_3d.setEnabled(True)
					self.lineEdit_y_max_3d.setEnabled(True)
					self.lineEdit_y_min_3d.setText(str(self.graph.yMin))
					self.lineEdit_y_max_3d.setText(str(self.graph.yMax))
					self.radioButton_2.setChecked(True)
					self.lineTypeComboBox.setEnabled(False)
					self.opacityComboBox.setEnabled(True)
			else :
				self.filename = self.graph.filename
				if os.path.isfile(self.filename):
					self.isFileSelected = True
					self.expr.setEnabled(False)
					self.plotTypeWidget.setVisible(True)
					self.fileNameWidget.setVisible(True)
					self.fileNameLabel.setText(os.path.basename(str(self.graph.filename)))
					self.lineEdit_x_min_3d.setEnabled(False)
					self.lineEdit_x_max_3d.setEnabled(False)
					self.lineEdit_y_min_3d.setEnabled(False)
					self.lineEdit_y_max_3d.setEnabled(False)
					
					self.radioButton.setEnabled(False)
					self.radioButton_2.setEnabled(False)
					if self.graph.dim == 2:
						self.comboBox.clear()
						s1 = QtCore.QString("Line")
						s2 = QtCore.QString("Scatter")
						self.comboBox.addItem(s1)
						self.comboBox.addItem(s2)
						self.radioButton.setChecked(True)
						self.lineTypeComboBox.setEnabled(True)
						self.opacityComboBox.setEnabled(False)
					else:
						self.exprDimLabel.setText("Z = ")
						self.comboBox.clear()
						s1 = QtCore.QString("Surface")
						s2 = QtCore.QString("Scatter")
						self.comboBox.addItem(s1)
						self.comboBox.addItem(s2)
						self.radioButton_2.setChecked(True)
						self.lineTypeComboBox.setEnabled(False)
						self.opacityComboBox.setEnabled(True)

					if self.graph.plotType == "Scatter":
						self.comboBox.setCurrentIndex(1)
					else:
						self.comboBox.setCurrentIndex(0)
				else:
					self.isFileSelected = False
					self.plotTypeWidget.setVisible(False)
					self.fileNameLabel.setText("")

			self.colString = self.graph.colString
			styleSheet = "background-color: rgb" + str(self.colString)
			self.colorButton.setStyleSheet(styleSheet)
			
			self.box = box
		else:
			if self.filename:
				if os.path.isfile(self.filename):
					self.isFileSelected = True
					self.fileNameLabel.setText(os.path.basename(str(self.filename)))
					self.expr.clear()
					self.expr.setEnabled(False)
					self.lineEdit_x_min_3d.setEnabled(False)
					self.lineEdit_x_max_3d.setEnabled(False)
					self.lineEdit_y_min_3d.setEnabled(False)
					self.lineEdit_y_max_3d.setEnabled(False)

					self.radioButton.setEnabled(False)
					self.radioButton_2.setEnabled(False)

					self.plotTypeWidget.setVisible(True)
					self.fileNameWidget.setVisible(True)

					with open(self.filename) as fin:
						line = fin.readline().split()
						if len(line) == 2:
							self.radioButton.setChecked(True)
							self.exprDimLabel.setText("Y = ")
							self.comboBox.clear()
							s1 = QtCore.QString("Line")
							s2 = QtCore.QString("Scatter")
							self.comboBox.addItem(s1)
							self.comboBox.addItem(s2)
							self.lineTypeComboBox.setEnabled(True)
							self.opacityComboBox.setEnabled(False)

						elif len(line) == 3:
							self.exprDimLabel.setText("Z = ")
							self.radioButton_2.setChecked(True)
							self.comboBox.clear()
							s1 = QtCore.QString("Surface")
							s2 = QtCore.QString("Scatter")
							self.comboBox.addItem(s1)
							self.comboBox.addItem(s2)
							self.lineTypeComboBox.setEnabled(False)
							self.opacityComboBox.setEnabled(True)
					self.plotTypeWidget.setVisible(True)
					self.fileNameWidget.setVisible(True)
					
			else:
				self.lineEdit_x_min_3d.setText("-1")
				self.lineEdit_x_max_3d.setText("1")
				self.lineEdit_y_min_3d.setText("-1")
				self.lineEdit_y_max_3d.setText("1")
				self.isFileSelected = False
				
				self.plotTypeWidget.setVisible(False)
				self.fileNameWidget.setVisible(False)
				self.opacityComboBox.setEnabled(False)
			self.colString = QtGui.QColor(randint(0,255),randint(0,255),randint(0,255),255).getRgb()
	
	def clicked(self, index):
		item = self.model.itemFromIndex(index)
		self.constantsTableWidget.clear()
		for template in self.templates:
			if template[0] == item.text():
				if self.isFileSelected == False:
					if(template[2] == "2D"):
						self.show2DSettings()
					else:
						self.show3DSettings()
					self.expr.setText(template[1].replace("$",""))
					self.exprIndexText = template[1]

				self.constantsTableWidget.setColumnCount(2)
				self.constantsTableWidget.setRowCount(len(template)-3)
				
				flags = QtCore.Qt.ItemFlags()
				flags != QtCore.Qt.ItemIsEditable

				for i in xrange(3,len(template)):
					tempItem = QtGui.QTableWidgetItem(str(template[i]))
					flags != QtCore.Qt.ItemIsEditable
					tempItem.setFlags(flags)
					self.constantsTableWidget.setItem(i-3,0,tempItem)
				return

	def connectBasicButtons(self):
		## Numbers
		QtCore.QObject.connect(self.Button_0, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("0"))
		QtCore.QObject.connect(self.Button_1, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("1"))
		QtCore.QObject.connect(self.Button_2, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("2"))
		QtCore.QObject.connect(self.Button_3, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("3"))
		QtCore.QObject.connect(self.Button_4, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("4"))
		QtCore.QObject.connect(self.Button_5, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("5"))
		QtCore.QObject.connect(self.Button_6, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("6"))
		QtCore.QObject.connect(self.Button_7, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("7"))
		QtCore.QObject.connect(self.Button_8, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("8"))
		QtCore.QObject.connect(self.Button_9, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("9"))
		QtCore.QObject.connect(self.xButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("x"))
		QtCore.QObject.connect(self.yButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("y"))
		QtCore.QObject.connect(self.equalButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("="))
		QtCore.QObject.connect(self.decimalButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("."))

		## */+-
		QtCore.QObject.connect(self.multButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("*"))
		QtCore.QObject.connect(self.divButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("/"))
		QtCore.QObject.connect(self.addButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("+"))
		QtCore.QObject.connect(self.subButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("-"))
		
		##Delete
		QtCore.QObject.connect(self.delButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedDeleteButton())

		##Ac
		QtCore.QObject.connect(self.acButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedACButton())

		## Constants
		QtCore.QObject.connect(self.eButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("e"))
		QtCore.QObject.connect(self.piButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("pi"))
		QtCore.QObject.connect(self.leftParenthesisButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("("))
		QtCore.QObject.connect(self.rightParenthesisButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton(")"))

		## Specials
		QtCore.QObject.connect(self.sqrButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("^2"))
		QtCore.QObject.connect(self.xInverseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedBasicButton("^(-1)"))
		QtCore.QObject.connect(self.expButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("e^"))
		QtCore.QObject.connect(self.xPowerYButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("^"))
		QtCore.QObject.connect(self.logButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("log"))
		QtCore.QObject.connect(self.sinButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("sin"))
		QtCore.QObject.connect(self.cosButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("cos"))
		QtCore.QObject.connect(self.tanButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("tan"))
		QtCore.QObject.connect(self.asinButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("arcsin"))
		QtCore.QObject.connect(self.acosButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("arccos"))
		QtCore.QObject.connect(self.atanButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("arctan"))
		QtCore.QObject.connect(self.sqrtButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("sqrt"))
		QtCore.QObject.connect(self.sinhButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("sinh"))
		QtCore.QObject.connect(self.coshButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("cosh"))
		QtCore.QObject.connect(self.tanhButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("tanh"))
		QtCore.QObject.connect(self.asinhButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("arcsinh"))
		QtCore.QObject.connect(self.acoshButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("arccosh"))
		QtCore.QObject.connect(self.atanhButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("arctanh"))
		QtCore.QObject.connect(self.absButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedButtonWithCursorChange("abs"))
	
		QtCore.QObject.connect(self.colorButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedColorButton())
		QtCore.QObject.connect(self.plotButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedPlotButton())
		QtCore.QObject.connect(self.uploadFileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : self.pressedUploadFileButton())

		# Radio Buttons
		QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.pressedRadio2D)
		QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.pressedRadio3D)

		#fileNameRemoveButton
		QtCore.QObject.connect(self.fileNameRemoveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.pressedFileNameRemoveButton)

		#Add New Expression
		QtCore.QObject.connect(self.addExprButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.pressedAddExprButton)

		#Table Widget
		self.constantsTableWidget.itemChanged.connect(self.constantsTableWidgetItemChanged)

	def constantsTableWidgetItemChanged(self, tableItem):
		if self.isFileSelected == False:
			col = tableItem.column()
			row = tableItem.row()
			str2 = str(self.constantsTableWidget.item(row, col).text())
			str1 = str(self.constantsTableWidget.item(row, 0).text())
			if(col == 0):
				return
			self.replaceConstants()
			return

	def replaceConstants(self):
		tempExprStr = self.exprIndexText

		for row in xrange(0,self.constantsTableWidget.rowCount()):
			if(self.constantsTableWidget.item(row, 1) == None or self.constantsTableWidget.item(row, 0) == None):
				continue
			str2 = str(self.constantsTableWidget.item(row, 1).text())
			str1 = str(self.constantsTableWidget.item(row, 0).text())
			tempExprStr = tempExprStr.replace("$"+str1+"$", str2)
		self.expr.setText(tempExprStr.replace("$",""))
		return

	def pressedAddExprButton(self):
		if(self.isSlided == False):
			self.DialogBox.resize(self.DialogBox.width()+230, self.DialogBox.height())
			self.expr.resize(self.expr.width()+230, self.expr.height())
			self.isSlided = True
		else:
			self.DialogBox.resize(self.DialogBox.width()-230, self.DialogBox.height())
			self.expr.resize(self.expr.width()-230, self.expr.height())
			self.isSlided = False

	def pressedFileNameRemoveButton(self):
		self.isFileSelected = False
		self.fileNameWidget.setVisible(False)
		self.expr.setEnabled(True)
		self.radioButton.setEnabled(True)
		self.radioButton_2.setEnabled(True)
		self.lineEdit_x_min_3d.setEnabled(True)
		self.lineEdit_x_max_3d.setEnabled(True)
		self.lineEdit_y_min_3d.setEnabled(True)
		self.lineEdit_y_max_3d.setEnabled(True)
		self.plotTypeWidget.setVisible(False)

	def pressedRadio2D(self):
		self.lineEdit_y_min_3d.setDisabled(1)
		self.lineEdit_y_max_3d.setDisabled(1)
		self.exprDimLabel.setText("Y = ")
		self.lineTypeComboBox.setEnabled(True)
		self.opacityComboBox.setEnabled(False)


	def pressedRadio3D(self):
		self.lineEdit_y_min_3d.setDisabled(0)
		self.lineEdit_y_max_3d.setDisabled(0)
		self.exprDimLabel.setText("Z = ")
		self.lineTypeComboBox.setEnabled(False)
		self.opacityComboBox.setEnabled(True)

	def pressedBasicButton(self, str):
		if self.isFileSelected == False:
			strLength = len(str)
			cursor = self.expr.textCursor()
			text = self.expr.toPlainText()
			placeCursor = cursor.position()
			text.insert(cursor.position(),str)
			self.expr.setText(text)

			cursor.setPosition(placeCursor+strLength, QtGui.QTextCursor.MoveAnchor)
			self.expr.setTextCursor(cursor)

			self.expr.setFocus()
	
	def pressedButtonWithCursorChange(self, str):
		if self.isFileSelected == False:
			lengthStr = len(str)
			cursor = self.expr.textCursor()
			str+="()"
			text = self.expr.toPlainText()
			placeCursor = cursor.position()
			text.insert(cursor.position(),str)
			self.expr.setText(text)

			cursor.setPosition(placeCursor+1+lengthStr, QtGui.QTextCursor.MoveAnchor)
			self.expr.setTextCursor(cursor)

			self.expr.setFocus()

	def pressedDeleteButton(self):
		if self.isFileSelected == False:
			cursor = self.expr.textCursor()
			cursorPosition = cursor.position()-1

			if cursorPosition<0:
				cursor.setPosition(0, QtGui.QTextCursor.MoveAnchor)
				self.expr.setTextCursor(cursor)
				self.expr.setFocus()
				return

			text = self.expr.toPlainText()
			text= text[0:cursorPosition]+text[cursorPosition+1:]
			self.expr.setText(text)

			cursor.setPosition(cursorPosition, QtGui.QTextCursor.MoveAnchor)
			self.expr.setTextCursor(cursor)
			self.expr.setFocus()


	def pressedACButton(self):
		if self.isFileSelected == False:
			self.expr.setText("")
			self.expr.setFocus()

	def pressedPlotButton(self):
		try:
			ret = None
			print self.isFileSelected
			print self.filename
			if(self.isFileSelected == False):
				if self.radioButton.isChecked():
					x_min, x_max, name, colString, lineWidth, lineType = self.get_2d_values()
					# print x_min, x_max, name, colString, lineWidth
					_expr = str(self.expr.toPlainText())
					if name == "":
						name = _expr
					if x_min > x_max:
						QtGui.QMessageBox.critical(self.box, "Error", "X-Min is greater than X-Max", QtGui.QMessageBox.Ok)
						return
					
					graph = Graph(name = name, expr=_expr, dim=2, xMin = x_min, xMax = x_max, colString = colString, lineWidth=lineWidth, lineType=lineType)
					# Error
					if graph.points == None:
						QtGui.QMessageBox.critical(self.box, "Error", "Invalid Expression", QtGui.QMessageBox.Ok)
						return
						# raise Exception()
						# TODO

					else:
						self.plot2D(graph)
						
					
				if self.radioButton_2.isChecked():
					x_min, x_max, y_min, y_max, name, colString, lineWidth, opacity = self.get_values_3d()
					# print x_min, x_max, y_min, y_max, name, colString, lineWidth
					_expr = str(self.expr.toPlainText())
					if name == "":
						name = _expr
					graph = Graph(expr=_expr, dim=3, xMin = x_min, xMax = x_max, yMin = y_min, yMax = y_max, name = name, colString = colString, lineWidth=lineWidth, opacity=opacity)

					if x_min > x_max:
						QtGui.QMessageBox.critical(self.box, "Error", "X-Min is greater than X-Max", QtGui.QMessageBox.Ok)
						return
					if y_min > y_max:
						QtGui.QMessageBox.critical(self.box, "Error", "Y-Min is greater than Y-Max", QtGui.QMessageBox.Ok)
						return

					if graph.points == None:
						QtGui.QMessageBox.critical(self.box, "Error", "Invalid Expression", QtGui.QMessageBox.Ok)
						return
						# raise Exception()
						# TODO

					else:
						self.plot3D(graph)
						
			else:
				filename = self.filename
				name = self.lineEdit.text()
				if name == "":
					name = os.path.basename(str(filename))
				graph = Graph(name = name, filename = self.filename, colString = self.colString, lineWidth=float(self.doubleSpinBox.text()), plotType=str(self.comboBox.currentText()), lineType=str(self.lineTypeComboBox.currentText()), opacity=str(self.opacityComboBox.currentText()))
				print graph
				if graph.points == None:
					print "1"
					# print traceback.print_exc()
					errorMsg = graph.errorMsg
					ret = QtGui.QMessageBox.critical(None, "Error", "File error: "+errorMsg, QtGui.QMessageBox.Ok)
					return
					# TODO : File corrupt
				else:
					print "2"
					dim = len(graph.points)
					if dim == 2:
						graph.dim = 2
						self.plot2D(graph)
					else:
						graph.dim = 3
						self.plot3D(graph)

			if self.graph:
				if self.callingTabWidgetUI.plotType == 2:
					self.callingTabWidgetUI.w.removeItem(self.callingTabWidgetUI.listWidget.itemWidget(self.callingTabWidgetUI.listWidget.currentItem()).ui.item)
				else:
					self.callingTabWidgetUI.graphicsView_3d.removeItem(self.callingTabWidgetUI.listWidget.itemWidget(self.callingTabWidgetUI.listWidget.currentItem()).ui.item)
				self.callingTabWidgetUI.listWidget.takeItem(self.callingTabWidgetUI.listWidget.row(self.callingTabWidgetUI.listWidget.currentItem()))
				
			if ret == None:
				self.box.close()		
		except:
			traceback.print_exc()
			QtGui.QMessageBox.critical(self.box, "Error", "One of the parameters is not in the desired format", QtGui.QMessageBox.Ok)

	def plot2D(self, graph):
		if self.graph:
			self.callingTabWidgetUI.legend.removeItem(self.graph.name)
		""" Plots 2D curve(Line or Scatter) """
		x = graph.points[0]
		y = graph.points[1]

		lineType = str(graph.lineType)
		if lineType == "Dotted":
			style=QtCore.Qt.DotLine
		elif lineType == "Dashed":
			style=QtCore.Qt.DashLine
		else:
			style=QtCore.Qt.SolidLine

		pen = pg.mkPen(color=graph.colString, width=graph.lineWidth, style=style)
		if graph.plotType == None or graph.plotType == "Line":
			plot = pg.PlotCurveItem()
			plot.setData(x=x, y=y, pen=pen, name=graph.name)
		else:
			plot = pg.ScatterPlotItem()
			plot.setData(x=x, y=y, pen=pen, name=graph.name)
		
		if self.callingTabWidgetUI.plotType == None or self.callingTabWidgetUI.plotType == 2:
			self.callingTabWidgetUI.plotType = 2
			self.callingTabWidgetUI.w.addItem(plot)
			self.callingTabWidgetUI.graphicsView_2d.setVisible(True)
			self.callingTabWidgetUI.graphicsView_3d.setVisible(False)			
			self.callingTabWidgetUI.addItemToList(plot, graph)
		else : 
			newTab = QtGui.QWidget()
			ui_newTab = PlotterWidget(self.callingTabWidgetUI.parent)
			newTab.ui = ui_newTab			
			ui_newTab.setupUi(newTab)
			ui_newTab.additional(newTab)
			self.callingTabWidgetUI.parent.addTab(newTab, 'Tab')
			self.callingTabWidgetUI.parent.tab.movePlusButton()
			self.callingTabWidgetUI.parent.tab.setCurrentIndex(len(self.callingTabWidgetUI.parent.tab)-1)
			ui_newTab.plotType = 2			
			ui_newTab.w.addItem(plot)
			ui_newTab.graphicsView_2d.setVisible(True)
			ui_newTab.graphicsView_3d.setVisible(False)
			ui_newTab.addItemToList(plot, graph)
		self.lineEdit.clear()
		self.expr.clear()

	def plot3D(self, graph):
		""" Plots 3D curve(Line or Scatter) """
		x = graph.points[0]	
		y = graph.points[1]
		z = graph.points[2]		
		
		if graph.plotType == None or graph.plotType == "Surface":
			zipped = sorted(zip(x,y,z)) #Sorts based on 1st,2nd and then 3rd item

			xSurface = sorted(list(set(x)))
			ySurface = sorted(list(set(y)))
			zSurface = []
			i = 0
			for xS in xSurface:
				if i==len(zipped):
					break
				zList=[]
				for j in range(len(ySurface)):
					if zipped[i][0] == xS:
						if zipped[i][1] == ySurface[j]:
							zList.append(zipped[i][2])
							i+=1
						else:
							zList.append(float('NaN'))
					else:
						zList.append(float('NaN'))
				zSurface.append(np.asarray(zList))
					
			normalizedColString = (graph.colString[0]/255., graph.colString[1]/255., graph.colString[2]/255., graph.colString[3]/255.)
			if graph.expr:
				p2 = gl.GLSurfacePlotItem(x=np.asarray(xSurface), y=np.asarray(ySurface), z=np.asarray(zSurface), color=normalizedColString, shader="shaded", glOptions=str(graph.opacity))
			else:
				p2 = gl.GLSurfacePlotItem(x=np.asarray(xSurface), y=np.asarray(ySurface), z=np.asarray(zSurface), color=normalizedColString, glOptions=str(graph.opacity))
		else:
			pos = np.empty((len(graph.points[0]), 3))
			for i in range(len(graph.points[0])):
				pos[i] = (x[i], y[i], z[i])
			normalizedColString = (graph.colString[0]/255., graph.colString[1]/255., graph.colString[2]/255., graph.colString[3]/255.)
			p2 = gl.GLScatterPlotItem(pos=pos, size=graph.lineWidth*10, color=normalizedColString, pxMode=True, glOptions=str(graph.opacity))
			
		if self.callingTabWidgetUI.plotType == None or self.callingTabWidgetUI.plotType == 3:
			self.callingTabWidgetUI.plotType = 3			
			self.callingTabWidgetUI.graphicsView_3d.addItem(p2)		
			self.callingTabWidgetUI.graphicsView_3d.setVisible(True)
			self.callingTabWidgetUI.graphicsView_2d.setVisible(False)
			self.callingTabWidgetUI.addItemToList(p2, graph)

		else : 
			newTab = QtGui.QWidget()
			ui_newTab = PlotterWidget(self.callingTabWidgetUI.parent)
			newTab.ui = ui_newTab
			ui_newTab.setupUi(newTab)
			ui_newTab.additional(newTab)
			self.callingTabWidgetUI.parent.addTab(newTab, 'Tab')
			self.callingTabWidgetUI.parent.tab.movePlusButton()
			self.callingTabWidgetUI.parent.tab.setCurrentIndex(len(self.callingTabWidgetUI.parent.tab)-1)
			ui_newTab.plotType = 3
			
			
			ui_newTab.graphicsView_3d.addItem(p2)
			ui_newTab.graphicsView_3d.setVisible(True)
			ui_newTab.graphicsView_2d.setVisible(False)
			ui_newTab.addItemToList(p2, graph)
			
		self.expr.clear()
	def pressedUploadFileButton(self):
		self.filename = QtGui.QFileDialog.getOpenFileName()
		if os.path.isfile(self.filename):
			self.isFileSelected = True
			self.fileNameLabel.setText(os.path.basename(str(self.filename)))
			self.expr.clear()
			self.expr.setEnabled(False)
			self.lineEdit_x_min_3d.setEnabled(False)
			self.lineEdit_x_max_3d.setEnabled(False)
			self.lineEdit_y_min_3d.setEnabled(False)
			self.lineEdit_y_max_3d.setEnabled(False)

			self.radioButton.setEnabled(False)
			self.radioButton_2.setEnabled(False)

			self.plotTypeWidget.setVisible(True)
			self.fileNameWidget.setVisible(True)

			with open(self.filename) as fin:
				line = fin.readline().split()
				if len(line) == 2:
					self.radioButton.setChecked(True)
					self.exprDimLabel.setText("Y = ")
					self.comboBox.clear()
					s1 = QtCore.QString("Line")
					s2 = QtCore.QString("Scatter")
					self.comboBox.addItem(s1)
					self.comboBox.addItem(s2)

					self.opacityComboBox.setEnabled(False)


				elif len(line) == 3:
					self.exprDimLabel.setText("Z = ")
					self.radioButton_2.setChecked(True)
					self.comboBox.clear()
					s1 = QtCore.QString("Surface")
					s2 = QtCore.QString("Scatter")
					self.comboBox.addItem(s1)
					self.comboBox.addItem(s2)

					self.opacityComboBox.setEnabled(True)



	def pressedColorButton(self):
		col = QtGui.QColorDialog.getColor()
		self.colString = col.getRgb()
		print col.getRgb(), " Color"
		styleSheet = "background-color: rgb" + str(self.colString)
		self.colorButton.setStyleSheet(styleSheet)	
	
	def get_2d_values(self):
		try:
			name = str(self.lineEdit.text())
			x_min = float(self.lineEdit_x_min_3d.text())
			x_max = float(self.lineEdit_x_max_3d.text())
			colString = self.colString
			lineWidth = float(self.doubleSpinBox.text())
			lineType = str(self.lineTypeComboBox.currentText())
			return (x_min, x_max, name, colString, lineWidth, lineType)
		except ValueError:
			pass

	def get_values_3d(self):
		try:
			name = str(self.lineEdit.text())
			x_min = float(self.lineEdit_x_min_3d.text())
			x_max = float(self.lineEdit_x_max_3d.text())
			y_min = float(self.lineEdit_y_min_3d.text())
			y_max = float(self.lineEdit_y_max_3d.text())
			colString = self.colString
			lineWidth = float(self.doubleSpinBox.text())
			opacity = str(self.opacityComboBox.currentText())
			return (x_min, x_max, y_min, y_max, name, colString, lineWidth, opacity)
		except ValueError:
			pass
		
class TabBarPlus(QtGui.QTabBar):

	plusClicked = QtCore.Signal()

	def __init__(self):
		super(TabBarPlus, self).__init__()

		# Plus Button
		self.plusButton = QtGui.QPushButton("+")
		self.plusButton.setParent(self)
		self.plusButton.setMaximumSize(25, 33)
		self.plusButton.setMinimumSize(25, 33)
		self.plusButton.clicked.connect(self.plusClicked.emit)
		self.plusButton.setVisible(True)
	# end Constructor

	def sizeHint(self):
		sizeHint = QtGui.QTabBar.sizeHint(self) 
		width = sizeHint.width()
		height = sizeHint.height()
		return QtCore.QSize(width+25, height)


	def movePlusButton(self):
		size = 0
		for i in range(self.count()):
			size += self.tabRect(i).width()

		h = self.geometry().top()

		self.plusButton.move(size, h)

	def moveBackPlusButton(self):
		size = 0
		lastSize = 0
		for i in range(self.count()):
			size += self.tabRect(i).width()
			lastSize = self.tabRect(i).width()

		h = self.geometry().top()

		self.plusButton.move(size-lastSize, h)
	# end movePlusButton
# end class MyClass

class ViewWidget3D(gl.GLViewWidget):
	def __init__(self, x, tab):
		super(ViewWidget3D, self).__init__(x)
		self.tab = tab
		self.setAcceptDrops(True)
	
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls:
			event.accept()
		else:
			event.ignore()
	def dropEvent(self, event):
		url = event.mimeData().urls()[0]
		filename = str(url.toLocalFile())
		self.tab.fileDraggedIn(filename)
		
	def save_file(self):
		file_types="PNG (*.png);;EPS (*.eps);;PDF (*.pdf);;BMP (*.bmp)"
		filename, filter = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save file', '', file_types)
		if filter == "PNG (*.png)":
			if not str(filename).endswith('.png'):
				filename = filename+".png"
			self.grabFrameBuffer().save(filename)

		if filter == "EPS (*.eps)":
			if not str(filename).endswith('.eps'):
				filename = filename + ".eps"
			self.grabFrameBuffer().save("/tmp/test.png")
			os.system("convert /tmp/test.png "+str(filename))
		if filter == "PDF (*.pdf)":
			if not str(filename).endswith('.pdf'):
				filename = filename+".pdf"
			self.grabFrameBuffer().save("/tmp/test.png")
			os.system("convert /tmp/test.png " + str(filename))
		if filter == "BMP (*.bmp)":
			if not str(filename).endswith('.bmp'):
				filename = filename+".bmp"
			self.grabFrameBuffer().save("/tmp/test.png")
			os.system("convert /tmp/test.png " + str(filename))
		#if filter == "SVG (*.svg)":
		#	if not str(filename).endswith('.svg'):
		#		filename = filename".svg"
		#	self.grabFrameBuffer().save("/tmp/test.png")
		#	os.system("convert /tmp/test.png "str(filename))
   
		
	def changeBackground3d(self):
		col = QtGui.QColorDialog.getColor()
		self.setBackgroundColor(col)
	def contextMenuEvent(self, event):
		menu = QtGui.QMenu()
		exportAction = menu.addAction('Export...')
		exportAction.triggered.connect(self.save_file)
		#changeBackgroundAction = menu.addAction('Change background...')
		#changeBackgroundAction.triggered.connect(self.changeBackground3d)
		menu.exec_(event.globalPos()) 

class MyGraphicsLayoutWidget(pg.GraphicsLayoutWidget):
	def __init__(self, x, tab):
		self.plot=None
		self.tab = tab
		super(MyGraphicsLayoutWidget, self).__init__(x)
		self.setAcceptDrops(True)
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls:
			event.accept()
			url = event.mimeData().urls()[0]
			filename = str(url.toLocalFile())
			self.tab.fileDraggedIn(filename)
		else:
			event.ignore()
	def leaveEvent(self, event):
		self.tab.clearStatusBar()
class ChangeAxisDialog(changeAxisDialog.Ui_Dialog):
	def __init__(self, tab):
		super(ChangeAxisDialog, self).__init__()
		self.tab = tab
	def additional(self):
		self.lineEdit_x_title.setText(self.tab.w.getAxis('bottom').labelText)
		self.lineEdit_y_title.setText(self.tab.w.getAxis('left').labelText)
		if self.tab.w.getAxis('bottom').labelUnits:
			self.lineEdit_x_unit.setText(self.tab.w.getAxis('bottom').labelUnits)
		if self.tab.w.getAxis('left').labelUnits:
			self.lineEdit_y_unit.setText(self.tab.w.getAxis('left').labelUnits)
		self.buttonBox.accepted.connect(self.changeAxisLabels)
		
	def changeAxisLabels(self):
		if self.lineEdit_x_unit.text() == "":
			self.tab.w.getAxis('bottom').setLabel(self.lineEdit_x_title.text())
		else :
			self.tab.w.getAxis('bottom').setLabel(self.lineEdit_x_title.text(), units=self.lineEdit_x_unit.text())
		if self.lineEdit_y_unit.text() == "":
			self.tab.w.getAxis('left').setLabel(self.lineEdit_y_title.text())
		else :
			self.tab.w.getAxis('left').setLabel(self.lineEdit_y_title.text(), units=self.lineEdit_y_unit.text())
		

class CustomTabWidget(QtGui.QTabWidget):

	def __init__(self, parent, window):
		super(CustomTabWidget, self).__init__(parent)

		# Tab Bar
		self.tab = TabBarPlus()
		self.setTabBar(self.tab)

		# Properties
		#self.setMovable(True)
		self.setTabsClosable(True)

		# Signals
		self.tab.plusClicked.connect(self.addCustomTab)
		#self.tab.tabMoved.connect(self.moveTab)
		self.tabCloseRequested.connect(self.removeTab)
		self.window = window
		self.parent = parent

	def addCustomTab(self):
		newTab = QtGui.QWidget()
		ui_newTab = PlotterWidget(self)
		newTab.ui = ui_newTab
		ui_newTab.setupUi(newTab)
		ui_newTab.additional(newTab)
		self.addTab(newTab, 'Tab')
		self.tab.movePlusButton()
		self.tab.setCurrentIndex(len(self.tab)-1)
		return ui_newTab

	def removeTab(self,currentIndex):
		print "ssss"+str(currentIndex)	
		if len(self.tab) == 1:
			reply = QtGui.QMessageBox.question(self.parent, "Exiting", "Are you sure you want to exit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				QtGui.QApplication.quit()
			else:
				return
				
		widget = self.widget(currentIndex)
		if widget is not None:
		    widget.deleteLater()
		self.tab.moveBackPlusButton()
		# self.tab.removeTab(currentIndex)

	def addPlot(self):
		self.currentWidget().ui.addPlotPressed()
class StatusBar(QtGui.QStatusBar):
	def __init__(self):
		super(StatusBar, self).__init__()
		self.label = QtGui.QLabel("")
		self.addWidget(self.label, 1)
		
class HarryPlotter(Ui_MainWindow):
	def __init__(self, win, app):
		super(HarryPlotter, self).__init__()
		self.window = win
		self.app = app
	
	def additional(self, x):
		self.tabWidget = CustomTabWidget(self.centralwidget, self)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

		self.statusBar = StatusBar()
		self.window.setStatusBar(self.statusBar)
		self.connectActions()

		QtCore.QObject.connect(self.action_About, QtCore.SIGNAL(_fromUtf8("triggered()")), self.pressedAbout)
		QtCore.QObject.connect(self.actionBlack, QtCore.SIGNAL(_fromUtf8("triggered()")), self.pressedBlack)
		QtCore.QObject.connect(self.actionWhite, QtCore.SIGNAL(_fromUtf8("triggered()")), self.pressedWhite)

	def pressedBlack(self):
		self.actionBlack.setChecked(True)
		self.actionWhite.setChecked(False)
		import qdarkstyle	
		self.app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

	def pressedWhite(self):
		self.actionBlack.setChecked(False)
		self.actionWhite.setChecked(True)
		self.app.setStyleSheet("")

	def pressedAbout(self):
		QtGui.QMessageBox.about(self.window,
					"About Harry Plotter",
					"""<span style = "font:16px">\nHarryPlotter is the ultimate technical graphing package available. This easy-to-use, powerful, dynamic program will help you create superior publication-quality professional graphs in minutes! Wow your audience every time they see your graphs.<br><br>
					HarryPlotter is a feature-rich yet easy-to-use graph plotting and data visualization software suitable for students, engineers and everybody who needs to work with 2D and 3D graphs.<br><br>
					With HarryPlotter you can easily plot the equation and table-based graphs, zoom them, rotate, and do a lot more. You can draw unlimited number of graphs in one coordinate system to visualize and analyze the domains of functions and their intercepts.<br><br>
					The software uses a multiple document interface so that you can work on multiple solutions simultaneously. There is a fully featured scientific calculator which includes a very useful integrated variables and functions list window so that you can easily track defined variables and functions.<br><br>
					This a powerful and versatile mathematical software that anyone working on mathematical projects will find useful.</span>""")


	def connectActions(self):
		self.actionNew_Tab.triggered.connect(self.tabWidget.addCustomTab)
		self.actionNew_Tab.setShortcut('Ctrl+T')
		
		self.actionAdd_Plot.triggered.connect(self.tabWidget.addPlot)
		self.actionAdd_Plot.setShortcut('Ctrl+N')

		self.actionClose_Tab.triggered.connect(lambda : self.tabWidget.removeTab(self.tabWidget.currentIndex()))
		self.actionClose_Tab.setShortcut('Ctrl+W')		
		
		self.actionAxisLabels.triggered.connect(self.changeAxisLabels)
	
	def changeAxisLabels(self):
		if self.tabWidget.currentWidget().ui.plotType == 2:
			box = QtGui.QDialog()
			box_ui = ChangeAxisDialog(self.tabWidget.currentWidget().ui)
			box_ui.setupUi(box)
			box_ui.additional()
			import qdarkstyle	
			box.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
			box.exec_()
				
	def restoreFromOutside(self, restoreEarlier):
		if restoreEarlier == True:
			self.restore()
		else:
			self.tabWidget.addCustomTab()


	def restore(self):
		with open(".json.txt") as f:
			for line in f:
				self.openTab(line)
		
	def openTab(self, line):
		dicOuter = json.loads(str(line))
		tab = self.tabWidget.addCustomTab()
		x_title = str(dicOuter["x_axis_label"])
		y_title = str(dicOuter["y_axis_label"])
		x_unit = "" if str(dicOuter["x_axis_unit"])=="None" else str(dicOuter["x_axis_unit"])
		y_unit = "" if str(dicOuter["y_axis_unit"])=="None" else str(dicOuter["y_axis_unit"])
		
		tab.w.getAxis('bottom').setLabel(x_title, units=x_unit)
		tab.w.getAxis('left').setLabel(y_title, units=y_unit)
		
		dic = dicOuter["plots"]
		for i in range(len(dic)):
			expr = None if dic[i]["expr"]=="None" else str(dic[i]["expr"])
			name = dic[i]["name"]
			filename = None if dic[i]["filename"]=="None" else str(dic[i]["filename"])
			xMin = None if dic[i]["xMin"]=="None" else float(dic[i]["xMin"])
			xMax = None if dic[i]["xMax"]=="None" else float(dic[i]["xMax"])
			yMin = None if dic[i]["yMin"]=="None" else float(dic[i]["yMin"])
			yMax = None if dic[i]["yMax"]=="None" else float(dic[i]["yMax"])
			dim = None if dic[i]["dim"]=="None" else  int(dic[i]["dim"])
			plotType = None if dic[i]["plotType"]=="None" else  str(dic[i]["plotType"])
			#color = dic[i]["color"]
			lineType = dic[i]["lineType"]
			lineWidth = None if dic[i]["lineWidth"]=="None" else float(dic[i]["lineWidth"])
			colString = dic[i]["colString"]
			opacity = dic[i]["opacity"]
			tup = literal_eval(colString)
			colString = (tup[0], tup[1], tup[2], tup[3])
			graph = Graph(expr=expr, name=name, filename=filename, xMin=xMin, xMax=xMax, yMin=yMin, yMax=yMax, dim=dim, plotType=plotType, lineType=lineType, lineWidth=lineWidth, colString=colString, opacity=opacity)
			tab.drawGraph(graph)	

class PlotterWidget(Ui_Form):
	def __init__(self, parent):
		super(PlotterWidget, self).__init__()
		self.parent = parent
		self.plotType = None
		self.parent.window.statusBar.label.setText("")
	def additional(self, widget):
		self.graphicsView_2d = MyGraphicsLayoutWidget(widget, self)
		self.graphicsView_2d.setObjectName(_fromUtf8("graphicsView_2d"))
		self.gridLayout.addWidget(self.graphicsView_2d, 0, 0, 2, 1)

		self.graphicsView_2d.setVisible(True)
		self.w = self.graphicsView_2d.addPlot()
		
		self.actionBackground2d = QtGui.QAction(widget)
		self.actionBackground2d.setObjectName(_fromUtf8("actionBackground"))
		self.actionBackground2d.triggered.connect(self.changeBackground2d)
		self.actionBackground2d.setText("Change background colour...")

		self.actionLines = QtGui.QAction(widget)
		self.actionLines.setObjectName(_fromUtf8("actionBackground"))
		self.actionLines.triggered.connect(self.hideLines)
		self.actionLines.setText("Hide cursor lines")

		self.linesVisible = True

		self.w.ctrlMenu = [self.actionBackground2d, self.actionLines, self.w.ctrlMenu]
		self.w.getAxis('left').setLabel('Y Axis', units=None)
		self.w.getAxis('bottom').setLabel('X Axis', units=None)
		self.legend = self.w.addLegend()
		
		self.graphicsView_3d = ViewWidget3D(widget, self)
		self.graphicsView_3d.setObjectName(_fromUtf8("graphicsView_3d"))
		self.gridLayout.addWidget(self.graphicsView_3d, 0, 0, 2, 1)

		self.vLine = pg.InfiniteLine(angle=90, movable=False)
		self.hLine = pg.InfiniteLine(angle=0, movable=False)
		self.w.addItem(self.vLine, ignoreBounds=True)
		self.w.addItem(self.hLine, ignoreBounds=True)
		#   for 3d
		self.graphicsView_3d.setVisible(False)
		
		self.graphicsView_3d.setWindowTitle('pyqtgraph example: GLSurfacePlot')
		self.graphicsView_3d.setCameraPosition(distance=50)
		
		gx = gl.GLGridItem()
		gx.rotate(90, 0, 1, 0)
		gx.translate(-10, 0, 0)
		self.graphicsView_3d.addItem(gx)
		gy = gl.GLGridItem()
		gy.rotate(90, 1, 0, 0)
		gy.translate(0, -10, 0)
		self.graphicsView_3d.addItem(gy)
		gz = gl.GLGridItem()
		gz.translate(0, 0, -10)
		self.graphicsView_3d.addItem(gz)
		
		axis = gl.GLAxisItem()
		axis.setSize(x=100, y=100, z=100)
		self.graphicsView_3d.addItem(axis)
		self.w.scene().sigMouseMoved.connect(self.mouseMoved)
		self.w.scene().sigMouseClicked.connect(self.mouseClicked)
		self.addPlotButton.clicked.connect(self.addPlotPressed)
		
		self.listWidget.itemDoubleClicked.connect(self.itemDoubleClicked)
		
	def hideLines(self):
		#print self.hLine.isVisible()
		#self.hLine.setVisible(not self.hLine.isVisible())
		#self.vLine.setVisible(not self.vLine.isVisible())
		self.linesVisible = not self.linesVisible
		if self.linesVisible == True:
			self.actionLines.setText("Hide cursor lines")
		else:
			self.actionLines.setText("Show cursor lines")

	def changeBackground2d(self):
		col = QtGui.QColorDialog.getColor()
		self.graphicsView_2d.setBackground(col)
		
	@QtCore.pyqtSlot()
	def addPlotPressed(self):
		box = QtGui.QDialog()
		box_ui = PlotBox(self)
		box_ui.setupUi(box)
		box_ui.additional(box)
		box.exec_()
	
	def mouseClicked(self, evt):
		evt = evt.scenePos().toQPoint()
		if self.w.sceneBoundingRect().contains(evt):
			mousePoint = self.w.vb.mapSceneToView(evt)
			for item in self.w.scene().items():	
				if isinstance(item, pg.PlotCurveItem):
					if item.mouseShape().contains(mousePoint):
						QtGui.QToolTip.showText(evt, item.name())
						
	def mouseMoved(self,evt):
		if self.w.sceneBoundingRect().contains(evt):
			mousePoint = self.w.vb.mapSceneToView(evt)
			self.vLine.setPos(mousePoint.x())
			self.hLine.setPos(mousePoint.y())
			if self.linesVisible == True:
				self.vLine.setVisible(True)
				self.hLine.setVisible(True)
			else:
				self.vLine.setVisible(False)
				self.hLine.setVisible(False)
			self.parent.window.statusBar.label.setText("x : "+str(mousePoint.x())+" y : "+str(mousePoint.y()))
		else:
			self.clearStatusBar()	
	def clearStatusBar(self):
		self.vLine.setVisible(False)
		self.hLine.setVisible(False)
		self.parent.window.statusBar.label.setText("")
		
			
	def itemDoubleClicked(self, item):
		box = QtGui.QDialog()
		box_ui = PlotBox(self,  self.listWidget.itemWidget(item).ui.graph)
		box_ui.setupUi(box)
		box_ui.additional(box)
		box.exec_()
	
	def fileDraggedIn(self, filename):
		box = QtGui.QDialog()
		box_ui = PlotBox(self,  graph=None, filename=filename)
		print filename
		box_ui.setupUi(box)
		box_ui.additional(box)
		box.exec_()
		
	def getJson(self):
		json = "{\"plots\":["
		for i in range(self.listWidget.count()):
			json = json + self.listWidget.itemWidget(self.listWidget.item(i)).ui.getJson() + ","
		if self.listWidget.count() > 0:
			json = json[:-1]
		json = json + "], \"x_axis_label\":\""+str(self.w.getAxis('bottom').labelText)+"\", \"x_axis_unit\":\""+str(self.w.getAxis('bottom').labelUnits)+"\", \"y_axis_label\":\""+str(self.w.getAxis('left').labelText)+"\", \"y_axis_unit\":\""+str(self.w.getAxis('left').labelUnits)+"\"}"
		return json
		
	def addItemToList(self, plot, graph):
		item = QtGui.QListWidgetItem()
		item_widget = QtGui.QWidget()
		ui_item_form = ListItem(plot, self, item, graph)
		item_widget.ui = ui_item_form
		ui_item_form.setupUi(item_widget)
		ui_item_form.additional()
		textStyle = "<span style =\"color: rgb" + str(graph.colString)+"\">" + graph.name +"<br>--------------------</span>"
		ui_item_form.label.setText(textStyle)
		# styleSheet = "background-color: rgb" + str(graph.colString)
		# ui_item_form.widget.setStyleSheet(styleSheet)
		self.listWidget.addItem(item)
		self.listWidget.setItemWidget(item, item_widget)
		item.setSizeHint(QtCore.QSize(0,40))

	def drawGraph(self, graph):
		if graph.filename:
			self.drawGraphFromFile(graph)
		else:
			self.drawGraphFromExpr(graph)
	
	
	def plot3D(self, graph):
		""" Plots 3D curve(Line or Scatter) """
		x = graph.points[0]	
		y = graph.points[1]
		z = graph.points[2]		

		if graph.plotType == None or graph.plotType == "Surface":
			zipped = sorted(zip(x,y,z)) #Sorts based on 1st,2nd and then 3rd item

			xSurface = sorted(list(set(x)))
			ySurface = sorted(list(set(y)))
			zSurface = []
			i = 0
			for xS in xSurface:
				if i==len(zipped):
					break
				zList=[]
				for j in range(len(ySurface)):
					if zipped[i][0] == xS:
						if zipped[i][1] == ySurface[j]:
							zList.append(zipped[i][2])
							i+=1
						else:
							zList.append(float('NaN'))
					else:
						zList.append(float('NaN'))
				zSurface.append(np.asarray(zList))
					
			normalizedColString = (graph.colString[0]/255., graph.colString[1]/255., graph.colString[2]/255., graph.colString[3]/255.)
			if graph.expr:
				p2 = gl.GLSurfacePlotItem(x=np.asarray(xSurface), y=np.asarray(ySurface), z=np.asarray(zSurface), color=normalizedColString, shader="shaded", glOptions=str(graph.opacity))
			else:
				p2 = gl.GLSurfacePlotItem(x=np.asarray(xSurface), y=np.asarray(ySurface), z=np.asarray(zSurface), color=normalizedColString, glOptions=str(graph.opacity))
		else:
			pos = np.empty((len(graph.points[0]), 3))
			for i in range(len(graph.points[0])):
				pos[i] = (x[i], y[i], z[i])
			normalizedColString = (graph.colString[0]/255., graph.colString[1]/255., graph.colString[2]/255., graph.colString[3]/255.)
			p2 = gl.GLScatterPlotItem(pos=pos, size=graph.lineWidth*10, color=normalizedColString, pxMode=True, glOptions=str(graph.opacity))
	
		return p2
	def plot2D(self, graph):
		""" Plots 2D curve(Line or Scatter) """
		x = graph.points[0]
		y = graph.points[1]

		pen = pg.mkPen(color=graph.colString, width=graph.lineWidth)
		if graph.plotType == None or graph.plotType == "Line":
			plot = pg.PlotCurveItem()
			plot.setData(x=x, y=y, pen=pen, name=graph.name)
		else:
			plot = pg.ScatterPlotItem()
			plot.setData(x=x, y=y, pen=pen, name=graph.name)
		return plot	
	
	def drawGraphFromExpr(self, graph):
		if graph.dim == 2:
			self.plotType = 2
			plot = self.plot2D(graph)
			self.w.addItem(plot)
			self.addItemToList(plot, graph)
			self.graphicsView_2d.setVisible(True)
			self.graphicsView_3d.setVisible(False)
			
		else:
			self.plotType = 3
			p2 = self.plot3D(graph)
			self.graphicsView_3d.addItem(p2)
					
			self.graphicsView_3d.setVisible(True)
			self.graphicsView_2d.setVisible(False)
						
			self.addItemToList(p2, graph)
	def drawGraphFromFile(self, graph):
		if graph.dim==2:
			self.graphicsView_2d.setVisible(True)
			self.graphicsView_3d.setVisible(False)
			plot = self.plot2D(graph)
			self.w.addItem(plot)
			self.addItemToList(plot, graph)
		
		else:
			self.graphicsView_2d.setVisible(False)
			self.graphicsView_3d.setVisible(True)

			x = graph.points[0]
			y = graph.points[1]
			z = graph.points[2]
	
			p2 = self.plot3D(graph)
			
			self.graphicsView_3d.addItem(p2)
			self.addItemToList(p2, graph)

class Window(QtGui.QMainWindow):

	def __init__(self, app):
		super(Window, self).__init__()
		self.ui=HarryPlotter(self, app)
		self.ui.setupUi(self)
		self.ui.additional(self)
		self.show()
	def closeEvent(self, event):
		json = ""
		
		for i in range(self.ui.tabWidget.count()):
			json = json + self.ui.tabWidget.widget(i).ui.getJson()+"\n"
			
		f = open(".json.txt", "w")
		f.write(json)
		f.close()
		   
def main():


	app = QtGui.QApplication(sys.argv)

	import qdarkstyle	
	app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

	start = time.time()
	# Create and display the splash screen
	splash_pix = QtGui.QPixmap('/usr/lib/harryplotter/harry.png')
	splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	splash.show()

	while time.time() - start < 1:
		time.sleep(0.001)
		app.processEvents()
	ex = Window(app)
	ex.showMaximized()
	ex.hide()
	splash.finish(ex)
	ex.show()
	toRestore = False
	if os.path.isfile(".json.txt"):
		reply = QtGui.QMessageBox.StandardButton()
		x = ex
		reply = QtGui.QMessageBox.question(x, "Restore session", "Do you want to restore the previous session ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
		if reply == QtGui.QMessageBox.Yes:
			toRestore = True
		else:
			toRestore = False
	else:
		toRestore = False
	ex.ui.restoreFromOutside(toRestore)
	sys.exit(app.exec_())


	# app = QtGui.QApplication(sys.argv)
	# ex = Window()
	# sys.exit(app.exec_())

if __name__ == '__main__':
	main()
