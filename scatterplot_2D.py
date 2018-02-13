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
        super(ScatterPlot2D, self).__init__(parent)
        # List for the points to be displayed. Handles them as if their were 
        # center of a circle
        self.points = []
        self.range = []
        self.divisions = 5

        self.InitCirclePoints()
        self.initGrid()

        # random points
        # r.seed()
        # for i in range(100):
        #     self.points.append((r.uniform(0, 1), r.uniform(0, 1)))
        # self.GetRanges()

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
            for i in range(1, len(inputArray)):
                if len(inputArray[i-1]) != len(inputArray[i]):
                    return False;
            return True

        assert newData, "Input data must not be emtpy"
        assert EqualLenght(newData), "All input data must be the same length"

        self.points.clear()
        self.points = newData.copy()
        self.GetRanges()

        assert self.points, "Copy not made"
        assert EqualLenght(self.points), "All rows must be the same length"

    def GetRanges(self):
        """Calculate the ranges of each dimension"""
        if not self.points:
            return

        self.range.clear()
        
        minX = maxX = self.points[0][0]
        minY = maxY = self.points[0][1]
        for i in range(len(self.points[0])):
            # For the x coordinate
            if self.points[0][i] < minX:
                minX = self.points[0][i]
            elif maxX < self.points[0][i]:
                maxX = self.points[0][i]
            # For the y coordinate
            if self.points[1][i] < minY:
                minY = self.points[1][i]
            elif maxY < self.points[1][i]:
                maxY = self.points[1][i]
        
        self.range.append([minX, maxX])
        self.range.append([minY, maxY])

        assert self.range, "Not initialized range array"

    def SetDivisionNumber(self, nDiv):
        """Stablishes the number of divions on the grid"""
        assert type(nDiv) is int, "Must be integer: " + str(type(nDiv))
        assert nDiv > 0, "Number of divisions must be greater than zero"

        self.divisions = nDiv

        assert self.divisions > 0, "Number of divisions must be greater than zero"

    def initGrid(self):
        """Initialize the cube on the background, it defines the grid over which
        the plot will be displayed."""
        # For the face of the square. 	Format:		[x, y, z]
        self.face = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
        # For the grid
        self.square = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.DrawGrid()
        self.DrawPoints()
        self.DrawLabels()

        self.SwapBuffers()

    def DrawPoints(self):
        """Draws the points of the plot"""
        if not self.points:
            return
        glColor3f(0.0, 0.0, 1.0)
        for i in range(len(self.points)):
            self.DrawPoint(self.points[i][0], self.points[i][1], 0.01)

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
        for j in range(self.divisions):
            print(j)
            glPushMatrix()
            width = 1.0 / self.divisions
            glTranslate(0.0, j * width, 0.0)
            for i in range(self.divisions):
                glPushMatrix()
                glTranslate(i * width, 0.0, 0.0)
                glScalef(width, width, 0.0)
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

    def DrawLabels(self):
        """Displays the corresponding values for the divisons of each of the axes.
        Depends on the ranges already be set"""
        def lerp(a, b, t):
            """For interpolating between the range [a, b], according to the formula:
            value = (1 - t) * a + t * b, for t in [0, 1]"""
            assert 0.0 <= t <= 1.0
            value = (1 - t) * a + t * b

            assert a <= value <= b, "Out of range"
            return value

        assert self.range, "Ranges must be initialized"

        for i in range(self.divisions + 1):
            xValue = lerp(self.range[0][0], self.range[0][1], i / self.divisions)
            yValue = lerp(self.range[1][0], self.range[1][1], i / self.divisions)
            strxValue = "%.2f" % xValue
            stryValue = "%.2f" % yValue
            pos = i / self.divisions
            # For the x-axis
            glRasterPos2f(pos, -0.04)
            for c in strxValue:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            # For the y-axis
            glRasterPos2f(-0.07, pos)
            for c in stryValue:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    def SetNumDivisions(self, nDivisions):
        """Stablishes the number of divisions on the grid"""
        assert type(nDivisions) is int, "Incorrect input type"
        assert nDivisions > 0, "Number of divisions must greater than zero"

        self.divisions = nDivisions

        assert self.divisions > 0, "Number of divisions must be greater than zero"