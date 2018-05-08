"""
For the line graph. A line graph is a type of chart that displays information as a
serie of data points connected by straight line segments. Similar to a scatter plot, 
except that the measurement points are ordered (by x-axis value) and connected with 
a straight line. The y value of the point, corresponds to the frequencie or value of that
data at that moment.
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

# Auxiliary functions        
def isSort(data):
    """ Verifies if the array is sorted """
    for i in range(1, len(data)):
        if data[i - 1] > data[i]:
            return False
    return True

class LinePlot(oglC.OGLCanvas):
    """
    Class for the line plot. It will hold variables for the domain, the range,
    and the values of the data points. It will be a dynamic graph, meaning that the variable, the range,
    and all its internal variables will be able to change as necessary. The drawing must be changed accordingly.
    Internal variables:
        -data: Dictionary containing the values and its frequencies
        -range: Possible values that can be taken by the y-axis coordinates of the points. In format: [min, max].
        -domain: Possible values that can be taken by the x-axis coordinates of the points. In the format: [min, max]
    """
    def __init__(self, parent):
        super(LinePlot, self).__init__(parent)

        # Data points
        self.data = {}
        # Range (y-axis) and Domain (x-axis)
        self.range = []
        self.maxFreq = 0
        self.axis = 0
        self.gridSize = 4
        self.name = ""

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
        glutInit(sys.argv)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.DrawGrid()
        self.DrawPoints()
        self.drawLabels()

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
        for j in range(self.gridSize):
            glPushMatrix()
            glTranslate(0.0, j * 0.25, 0.0)
            for i in range(self.gridSize):
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
        if not self.data:
            return
        if not self.range:
            return

        glColor(0.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        # Iterate over all elements of the dictionary
        for d in self.data:
            x = Map(d, self.range)
            y = self.data[d]
            glVertex3f(x, y, 0.0)
        glEnd()

    def setData(self, ndata):
        """ Set the data of the line plot. data is an array containing the 
        values of the axis on which the frequencies are calculated.
            -ndata: The new data.
        """
        assert type(ndata) is list, "Incorrect input type"
        
        data = sorted(ndata)
        # Compute the frequencies
        for d in data:
            self.data[d] = self.data.get(d, 0) + 1

        # Get the max value
        self.maxFreq = self.data[ndata[0]]
        for d in self.data:
            if self.data[d] > self.maxFreq:
                self.maxFreq = self.data[d]
        # Normalize the frequencies
        for d in self.data:
            self.data[d] /= self.maxFreq

        self.setRange(data)

    def setRange(self, data):
        """
        Set the range of the x axis
        """
        assert type(data) is list, "Incorrect input type"
        assert isSort(data), "The data is not sorted"

        self.range = [data[0], data[-1]]

        assert len(self.range) == 2, "Incorrect len of range"

    def setAxis(self, nAxis):
        """ Set the axis """
        assert type(nAxis) is int, "Incorrect type"
        self.axis = nAxis

    def setGridSize(self, ngridSize):
        """ Set the size of the grid """
        assert type(ngridSize) is int, "Incorrect type"
        self.gridSize = ngridSize

    def drawLabels(self):
        """ Draws labels on the graph """
        def GetLabelWidth(label):
            """Returns the total width of the length of 'label', using the
            fonts from glut"""
            assert type(label) is str, "Incorrect type"

            length = 0
            for c in label:
                length += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(c))

            assert type(length) is int
            assert length >= 0

            return length

        # Draw the value variables
        divWidth = 1.0 / len(self.data)
        i = 0
        for d in self.data:
            label = str(d)
            length = GetLabelWidth(label)
            length /= self.size.width
            glRasterPos2f(i * divWidth - length / 2.0, -0.06)
            i += 1
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # For the y axis
        divWidth = 1.0 / self.gridSize
        minFreq = 0
        for i in range(self.gridSize):
            y = minFreq + i * divWidth
            yLabel = str(y)
            length = GetLabelWidth(yLabel)
            length /= self.size.width
            glRasterPos2f(-0.06, i * divWidth - length / 2.0)
            for c in yLabel:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        if self.name == "":
            return
        # Draw the name of the variable
        glRasterPos2f(0.5, 1.05)
        for c in self.name:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    def setName(self, nName):
        """ Set the name of the variable """
        assert type(nName) is str, "Incorrect type"
        self.name = nName

#--------------------------------------------------------------------------------------------

class Axes:
    """ Simple class containing the axes name and number """
    def __init__(self, number, name):
        self.axisNumber = number
        self.axisName = name

#----------------------------------------------------------------------------------------------

class LinePlotWidget(wx.Panel):
    """ Holds the canvas for the panel, and all the widgets and events associated with it 
            -data: reference to the original database.
            -labels: Name of the axes.
            -axis: Axis to analyze
    """
    def __init__(self, parent, data, labels, axis):
        super(LinePlotWidget, self).__init__(parent)
        # Hold the reference
        self.data = data
        self.labels = labels
        self.axis = axis

        self.initLP()
        self.initCtrls()
        
    def initLP(self):
        """ Initialize the lineplot """
        self.lp = LinePlot(self)
        self.lp.setName(self.labels[self.axis])
        self.lp.setAxis(self.axis)
        data = [d[self.axis] for d in self.data]
        self.lp.setData(data)
        self.lp.SetMinSize((300, 300))

    def initComboBox(self):
        """ Initialize and fill the combobox with the name and number of the axis. """
        axes = []
        for i in range(len(self.data[0])):
            axes.append(Axes(i, self.labels[i]))

        self.cb1 = wx.ComboBox(self, size=wx.DefaultSize, choices=[])
        for axis in axes:
            self.cb1.Append(axis.axisName, axis)

    def initCtrls(self):
        """ Group all the controls for the lineplot """
        label = wx.StaticText(self, -1, "Change Axis: ")
        self.initComboBox()

        axesSizer = wx.BoxSizer(wx.HORIZONTAL)
        axesSizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_LEFT)
        axesSizer.Add(self.cb1, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.lp, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.sizer.Add(axesSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.sizer)
