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
    Class for the 2D scatterplot. Members:
        -points: Array of arrays containing the two variable to display.
                In the format: [[x_i],[y_i]], i = 1, 2, ..., N.
        -range: Array containing the ranges of each axis: [[x_min, x_max],[y_min, y_max]].
        -divisions: The number of divisions to show on the graph.
        -axis1Name: The name of the variable for the x-axis (horizontal).
        -axis2Name: The name of the variable for the y-axis (vertical).
    """
    def __init__(self, parent):
        super(ScatterPlot2D, self).__init__(parent)
        # List for the points to be displayed. Handles them as if their were 
        # center of a circle
        self.points = []
        self.range = []
        self.divisions = 5
        self.axis1Name = ""
        self.axis2Name = ""

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
        """ Initialize the OpenGL context """
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
        """Copy the data to the internal variable.
            -newData: Array containing the two variables to draw in the form: [[x_i],[y_i]]"""
        def EqualLenght(inputArray):
            """Verifies that all the elements in the input are of equal length"""
            for i in range(1, len(inputArray)):
                if len(inputArray[i-1]) != len(inputArray[i]):
                    return False;
            return True

        assert newData, "Input data must not be emtpy"
        assert EqualLenght(newData), "All input data must be the same length"

        self.points = newData
        self.GetRanges()

        assert self.points, "Copy not made"
        assert EqualLenght(self.points), "All rows must be the same length"

    def setAxesNames(self, axis1Name, axis2Name):
        """ Set the name of the variable of each axis:
            -axis1Name: The name of the first variable (x-axis).
            -axis2Name: The name of the second variable (y-axis). """
        assert type(axis1Name) is str, "Incorrect input type"
        assert type(axis2Name) is str, "Incorrect input type"

        self.axis1Name = axis1Name
        self.axis2Name = axis2Name

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

        assert minX < maxX, "Incorrect x min and max " + str(minX) + " " + str(maxX)
        assert minY < maxY, "Incorrect y min and max " + + str(minY) + " " + str(maxy)
        assert self.range, "Not initialized range array"

    def SetDivisionNumber(self, nDiv):
        """Stablishes the number of divions on the grid.
            nDiv: The number of divisions."""
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

    def DrawPoints(self, r = 0.01):
        """Draws the points of the plot"""
        def Map(value, Range):
            """Map the value in range [range[0], range[1]] to the range [0, 1]"""
            # Formula for mapping [A, B] -> [a, b]:
            #
            #   (val - A) * (b - a) / (B - A) + a
            assert type(value) is (float or int), str(type(value))
            assert len(Range) > 0
            unitRange = [0.0, 1.0]

            norm = ((value - Range[0]) * (unitRange[1] - unitRange[0]) / (Range[1] - Range[0])) + unitRange[0]
            assert unitRange[0] <= norm <= unitRange[1], "Out of range: " + str(norm) + " " + str(Range) + " " + str(value)
            return norm

        assert self.range, "Ranges must exists"

        if not self.points:
            return
        glColor3f(0.0, 0.0, 1.0)
        for i in range(len(self.points[0])):
            # Normalize x
            x = Map(self.points[0][i], self.range[0])
            # Normalize y
            y = Map(self.points[1][i], self.range[1])
            self.DrawPoint(x, y, r)

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
        Depends on the ranges already be set.
        Displays as well the name of each of the variables on its corresponding axis. """
        def lerp(a, b, t):
            """For interpolating between the range [a, b], according to the formula:
            value = (1 - t) * a + t * b, for t in [0, 1]"""
            assert 0.0 <= t <= 1.0
            value = (1 - t) * a + t * b

            assert a <= value <= b, "Out of range"
            return value
        #
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

        # Draw the name of the axis
        width = GetLabelWidth(self.axis1Name)
        width /= self.size.width
        # For the first axis
        glRasterPos2f(0.5, 1.05)
        for c in self.axis1Name:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        # For the second axis
        length = len(self.axis2Name)
        fontHeight = 19 # As specified by font size
        # Normalize to [0, 1] range
        fontHeight /= self.size.height
        i = 0
        start = 1.0 # Start at one
        for c in self.axis2Name:
            glRasterPos2f(-0.05, start - i * fontHeight)
            i += 1

    def SetNumDivisions(self, nDivisions):
        """Stablishes the number of divisions on the grid"""
        assert type(nDivisions) is int, "Incorrect input type"
        assert nDivisions > 0, "Number of divisions must greater than zero"

        self.divisions = nDivisions

        assert self.divisions > 0, "Number of divisions must be greater than zero"

    def reDraw(self):
        """ Send an event to redraw the graph """
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

#----------------------------------------------------------------------------------------------

class Axes:
    """ Simple class containing the axes name and number """
    def __init__(self, number, name):
        self.axisNumber = number
        self.axisName = name

#----------------------------------------------------------------------------------------------

class ScatterplotWidget(wx.Panel):
    """ Widget for the scatterplot widget and its controls """
    def __init__(self, parent, data, labels, axis1, axis2):
        super(ScatterplotWidget, self).__init__(parent)

        # Hold a reference for the data and labels
        self.data = data
        self.labels = labels
        self.sizer = None
        self.axis1 = axis1
        self.axis2 = axis2

        # Init controls and canvas
        self.initScp()
        self.initCtrls()
        self.bindEvents()

    def initScp(self):
        """ Initialize the canvas for the scp """
        self.scp = ScatterPlot2D(self)
        self.updateAxes()
        self.scp.SetMinSize((400, 400))

    def initComboBox(self):
        """ Initialize and fill the combobox with the name and number of the axis. """
        axes = []
        for i in range(len(self.data[0])):
            axes.append(Axes(i, self.labels[i]))

        self.cb1 = wx.ComboBox(self, size=wx.DefaultSize, choices=[])
        self.cb2 = wx.ComboBox(self, size=wx.DefaultSize, choices=[])
        for axis in axes:
            self.cb1.Append(axis.axisName, axis)
            self.cb2.Append(axis.axisName, axis)

    def initCtrls(self):
        """ Initialize all necessary controls and group them. """
        label = wx.StaticText(self, -1, "Change axes.")
        axis1Label = wx.StaticText(self, -1, "Axis 1: ")
        axis2Label = wx.StaticText(self, -1, "Axis 2: ")
        self.initComboBox()

        # Group the controls of the axis change
        axis1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        axis1Sizer.Add(axis1Label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        axis1Sizer.Add(self.cb1, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        axis2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        axis2Sizer.Add(axis2Label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        axis2Sizer.Add(self.cb2, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        changeSizer = wx.BoxSizer(wx.HORIZONTAL)
        changeSizer.Add(label, 0, wx.ALIGN_TOP | wx.ALIGN_CENTER_VERTICAL)
        changeSizer.Add(axis1Sizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        changeSizer.Add(axis2Sizer, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.scp, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(changeSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.sizer)

    def bindEvents(self):
        """ Bind the combobox events to its corresponding events """
        self.cb1.Bind(wx.EVT_COMBOBOX, self.onAxis1Changed)
        self.cb2.Bind(wx.EVT_COMBOBOX, self.onAxis2Changed)

    def updateAxes(self):
        """ Update the data and the labels of the scatterplot """
        axesData = [self.data[self.axis1], self.data[self.axis2]]
        self.scp.SetData(axesData)
        self.scp.setAxesNames(self.labels[self.axis1], self.labels[self.axis2])

    def onAxis1Changed(self, event):
        """ When another axis is selected. Get the selected
        axis, set it to the scatterplot, and update it. """
        selection = self.cb1.GetClientData(self.cb1.GetSelection())
        axis = selection.axisNumber
        # Update axis
        self.axis1 = axis
        self.updateAxes()
        self.scp.reDraw()

    def onAxis2Changed(self, event):
        """ When the y axis variable change. """
        selection = self.cb2.GetClientData(self.cb2.GetSelection())
        axis = selection.axisNumber
        # Update axis
        self.axis2 = axis
        self.updateAxes()
        self.scp.reDraw()
