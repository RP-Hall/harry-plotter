import numpy as np
import numexpr as ne
import sys, traceback

"""
    where(bool, number1, number2)			:	 number -- number1 if the bool condition is true, number2 otherwise.
    {sin,cos,tan}(float|complex)			:	 float|complex -- trigonometric sine, cosine or tangent.
    {arcsin,arccos,arctan}(float|complex)	: 	 float|complex -- trigonometric inverse sine, cosine or tangent.
    arctan2(float1, float2)					:	 float -- trigonometric inverse tangent of float1/float2.
    {sinh,cosh,tanh}(float|complex)			:	 float|complex -- hyperbolic sine, cosine or tangent.
    {arcsinh,arccosh,arctanh}(float|complex):	 float|complex -- hyperbolic inverse sine, cosine or tangent.
    {log,log10,log1p}(float|complex)		:	 float|complex -- natural, base-10 and log(1+x) logarithms.
    {exp,expm1}(float|complex)				:	 float|complex -- exponential and exponential minus one.
    sqrt(float|complex)						:	 float|complex -- square root.
    abs(float|complex)						:	 float|complex -- absolute value.
    {real,imag}(complex)					: 	 float -- real or imaginary part of complex.
    complex(float, float)					:	 complex -- complex from real and imaginary parts. 
"""

"""
 e ^ something 	-> exp(something) 
 e 				-> e
 sin inverse x 	-> arcsin(x)
 
 pi 		  	-> pi
 cosec(x) 	 	-> 1/sin(x)
"""

""" 
	data2D_generator is for single parameter x, (it must be specified as x ) generates data_file.txt, ( ALWAYS FOR EXPLICIT)
"""

numPoints2D = 10000
numPoints3D = 100

def isvariable(c):
	return c=='x' or c=='y' or c=='z'

""" 2x, 2sin, xy, xsin """
def canInsertMultSign(prev, curr):
	return ( prev.isdigit() or isvariable(prev) ) and curr.isalpha()

# It converts z=f(x,y) to g(x,y) in correct python form for evaluation
# It converts y=f(x) to g(x) in correct python form for evaluation
def preProcess(expr):			# preprocessing on expr to make it of proper format, returns processed string
	expr = expr.lower()
	expr = expr.replace(" ", "") ## Remove spaces
	expr = expr.replace("^","**")
	## Insert * signs
	l = len(expr)
	i=1
	while True:
		if i>=l:
			break
		if expr[i-1] == "e" and expr[i] != "^" and expr[i] != "+" and expr[i] != "-" and expr[i] != "*" and expr[i] != "/" and expr[i] != ")":
			expr = expr[0:i] + "*" + expr[i:]
			l = l+1
		i = i + 1

	i=2
	while True:
		if i>=l:
			break
		if expr[i-2:i] == "pi" and expr[i] != "^" and expr[i] != "+" and expr[i] != "-" and expr[i] != "*" and expr[i] != "/" and expr[i] != ")":
			expr = expr[0:i] + "*" + expr[i:]
			l = l+1
		i = i + 1

	i=1
	while True:
		if i>=l:
			break
		if expr[i-1] == ")" and expr[i] != "^" and expr[i] != "+" and expr[i] != "-" and expr[i] != "*" and expr[i] != "/" and expr[i] != ")":
			expr = expr[0:i] + "*" + expr[i:]
			l = l+1
		i = i + 1

	i = 1
	while True:
		if i>=l:
			break
		if canInsertMultSign(expr[i-1], expr[i]):
			expr = expr[0:i] + "*" + expr[i:]
			l = l+1
		i = i + 1

	## Make it of f(x,y) or f(x) form for evaluation
	if expr.startswith("y="):
		expr = expr[2:]
	elif expr.endswith("=y"):
		expr = expr[:-2]
	
	if expr.startswith("z="):
		expr = expr[2:]
	elif expr.endswith("=z"):
		expr = expr[:-2]

	return expr

def generateData(expr, xMin, xMax, yMin, yMax):
	""" Genearates data by identifying the type of plot(2D or 3D) """
	expr = expr.lower()
	expr = expr.replace(" ", "") #Remove spaces
	# y=f(x) or z=f(x,y)
	if '=' in expr:
		if expr.startswith("y=") or expr.endswith("=y"):
			return data2D_generator(expr, xMin, xMax)		
		if expr.startswith("z=") or expr.endswith("=z"):
			return data3D_generator(expr, xMin, xMax, yMin, yMax)
		return None
	# f(x) or f(x,y)
	else:
		if 'y' in expr:
			return data3D_generator(expr, xMin, xMax, yMin, yMax)
		else:
			return data2D_generator(expr, xMin, xMax)


def data2D_generator(expr, xMin, xMax):
	""" Generates [xList, yList]"""
	""" Returns None if syntax is not correct """
	xMin = float(xMin)
	xMax = float(xMax)
	numPoints = 1000000
	xdel=(xMax-xMin)/numPoints2D			
	try:
		expr = preProcess(expr)
		if 'x' not in expr:
			expr+="+0*x"
		print expr
		x = np.arange(xMin, xMax, xdel)
		pi = np.pi
		e = np.e
		y = ne.evaluate(expr)
		
		# print x,y
		return [x.tolist(), y.tolist()] #OK

	except:
		# traceback.print_exc()
		return None # Error

""" 
	data3D_generator is for single parameter x,y (it must be specified as x, y ) generates data_file.txt, ( ALWAYS FOR EXPLICIT)
"""
def data3D_generator(expr, xMin, xMax, yMin, yMax):
	""" Generates [xList, yList, zList]"""
	""" Returns None if syntax is not correct """
	xMin = float(xMin)
	xMax = float(xMax)
	yMin = float(yMin)
	yMax = float(yMax)
	numPoints = 100
	xdel=(xMax-xMin)/numPoints3D
	ydel=(yMax-yMin)/numPoints3D		
	try:
		expr = preProcess(expr)
		if 'x' not in expr:
			expr+="+0*x"
		if 'y' not in expr:
			expr+="+0*y"
		print expr
		zList = []
		pi = np.pi
		e  = np.e
		xRet = []
		yRet = []
		zRet = []
		xList  = np.arange(xMin, xMax, xdel)
		y  = np.arange(yMin, yMax, ydel)
		for x in xList:
			z  = ne.evaluate(expr)
			yRet=yRet+y.tolist()
			zRet=zRet+z.tolist()
			for i in range(len(z)):
				xRet.append(x)
		
		return [xRet, yRet, zRet]
		# return [xList.tolist(), y.tolist(), zList] #OK		
	except:
		# traceback.print_exc()
		return None # Error

if __name__ == "__main__":

	# print preProcess("y=2x*2x^2=y")
	print data2D_generator("y=2sin(e^x)",-2 ,2)
	# print data3D_generator("sin(x+y)",0,1,0.5,1,2,0.3)

