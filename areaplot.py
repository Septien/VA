"""
For the area plot. An area graph displays quantitative data graphically. It is based on the line graph. An area is drawn
below the line. Are usually used for representing cummulative totals using numbers or percentages over time. It can be used
also for showing trends over time among related attributes. The color indicates volumen.
"""

# wxPython
import wx

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# OpenGL canvas
import oglCanvas as oglC

# numpy
import numpy as np

# math library
import math as m

#
import random as r

class AreaPlot(oglC.OGLCanvas):
    """
    As with the line graph, this class holds variables for the range and domain of the y and x coordinates, respectively, 
    and the values of the data points (in 2D). It is a dynamic graph.
    Internal variables:
        -xdata: Array holding the x values to be displayed, could be an array of arrays, indicating multiple areas-
        -ydata: Holds the y values of the data.
        -range: The range of the data.
        .domain: The domain of the data.
    """
    def __init__(self, parent):
        super(AreaPlot, self).__init__(parent)

        # Data points
        self.xdata = []
        self.ydata = []
        # Range (y-axis) and Domain (x-axis)
        self.range = []
        self.domain = []

        self.initGrid()

    def initGrid(self):
        """Initialize the cube on the background, it defines the grid over which
        the plot will be displayed."""
        # Face for the cube.    Format:     [x, y, z]
        self.face = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
        # For the grid
        self.square = [[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.0, 0.25, 0.0], [0.25, 0.25, 0.0]]

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
        # Enable alpha channel
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glutInit(sys.argv)

    def SetDomain(self, nDomain):
        """Set the domain of the x-coordinate"""
        assert type(nDomain) == list, "Invalid input type"
        assert len(nDomain) == 2, "Input domain must be in format: [lowerbound, upperbound]"
        assert nDomain[0] < nDomain[1], "Invalid values, must be: lowerbound < upperbound"

        self.domain = nDomain.copy()
        # Send a draw event
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

        assert self.domain, "Empty domain"
        assert self.domain[0] < self.domain[1], "Invalid domain"

    def SetRange(self, nRange):
        """Set the range of the y-coordiante"""
        assert type(nRange) == list, "Invalid input type"
        assert len(nRange) == 2, "Input range must be in format: [lowerbound, upperbound]"
        assert nRange[0] < nRange[1], "Invalid input values, must be: lowerbound < upperbound"

        self.range = nRange.copy()
        # Send a draw event
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

        assert self.range, "Input range"
        assert self.range[0] < self.range[1], "Invalid range"


    def AddPoints(self, points):
        """Add a new array of points to the graph.
        -points is a variable of length 2, holding both the x values and the y values
            of the new points"""
        def IsSort(array):
            """Verify if the array is in ascending order"""
            x = array[0]
            for y in array[1:]:
                if x > y:
                    return False
                x = y
            return True

        assert type(points) is list, "Incorrect input type"
        assert len(points) == 2, "Incorrect number of dimensions."
        assert IsSort(points[0]), "Unordered x array"
        assert len(points[0]) == len(points[1])

        # Add to arrays
        self.xdata.append(points[0].copy())
        self.ydata.append(points[1].copy())

        # Send a draw event
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

        assert len(self.xdata) == len(self.ydata)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.DrawGrid()
        self.DrawArea()

        self.SwapBuffers()

    def DrawArea(self):
        """Display the area on the graph. The area will be drawn per segments, from point A to point B.
        A square will be drawn. For that, a triangle strip will be used."""
        def Map(value, Range):
            """Map the value in range [range[0], range[1]] to the range [0, 1]"""
            # Formula for mapping [A, B] -> [a, b]:
            #
            #   (val - A) * (b - a) / (B - A) + a
            assert Range[0] < Range[1], "Incorrect range"
            unitRange = [0.0, 1.0]

            norm = ((value - Range[0]) * (unitRange[1] - unitRange[0]) / (Range[1] - Range[0])) + unitRange[0]
            assert 0.0 <= norm <= 1.0, "Out of range: " + str(norm) + " " + str(value)
            return norm
        #
        # Don't draw if empty
        if not self.xdata or not self.ydata:
            return
        if not self.domain or not self.range:
            return

        assert len(self.xdata) == len(self.ydata), "x and y arrays must have the same length"

        alpha = 0.6
        for i in range(len(self.xdata)):
            prevPoint = [0.0, 0.0, 0.0]
            glColor(r.random(), r.random(), r.random(), alpha)
            for j in range(len(self.ydata[i])):
                x = self.xdata[i][j]
                y = self.ydata[i][j]
                xNorm = Map(x, self.domain)
                yNorm = Map(y, self.range)
                currPoint = [xNorm, yNorm, 0.0]
                assert currPoint != prevPoint, "Equal points"
                glBegin(GL_TRIANGLE_FAN)
                glVertex3f(prevPoint[0], 0.0, 0.0)
                glVertex3fv(prevPoint)
                glVertex3fv(currPoint)
                glVertex3f(currPoint[0], 0.0, 0.0)
                glEnd()
                prevPoint = currPoint.copy()
            # Draw last part of graph
            glBegin(GL_TRIANGLES)
            glVertex3f(prevPoint[0], 0.0, 0.0)
            glVertex3fv(prevPoint)
            glVertex3f(1.0, 0.0, 0.0)
            glEnd()


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
