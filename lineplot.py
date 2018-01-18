"""
For the line graph. A line graph is a type of chart that displays information as a
serie of data points connected by straight line segments. Similar to a scatter ṕlot, 
except that the measurement points are ordered (by x-axis value) and connected with 
a straight line.
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

class LinePlot(oglC.OGLCanvas):
    """
    Class for the line plot. It will hold variables for the domain, the range,
    and the values of the data points. It will be a dynamic graph, meaning that the variable, the range,
    and all its internal variables will be able to change as necessary. The drawing must be changed accordingly.
    Internal variables:
        -xdata: Array holding the x values to be displayed, could be an array of arrays, indicating multiple lines.
        -ydata: Array holding the y values of the xdata points
        -range: Possible values that can be taken by the y-axis coordinates of the points. In format: [min, max].
        -domain: Possible values that can be taken by the x-axis coordinates of the points. In the format: [min, max]
    """
    def __init__(self, parent):
        super(LinePlot, self).__init__(parent)

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
        # assert over the last element

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

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.DrawGrid()
        self.DrawPoints()
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

    def DrawPoints(self):
        """Display the points on the graph"""
        def Map(value, Range):
            """Map the value in range [range[0], range[1]] to the range [0, 1]"""
            # Formula for mapping [A, B] -> [a, b]:
            #
            #   (val - A) * (b - a) / (B - A) + a
            unitRange = [0.0, 1.0]

            norm = ((value - Range[0]) * (unitRange[1] - unitRange[0]) / (Range[1] - Range[0])) + unitRange[0]
            return norm
        #
        # Don't draw if empty
        if not self.xdata or not self.ydata:
            return
        if not self.domain or not self.range:
            return

        assert len(self.xdata) == len(self.ydata), "x and y arrays must be the same length"

        glColor(0.0, 0.0, 0.0)
        for i in range(len(self.xdata)):
            glBegin(GL_LINE_STRIP)
            for j in range(len(self.xdata[i])):
                x = self.xdata[i][j]
                y = self.ydata[i][j]
                xNorm = Map(x, self.domain)
                yNorm = Map(y, self.range)
                glVertex3f(xNorm, yNorm, 0.0)
            glEnd()
