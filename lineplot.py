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

import operator

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
        self.minFreq = 0
        self.axis = 0
        self.gridSize = 10
        self.name = ""
        self.unit = ""
        self.classWidth = 0.1
        self.numClass = 0
        self.length = 0

        self.initGrid()

    def initGrid(self):
        """Initialize the cube on the background, it defines the grid over which
        the plot will be displayed."""
        # Face for the cube.    Format:     [x, y, z]
        self.face = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
    
    def InitGL(self):
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.2, 1.1, -0.2, 1.1, 1.0, 10.0)
        #
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glutInit(sys.argv)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glPushMatrix()
        glScalef(1.0 / (self.numClass * self.classWidth), 1, 0)
        self.DrawGrid()
        self.DrawPoints()
        self.drawLabels()
        glPopMatrix()
        self.drawYLabels()

        self.SwapBuffers()

    def DrawGrid(self):
        # Face
        # glPolygonMode(GL_FRONT, GL_FILL)
        # glColor(1.0, 1.0, 1.0, 1.0)
        # glBegin(GL_TRIANGLE_STRIP)
        # glVertex3fv(self.face[0])
        # glVertex3fv(self.face[1])
        # glVertex3fv(self.face[2])
        # glVertex3fv(self.face[3])
        # glEnd()
        # Grid
        glColor(0.0, 0.0, 0.0, 1.0)
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xCCCC)
        glLineWidth(0.5)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINES)
        for i in range(self.numClass):
            x = i * self.classWidth
            glVertex3f(x, 0.0, 0.1)
            glVertex3f(x, 1.0, 0.1)
            glVertex3f(0.0, x, 0.1)
            glVertex3f(self.length - 0.1, x, 0.1)
        glEnd()
        glPopAttrib()

    def DrawPoints(self):
        """Display the points on the graph"""
        def Map(value, Range):
            """Map the value in range [range[0], range[1]] to the range [0, 1]"""
            # Formula for mapping [A, B] -> [a, b]:
            #
            #   (val - A) * (b - a) / (B - A) + a
            assert Range[0] < Range[1]
            assert Range[0] <= value <= Range[1]
            unitRange = [0.0, 1.0]

            norm = ((value - Range[0]) * (unitRange[1] - unitRange[0]) / (Range[1] - Range[0])) + unitRange[0]
            assert unitRange[0] <= norm <= unitRange[1], "Out of range: " + str(norm)
            return norm
        #
        # Don't draw if empty
        if not self.data:
            return
        if not self.range:
            return

        glColor(0.0, 0.4, 0.6)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        # Iterate over all elements of the dictionary
        i = 0
        self.classWidth = 0.1
        for d in self.sortedData:
            # x = Map(d[0], self.range)
            y = d[1]
            glVertex3f(i * self.classWidth, y, 0.0)
            i += 1
        glEnd()

    def setData(self, ndata):
        """ Set the data of the line plot. data is an array containing the 
        values of the axis on which the frequencies are calculated.
            -ndata: The new data.
        """
        assert type(ndata) is list, "Incorrect input type"
        
        self.data.clear()
        data = sorted(ndata)
        # Compute the frequencies
        for d in data:
            self.data[d] = self.data.get(d, 0) + 1

        # Get the max value
        self.maxFreq = self.data[ndata[0]]
        self.minFreq = self.data[ndata[0]]
        for d in self.data:
            if self.data[d] > self.maxFreq:
                self.maxFreq = self.data[d]
            if self.data[d] < self.minFreq:
                self.minFreq = self.data[d]
        # Normalize the frequencies
        for d in self.data:
            self.data[d] /= self.maxFreq

        self.numClass = len(self.data)
        self.length = self.classWidth * self.numClass
        self.setRange(data)
        # Get the ordered sequence of values
        self.sortedData = sorted(self.data.items(), key=operator.itemgetter(0))

    def setRange(self, data):
        """
        Set the range of the x axis
        """
        assert type(data) is list, "Incorrect input type"
        assert isSort(data), "The data is not sorted"

        self.range = [data[0], data[-1]]

        assert len(self.range) == 2, "Incorrect len of range"

    def setUnit(self, unit):
        """ Set the unit of the axis """
        self.unit = unit

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

        glColor3f(0.0, 0.0, 0.0)
        # Draw the value variables
        divWidth = 1.0 / len(self.data)
        i = 0
        for d in self.sortedData:
            label = str(d[0])
            length = GetLabelWidth(label)
            length /= self.size.width
            glRasterPos2f(i * self.classWidth - length / 2.0, -0.07)
            i += 1
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

        if self.name == "":
            return
        # Draw the name of the variable
        label = self.name + ' (' + self.unit + ')'
        length = GetLabelWidth(label)
        length /= self.size.width
        glRasterPos2f((self.length / 2) - length, 1.05)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    def drawYLabels(self):
        """ Draws the labels of the y axis """
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

        # For the y axis
        divWidth = 1.0 / self.gridSize
        minFreq = 0
        yoffset = 0.01
        for i in range(self.gridSize + 1):
            y = minFreq + i * divWidth
            yLabel = str(self.minFreq + i * self.gridSize)
            length = GetLabelWidth(yLabel)
            length /= self.size.width
            glRasterPos2f(-0.05, yoffset + (i * divWidth) - (length / 2.0))
            for c in yLabel:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

        label = 'Number of elements'
        length = len(label)
        fontHeight = glutBitmapHeight(GLUT_BITMAP_HELVETICA_18) / self.size.height
        start = 0.5 + ((fontHeight * length) / 2.0)
        i = 0
        for c in label:
            glRasterPos2f(-0.13, start - i * fontHeight)
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            i += 1

    def setName(self, nName):
        """ Set the name of the variable """
        assert type(nName) is str, "Incorrect type"
        self.name = nName

    def reDraw(self):
        """ Send an event for drawing """
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

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
    def __init__(self, parent):
        super(LinePlotWidget, self).__init__(parent, style=wx.RAISED_BORDER)
        # Hold the reference
        self.data = None
        self.labels = None
        self.axis = None
        self.category = None
        self.units = None

        self.lp = LinePlot(self)
        self.lp.SetMinSize((400, 400))

    def create(self, data, labels, axis, category, units):
        """ Pass the data and initialize """
        if not self.lp:
            self.lp = LinePlot(self)
            self.lp.SetMinSize((400, 400))

        # Hold the reference
        self.data = data
        self.labels = labels
        self.axis = axis
        self.category = category
        self.units = units

        self.initLP()
        self.initCtrls()
        self.bindEvents()

    def initLP(self):
        """ Initialize the lineplot """
        self.lp.setName(self.labels[self.axis])
        data = [d[self.axis] for d in self.data]
        self.data.rewind()
        self.lp.setData(data)
        self.lp.setUnit(self.units[self.axis])

    def initComboBox(self):
        """ Initialize and fill the combobox with the name and number of the axis. """
        axes = []
        for i in range(self.data.dataLength()):
            if self.category[i] == 0:
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
        self.sizer.Add(axesSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(self.sizer)

    def bindEvents(self):
        """ Bind the event to the combobox """
        self.cb1.Bind(wx.EVT_COMBOBOX, self.onCBSelected)

    def onCBSelected(self, event):
        """ Manage the combobox events. When the axis is changed, make the 
        appropiate changes to graph """
        selection = self.cb1.GetClientData(self.cb1.GetSelection())
        self.axis = selection.axisNumber
        data = [d[self.axis] for d in self.data]
        self.data.rewind()
        self.lp.setData(data)
        self.lp.setName(self.labels[self.axis])
        self.lp.setUnit(self.units[self.axis])
        self.lp.reDraw()

    def close(self):
        """ Close all the controls """
        self.DestroyChildren()
        self.lp = None