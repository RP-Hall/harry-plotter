""" This is the class which represents a Graph object """
from parser import *
import numpy as np

class Graph:

    errorMsg = None
    def __init__(self, expr=None, filename=None, dim=None, xMin=None, xMax=None, yMin=None, yMax=None, plotType=None, lineType="Solid", opacity="additive", lineWidth=2, name = None, colString=None):
        """
        Constructs the Graph object based on the source and stores the points.
        Can be constructed from expr or file.
        From expr: If dimension is given, then use that.
        		   Otherwise guess from expression.
        		   y=f(x) or f(x) is treated as 2D and self.points = [[],[]].
                   z=f(x,y) or f(x,y) is treated as 3D and self.points = [[],[], []].
        From file: if first line contains 2 numbers, it is 2D
                   if first line contains 3 numbers, it is 3D

        """
        try:
            self.expr=expr
            self.filename=filename
            self.dim=dim
            if xMin != None:
                self.xMin=float(xMin)
            else:
                self.xMin=None
            if xMax != None:
                self.xMax=float(xMax)
            else:
                self.xMax=None
            if yMin != None:
                self.yMin=float(yMin)
            else:
                self.yMin=None
            if yMax != None:
                self.yMax=float(yMax)
            else:
                self.yMax=None
            self.plotType = plotType
            self.lineType=lineType
            self.opacity = opacity
            self.lineWidth=lineWidth
            self.colString = colString
            self.name = name
            if expr:
                self.source="expr"
            else:
                self.source="file"

            ## From expr
            if self.source=="expr":
            	# If dimension is given, use that    
                if dim:
                	if dim == 2:
                		self.points = data2D_generator(self.expr, self.xMin, self.xMax)
                	elif dim == 3:
                		self.points = data3D_generator(self.expr, self.xMin, self.xMax, self.yMin, self.yMax)
                	else:
                		self.points = None
                # Dimension is not given, try to guess from expression
                else:
                	self.points = generateData(self.expr, self.xMin, self.xMax, self.yMin, self.yMax)

                # Error
                if self.points == None:
                	self.errorMsg = "Oops!!Invalid expression"
                
            ## From File
            else:
                f = open(filename, "r")
                lines = f.read().splitlines()
                d = len(lines[0].split()) #Dimension from file
                if d == 2:
                    lineNum=1
                    self.points=[[],[]]
                    for line in lines:
                        # Error
                        if len(line.split()) != 2:
                            f.close()
                            self.errorMsg = "Error on line number " + str(lineNum)
                            raise Exception()
                        x=float(line.split()[0])
                        y=float(line.split()[1])
                        self.points[0].append(x)
                        self.points[1].append(y)
                        lineNum+=1
                    f.close()
                elif d == 3:
                    lineNum=1
                    self.points=[[],[],[]]
                    for line in lines:
                        # Error
                        if len(line.split()) != 3:
                            f.close()
                            self.errorMsg = "Error on line number " + str(lineNum)
                            raise Exception()
                        x=float(line.split()[0])
                        y=float(line.split()[1])
                        z=float(line.split()[2])
                        self.points[0].append(x)
                        self.points[1].append(y)
                        self.points[2].append(z)
                        lineNum+=1
                    f.close()
                else:
                    f.close()
                    raise Exception()
        ## Some error
        except:
            self.points=None            
