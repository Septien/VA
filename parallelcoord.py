"""
For the parallel coordinates. A graph for visualizing high-dimensional data whitout information lost.
"""

import wx

import oglCanvas as oglC

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class ParallelCoordinates(oglC.OGLCanvas):
    """
    This class contains the implementation of the parallel coordinates graph.
    It has several attributes:
        -Data: The data to be visualized. This contains all the dataset.
        -Number of axes: The dimension of the data.
        -Labels: What represents each axis.
        -Axis range: Each coordinate is (linearly) interpolated between the maximum and minimum value among all
            the possible values of that axis
        -axesOrder: The order on which the axes are displayed.
        -filterAxis: The axis to apply the filtering.
        -filterRange: The range to filter
    """
    def __init__(self, parent):
        super(ParallelCoordinates, self).__init__(parent)

        self.data = []
        self.dimensions = None
        self.labels = []
        self.axesRange = []
        self.axesOrder = []
        self.filterAxis = -1
        self.filterRange = []

    def InitGL(self):
        glClearColor(0.9, 0.9, 0.9, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.1, 1.1, -0.2, 1.1, 1.0, 10.0)
        #
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_TEXTURE_2D)
        glutInit(sys.argv)

    def SetData(self, newData):
        """Sets the data to be displayed and calculates the range"""
        def EqualLength(matrix):
            """Verifies that all rows of the matrix have the same length"""
            for i in range(1, len(matrix)):
                if len(matrix[i-1]) != len(matrix[i]):
                    return False
            return True

        assert newData, "Empty input"
        assert type(newData) is list, "Incorrect input type"
        assert len(newData) > 0, "Data must have length than zero"
        assert EqualLength(newData), "All rows must be the same lenght"
        if self.labels:
            assert len(self.Labels) == len(newData[0]), "Labels must be the same length as the number of dimensions"

        # Hold a reference for the data
        self.data = newData
        # Set number of dimensions
        self.dimensions = len(self.data[0])
        # Set the default axes order
        for i in range(self.dimensions):
            self.axesOrder.append(i)
        self.ComputeRanges()

        assert self.data, "No data copied"
        assert EqualLength(self.data), "All rows must be the same lenght"
        assert len(self.axesOrder) == self.dimensions, "The length of the array for the order of axes, must be the same to the number of dimensiones"
        if self.labels:
            assert len(self.labels) == len(self.data[0]), "Labels must be the same length as the number of dimensions"
            assert self.dimensions == len(self.labels)

    def ComputeRanges(self):
        """Computes the range of each axis"""
        assert self.data, "Data must be initialized"
        assert self.dimensions != 0, "Dimensions must be initialized"

        self.axesRange.clear()
        for i in range(len(self.data[0])):
            minV = maxV = self.data[0][i]
            for j in range(len(self.data)):
                if self.data[j][i] < minV:
                    minV = self.data[j][i]
                elif self.data[j][i] > maxV:
                    maxV = self.data[j][i]
            self.axesRange.append([minV, maxV])

        assert len(self.axesRange) == len(self.data[0]), "Incorrect number of ranges " + str(len(self.axesRange)) + " " + str(len(self.data))
        assert len(self.axesRange) == self.dimensions, "Incorrect number of ranges"


    def SetLabels(self, newLabels):
        """Sets the labels of the data"""

        assert newLabels, "Labels data can not be empty"
        assert len(newLabels) > 0, "Labels can not be empty"
        if self.data:
            assert len(newLabels) == len(self.data[0]), "Number of labels must be the same as the number of axes"
            assert len(newLabels) == self.dimensions, "Incorrect number of labels: " % self.dimensions % ", " % len(newLabels)

        # Hold a reference for the labels
        self.labels = newLabels

        assert self.labels, "Labels array empty"
        assert len(self.labels) == len(self.data[0]), "Different number of dimensions"

    def changeAxes(self, axis1, axis2):
        """ Change the position of the axis 1 to the position of the axis 2, and viceversa """
        # Get the position
        index1 = 0
        index2 = 0
        for i in  range(len(self.axesOrder)):
            if self.axesOrder[i] == axis1:
                index1 = i
            if self.axesOrder[i] == axis2:
                index2 = i
        # Change the order
        self.axesOrder[index1] = axis2
        self.axesOrder[index2] = axis1
        # Send event to redraw
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

    def setDefaultAxesOrder(self):
        """ Set the default axis configuration """
        # Remove previous configurations
        self.axesOrder.clear()
        # Set default
        for i in range(self.dimensions):
            self.axesOrder.append(i)
        # Send event to redraw
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

    def setFilterAxis(self, axis):
        """ Sets the axis to filter """
        assert type(axis) is int, "Incorrect axis input type"

        self.filterAxis = axis

    def setFilterRange(self, nRange):
        """ Sets the range to filter """
        assert type(nRange) is list, "Incorrect input type"
        assert self.axesRange[self.filterAxis][0] <= nRange[0] <= self.axesRange[self.filterAxis][1], "Out of range"
        assert self.axesRange[self.filterAxis][0] <= nRange[1] <= self.axesRange[self.filterAxis][1], "Out of range"

        self.filterRange = nRange.copy()
        # Send event to redraw
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

    def getAxisRange(self, axis):
        """ Gets the range of the axis 'axis' """
        assert 0 <= axis < self.dimensions, "Out of range"
        return self.axesRange[axis]

    def resetFilter(self):
        """ Resets the class so all lines are drawn """
        self.filterAxis = -1
        self.filterRange = []
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

    def OnDraw(self):
        """Draw the graph"""
        glClear(GL_COLOR_BUFFER_BIT)

        # Dotted line
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glColor3f(0.0, 0.0, 0.0)
        self.DrawBoundingBox()
        self.DrawParallelAxes()
        glPopAttrib()

        glColor3f(0.0, 0.0, 1.0)
        self.DrawLines()
        glColor3f(0.0, 0, 0)
        self.DrawLabels()

        self.SwapBuffers()

    def DrawBoundingBox(self):
        """Draws the bounding box of the coordinates"""
        glBegin(GL_LINE_LOOP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)
        glEnd()

    def DrawParallelAxes(self):
        """Draws the axes of the plot"""
        assert self.data, "Data must be initialized"
        assert self.dimensions > 0, "Dimensions must be greater than zero"

        # Calculate the spacing between ||-lines
        spacing = 1.0 / (self.dimensions - 1.0)

        glBegin(GL_LINES)
        for i in range(self.dimensions - 1):
            glVertex3f(i * spacing, 0.0, 0.0)
            glVertex3f(i * spacing, 1.0, 0.0)
        glEnd()

    def DrawLines(self):
        """Draws the lines representing the data"""
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
        #
        assert self.data, "Data must be initialized"
        assert self.dimensions > 0, "Dimensions must be greater than zero"
        assert len(self.data[0]) == self.dimensions, "Dimensions in data must be the same as in the variable"
        assert len(self.axesRange) > 0, "Range must be initialized"

        spacing = 1.0 / (self.dimensions - 1.0)
        # Iterate over all rows
        for row in self.data:
            i = 0
            drawLine = True
            # Check if line is within interval, and a filter must be applied
            if self.filterAxis > -1:        # If a filter must be applied
                if not (self.filterRange[0] <= row[self.filterAxis] <= self.filterRange[1]): # If the variable is out of range
                    drawLine = False
            if drawLine:
                glBegin(GL_LINE_STRIP)
                for index in self.axesOrder:
                    coord = row[index]
                    coordNorm = Map(coord, self.axesRange[index])
                    glVertex3f(i * spacing, coordNorm, 0.0)
                    i += 1
                glEnd()


    def DrawLabels(self):
        """Print the labels on screen"""
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
        #
        assert self.labels, "Labels empty"

        spacing = 1.0 / (self.dimensions - 1.0)
        i = 0
        for index in self.axesOrder:
            label = self.labels[index]
            width = GetLabelWidth(label)
            width /= self.size.width
            if i % 2 == 0:
                y = -0.1
            else:
                y = -0.16
            glRasterPos2f(i * spacing - width / 2.0, y)
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            
            label = str(self.axesRange[index][0])
            glRasterPos2f(i * spacing, -0.04)
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))
            label = str(self.axesRange[index][1])
            glRasterPos2f(i * spacing, 1.01)
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))

            i += 1

#----------------------------------------------------------------------------------------------

class Axes:
    """ Simple class containing the axes name and number """
    def __init__(self, number, name):
        self.axisNumber = number
        self.axisName = name

#----------------------------------------------------------------------------------------------

class PCWidget(wx.Panel):
    """ For managing the widgets for the pc """
    def __init__(self, parent, data, labels):
        super(PCWidget, self).__init__(parent)

        # Hold a reference for the data and labels
        self.data = data
        self.labels = labels
        self.sizer = None
        self.axis = -1
        self.axisRange = []
        self.size = (600, 500)

        # Create the graph
        self.initPC()
        self.initCtrls()
        self.bindBtnEvents()

    def initPC(self):
        """ Initialize the ||-coord """
        self.pc = ParallelCoordinates(self)
        self.pc.SetData(self.data)
        self.pc.SetLabels(self.labels)
        self.pc.SetMinSize(self.size)

    def initComboBox(self):
        """ Fill the combo box with the axes data """
        axes = []
        for i in range(len(self.data[0])):
            axes.append(Axes(i, self.labels[i]))

        l = []
        # Make the combo boxes
        self.cb1 = wx.ComboBox(self, size=wx.DefaultSize, choices=l)
        self.cb2 = wx.ComboBox(self, size=wx.DefaultSize, choices=l)
        self.cb3 = wx.ComboBox(self, size=wx.DefaultSize, choices=l)

        # Fill the cb
        for axis in axes:
            self.cb1.Append(axis.axisName, axis)
            self.cb2.Append(axis.axisName, axis)
            self.cb3.Append(axis.axisName, axis)

    def initCtrls(self):
        """ Initialize and group the controls """
        # For the controls for changing axes position
        interChangeAxisLabel = wx.StaticText(self, -1, "Change axis position:")
        axis1Label = wx.StaticText(self, -1, "Axis 1:")
        axis2Label = wx.StaticText(self, -1, "Axis 2:")
        self.changeBtn = wx.Button(self, label="Change axes")
        self.resetBtn = wx.Button(self, label="Reset axes")
        # Init cbs
        self.initComboBox()

        # For the controls to filter
        filterLabel = wx.StaticText(self, -1, "Filter an axis:")
        axisLabel = wx.StaticText(self, -1, "Axis:")
        rangeLabel = wx.StaticText(self, -1, "Range:")
        lowerLimitLabel = wx.StaticText(self, -1, "Lower limit:")
        upperLimitLabel = wx.StaticText(self, -1, "Upper limit:")
        self.tbxRange = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.tbxLower = wx.TextCtrl(self, -1)
        self.tbxUpper = wx.TextCtrl(self, -1)
        self.resetFilterBtn = wx.Button(self, label="Reset")
        self.filterBtn = wx.Button(self, label="Filter")

        # Group the buttons
        btnsSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsSizer.Add(self.resetBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)
        btnsSizer.Add(self.changeBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)
        # Group the combo boxes with its respective labels
        # Combo box 1
        cbSizer1 = wx.BoxSizer(wx.VERTICAL)
        cbSizer1.Add(axis1Label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        cbSizer1.Add(self.cb1, 0, wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # Combo box 2
        cbSizer2 = wx.BoxSizer(wx.VERTICAL)
        cbSizer1.Add(axis2Label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        cbSizer1.Add(self.cb2, 0, wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # Both combo boxes
        cbSizer = wx.BoxSizer(wx.VERTICAL)
        cbSizer.Add(cbSizer1, 0, wx.TOP | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        cbSizer.Add(cbSizer2, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        # Group label, combo boxes and buttons
        widgetsSizer = wx.BoxSizer(wx.VERTICAL)
        widgetsSizer.Add(interChangeAxisLabel, 0, wx.TOP | wx.ALIGN_CENTER_VERTICAL)
        widgetsSizer.Add(cbSizer, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        widgetsSizer.Add(btnsSizer, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        # For filtering
        widgetsSizer.Add(filterLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        axSizer = wx.BoxSizer(wx.HORIZONTAL)
        axSizer.Add(axisLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        axSizer.Add(self.cb3, wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        rgSizer = wx.BoxSizer(wx.HORIZONTAL)
        rgSizer.Add(rangeLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        rgSizer.Add(self.tbxRange, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        lowSizer = wx.BoxSizer(wx.HORIZONTAL)
        lowSizer.Add(lowerLimitLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        lowSizer.Add(self.tbxLower, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        upSizer = wx.BoxSizer(wx.HORIZONTAL)
        upSizer.Add(upperLimitLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        upSizer.Add(self.tbxUpper, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        btnsSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        btnsSizer2.Add(self.resetFilterBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)
        btnsSizer2.Add(self.filterBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)

        widgetsSizer.Add(axSizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        widgetsSizer.Add(rgSizer, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        widgetsSizer.Add(lowSizer, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        widgetsSizer.Add(upSizer, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        widgetsSizer.Add(btnsSizer2, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)

        # Main sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.pc, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(widgetsSizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)

    def bindBtnEvents(self):
        """ Bind the event for both buttons """
        # https://wiki.python.org/self.Bind vs. self.button.Bind
        self.changeBtn.Bind(wx.EVT_BUTTON, self.onChangeBtn)
        self.resetBtn.Bind(wx.EVT_BUTTON, self.onResetBtn)
        self.cb3.Bind(wx.EVT_COMBOBOX, self.onAxisSelected)
        self.filterBtn.Bind(wx.EVT_BUTTON, self.onFilterBtn)
        self.resetFilterBtn.Bind(wx.EVT_BUTTON, self.onResetFilterBtn)

    def onChangeBtn(self, event):
        """ Handle the change button click """
        # Get the index of the axes
        cb1Selection = self.cb1.GetClientData(self.cb1.GetSelection())
        cb2Selection = self.cb2.GetClientData(self.cb2.GetSelection())
        # Change axes
        axis1 = cb1Selection.axisNumber
        axis2 = cb2Selection.axisNumber
        self.pc.changeAxes(axis1, axis2)

    def onResetBtn(self, event):
        """ Hangle the reset button click """
        self.pc.setDefaultAxesOrder()

    def onAxisSelected(self, event):
        """ When an axis is selected, get the range of the corresponding axis """
        selection = self.cb3.GetClientData(self.cb3.GetSelection())
        # Get the axis number
        self.axis = selection.axisNumber
        self.axisRange = self.pc.getAxisRange(self.axis)
        # Display it on the text box
        self.tbxRange.SetValue("")
        self.tbxRange.SetValue(str(self.axisRange))

    def onFilterBtn(self, event):
        """ When the filter button is pressed """
        upperS = self.tbxUpper.GetLineText(0)
        lowerS = self.tbxLower.GetLineText(0)
        if not upperS.isdecimal():
            #self.tbxUpper.SetToolTip("Only numbers within the range")
            return
        if not lowerS.isdecimal():
            return
        upper = float(upperS)
        lower = float(lowerS)
        if not self.axisRange[0] <= upper <= self.axisRange[1]:
            return
        if not self.axisRange[0] <= lower <= self.axisRange[1]:
            return
        if upper < lower:
            return

        # Set the range
        self.pc.setFilterAxis(self.axis)
        self.pc.setFilterRange([lower, upper])


    def onResetFilterBtn(self, event):
        """ Reset all the data points """
        self.pc.resetFilter()
        self.tbxRange.SetValue("")
        self.tbxUpper.SetValue("")
        self.tbxLower.SetValue("")
