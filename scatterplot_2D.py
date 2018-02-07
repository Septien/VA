"""
A 2D scatterplot.
"""

# wxPython
import wx

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# OpenGL canvas
import oglCanvas as oglC

#
import random as r

#
import math as m

#
import numpy as np

class ScatterPlot2D(oglC.OGLCanvas):
	"""
	For the 2D version of the scatter plot.
	"""

	def __init__(self, parent):
		"""
		ctor.
		"""
		super(ScatterPlot2D, self).__init__(parent)
		# List for the points to be displayed. Handles them as if their were 
		# center of a circle
		self.points = []

		self.InitCirclePoints()
		self.initGrid()

		# random points
		r.seed()
		for i in range(100):
			self.points.append((r.uniform(0, 1), r.uniform(0, 1)))

	def InitCirclePoints(self):
		"""
		Constructs an array containing the points for a circle centered at the origin
		and with radious 1.
		"""
		self.circle = []

		x = 0.0
		y = 0.0
		# Upper half
		for x in np.arange(1.0, -1.0, -0.01):
			y = m.sqrt(1 - x * x)
			self.circle.append((x, y))
		# Lower half
		for x in np.arange(-1.0, 1.0, 0.01):
			y = - m.sqrt(1 - x * x)
			self.circle.append((x, y))

	def InitGL(self):
		glClearColor(0.9, 0.9, 0.9, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		#
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-0.1, 1.1, -0.1, 1.1, 1.0, 10.0)
		#
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
		glShadeModel(GL_SMOOTH)
		glutInit(sys.argv)

    def SetData(self, newData):
        """Copy the data to the internal variable"""
        def EqualLenght(inputArray):
            """Verifies that all the elements in the input are of equal length"""
            for i in range(len(1, inputArray)):
                if len(inputArray[i-1]) != len(inputArray[i]):
                    return False;
            return True

        assert newData, "Input data must not be emtpy"
        assert EqualLenght(newData), "All input data must be the same length"

        self.points.clear()
        self.points = newData.copy()

        assert self.points, "Copy not made"


	def initGrid(self):
		"""Initialize the cube on the background, it defines the grid over which
		the plot will be displayed."""
		# Face for the cube. 	Format:		[x, y, z]
		self.face = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
		# For the grid
		self.square = [[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.0, 0.25, 0.0], [0.25, 0.25, 0.0]]

	def OnDraw(self):
		glClear(GL_COLOR_BUFFER_BIT)
		self.DrawGrid()

        if self.points:
    		glColor3f(0.0, 0.0, 1.0)
    		for i in range(len(self.points)):
    			self.DrawPoint(self.points[i][0], self.points[i][1], 0.01)

		self.SwapBuffers()

	def DrawGrid(self):
		# Face
		glPolygonMode(GL_FRONT, GL_FILL)
		glColor(1.0, 1.0, 1.0, 1.0)
		glBegin(GL_TRIANGLE_STRIP)
		glVertex3fv(self.face[0])
		glVertex3fv(self.face[1])
		glVertex3fv(self.face[2])
		glVertex3fv(self.face[3])
		glEnd()
		# Grid
		glPolygonMode(GL_FRONT, GL_LINE)
		for j in range(4):
			glPushMatrix()
			glTranslate(0.0, j * 0.25, 0.0)
			for i in range(4):
				glPushMatrix()
				glTranslate(i * 0.25, 0.0, 0.0)
				self.DrawSquare()
				glPopMatrix()
			glPopMatrix()

	def DrawSquare(self):
		glColor(0.0, 0.0, 0.0, 1.0)
		glBegin(GL_QUADS)
		glVertex3fv(self.square[0])
		glVertex3fv(self.square[1])
		glVertex3fv(self.square[3])
		glVertex3fv(self.square[2])
		glEnd()

	def DrawCircle(self):
		"""
		Draw a circle based on the points previously calculated. Uses a triangle fan.
		"""
		#glBegin(GL_LINE_LOOP)
		glBegin(GL_TRIANGLE_FAN)
		for i in range(len(self.circle)):
			glVertex3f(self.circle[i][0], self.circle[i][1], 0.0)
		glEnd()

	def DrawPoint(self, cx, cy, r):
		"""
		Draw a point centered at (cx, cy) with radious r.
		It is based on the function draw circle.
		"""
		glPushMatrix()
		glTranslatef(cx, cy, 0.0)
		glScalef(r, r, 0.0)
		self.DrawCircle()
		glPopMatrix()
