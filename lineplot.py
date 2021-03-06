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

import random as r

from multiprocessing import Process, Queue, Lock

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
        self.data = []
        # Range (y-axis) and Domain (x-axis)
        self.range = []
        self.maxFreq = 0
        self.minFreq = 0
        self.axes = []
        self.gridSize = 10
        self.name = []
        self.unit = ""
        self.classWidth = 0.1
        self.numClass = 0
        self.maxL = 0
        self.colors = []
        self.lineLength = 0.0

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
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.lineLength == 0:
            label = self.name[0] + ' (' + self.unit + ')'
            l = GetLabelWidth(label) + 0.02
            if l > self.lineLength:
                self.lineLength = l
        maxX = 1.1 + self.lineLength / self.size.width
        glOrtho(-0.2, maxX, -0.2, 1.1, 1.0, 10.0)

        glMatrixMode(GL_MODELVIEW)
        self.DrawGrid()
        glPushMatrix()
        glScalef(1.0 / (self.numClass * self.classWidth), 1.0, 0)
        self.DrawPoints()
        glPopMatrix()
        self.drawLabels()

        self.SwapBuffers()

    def DrawGrid(self):
        # Grid
        glColor(0.0, 0.0, 0.0, 1.0)
        start = 1.0 / self.gridSize
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xCCCC)
        glLineWidth(0.5)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINES)
        for i in range(self.gridSize + 1):
            x = i * start
            glVertex3f(x, 0.0, 0.1)
            glVertex3f(x, 1.0, 0.1)
            glVertex3f(0.0, x, 0.1)
            glVertex3f(1.0, x, 0.1)
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

        j = 0
        glLineWidth(2)
        for data in self.data:
            # Get the ordered sequence of values
            self.sortedData = sorted(data.items(), key=operator.itemgetter(0))
            glColor3fv(self.colors[j])
            j += 1
            glBegin(GL_LINE_STRIP)
            # Iterate over all elements of the dictionary
            i = 0
            self.classWidth = 0.1
            for d in self.sortedData:
                # x = Map(d[0], self.range)
                y = d[1]
                glVertex3f(i * self.classWidth, y, 0.0)
                i += 1
            del d
            glEnd()
        del data

    def setData(self, ndata, axis):
        """ Set the data of the line plot. data is an array containing the 
        values of the axis on which the frequencies are calculated.
            -ndata: The new data.
        """
        # Compute the frequencies
        q = Queue()
        lock = Lock()
        nRow = ndata.getNumberRows()
        p1 = Process(target=self.parallelCompute, args=(ndata.copy(), axis, 0.0, nRow / 3.0, lock, q))
        p2 = Process(target=self.parallelCompute, args=(ndata.copy(), axis, nRow / 3.0, (2 * nRow) / 3.0, lock, q))
        p3 = Process(target=self.parallelCompute, args=(ndata.copy(), axis, (2 * nRow) / 3.0, nRow, lock, q))
        # Start threads
        p1.start()
        p2.start()
        p3.start()
        # Wait for threads
        p1.join()
        p2.join()
        p3.join()

        dataFreq = {}
        last = None
        # Merge results
        while not q.empty():
            result = q.get()
            for d in result:
                dataFreq[d] = dataFreq.get(d, 0) + result[d]
                last = d
            del result

        ndata.rewind()

        # Get the max value
        self.maxFreq = dataFreq[last]
        self.minFreq = dataFreq[last]
        for d in dataFreq:
            if dataFreq[d] > self.maxFreq:
                self.maxFreq = dataFreq[d]
            if dataFreq[d] < self.minFreq:
                self.minFreq = dataFreq[d]
        # Normalize the frequencies
        for d in dataFreq:
            dataFreq[d] /= self.maxFreq

        self.data.append(dataFreq)
        self.axes.append(axis)
        self.setRange(ndata)
        self.numClass = len(dataFreq)
        self.colors.append([0.0, 0.4, 0.6])
        del dataFreq

    def parallelCompute(self, data, axis, startPosition, endPosition, lock, q):
        """ Compute the frequencies in a parallel manner """
        data.setDataSetPosition(int(startPosition))
        frequencies = {}
        total = 0
        # Compute frequencies
        for row in data:
            d = row[axis]
            del row
            frequencies[d] = frequencies.get(d, 0) + 1
            total += 1
            if total >= endPosition - startPosition:
                break
        # Put data on queue
        lock.acquire()
        q.put(frequencies)
        lock.release()

    def setRange(self, data):
        """
        Set the range of the x axis
        """
        def parallelComputeR(data, axis, startPosition, endPosition, lock, q):
            """ Get the maximum and minimum of the axis """
            data.setDataSetPosition(startPosition)
            minR = maxR = next(data)[axis]
            total = 0
            for d in data:
                if d[axis] < minR:
                    minR = d[axis]
                if maxR < d[axis]:
                    maxR = d[axis]
                total += 1
                if total >= endPosition - startPosition:
                    break
            lock.acquire()
            q.put([minR, maxR])
            lock.release()
        #
        q = Queue()
        lock = Lock()
        nRow = data.getNumberRows()
        p1 = Process(target=parallelComputeR, args=(data.copy(), self.axes[-1], 0.0, nRow / 3.0, lock, q))
        p2 = Process(target=parallelComputeR, args=(data.copy(), self.axes[-1], nRow / 3.0, (2 * nRow) / 3.0, lock, q))
        p3 = Process(target=parallelComputeR, args=(data.copy(), self.axes[-1], (2 * nRow) / 3.0, nRow, lock, q))
        # Start threads
        p1.start()
        p2.start()
        p3.start()
        # Wait for threads
        p1.join()
        p2.join()
        p3.join()

        minR, maxR = float('inf'), -float('inf')
        while not q.empty():
            result = q.get()
            if result[0] < minR:
                minR = result[0]
            if maxR < result[1]:
                maxR = result[1]

        if not self.range:
            self.range = [minR, maxR]
            self.maxL = data.dataLength()
        else:
            if minR < self.range[0]:
                self.range[0] = minR
                self.maxL = data.dataLength()
            if maxR > self.range[1]:
                self.range[1] = maxR
                self.maxL = data.dataLength()

        assert len(self.range) == 2, "Incorrect len of range"

    def addNewLine(self, ndata, axis):
        """ Add a new line to draw """
        assert type(ndata) is list, "Incorrect input type"
        
        for ax in self.axes:
            if ax == axis:
                return

        # Compute the frequencies
        q = Queue()
        lock = Lock()
        nRow = ndata.getNumberRows()
        p1 = Process(target=self.parallelCompute, args=(ndata.copy(), axis, 0.0, nRow / 3.0, lock, q))
        p2 = Process(target=self.parallelCompute, args=(ndata.copy(), axis, nRow / 3.0, (2 * nRow) / 3.0, lock, q))
        p3 = Process(target=self.parallelCompute, args=(ndata.copy(), axis, (2 * nRow) / 3.0, nRow, lock, q))
        # Start threads
        p1.start()
        p2.start()
        p3.start()
        # Wait for threads
        p1.join()
        p2.join()
        p3.join()

        dataFreq = {}
        last = None
        # Merge results
        while not q.empty():
            result = q.get()
            for d in result:
                dataFreq[d] = dataFreq.get(d, 0) + result[d]
                last = d
            del result
        ndata.rewind()

        # Get the max value
        self.maxFreq = dataFreq[last]
        self.minFreq = dataFreq[last]
        for d in dataFreq:
            if dataFreq[d] > self.maxFreq:
                self.maxFreq = dataFreq[d]
            if dataFreq[d] < self.minFreq:
                self.minFreq = dataFreq[d]
        # Normalize the frequencies
        for d in dataFreq:
            dataFreq[d] /= self.maxFreq

        self.data.append(dataFreq)
        self.setRange(data)
        self.axes.append(axis)
        if len(dataFreq) > self.numClass:
            self.numClass = len(dataFreq)
        self.colors.append([r.random(), r.random(), r.random()])
        del data
        del dataFreq

    def setUnit(self, unit):
        """ Set the unit of the axis """
        self.unit = unit

    def clearData(self):
        """ Clear the data """
        self.data.clear()
        self.colors.clear()
        self.name.clear()
        self.lineLength = 0.0

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
        def lerp(a, b, t):
            """For interpolating between the range [a, b], according to the formula:
            value = (1 - t) * a + t * b, for t in [0, 1]"""
            assert 0.0 <= t <= 1.0
            value = (1 - t) * a + t * b

            assert a <= value <= b, "Out of range"
            return value
        

        glColor3f(0.0, 0.0, 0.0)
        # Draw the value variables
        maxValue = 20
        divWidth = 0.0
        # Get the minimum between 20 (the max number of labels) and length of data
        if self.maxL < maxValue:
            maxValue = self.maxL
        divWidth = 1.0 / maxValue
        i = 0
        for d in range(maxValue+1):
            x = lerp(self.range[0], self.range[1], i / maxValue)
            label = '{:.1f}'.format(x)
            length = GetLabelWidth(label)
            length /= self.size.width
            if i % 2 == 0:
                y = -0.07
            else:
                y = -0.13
            glRasterPos2f(i * divWidth - length / 2.0, y)
            i += 1
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

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
        fontHeight = 18 #glutBitmapHeight(GLUT_BITMAP_HELVETICA_18) / self.size.height
        fontHeight /= self.size.height
        start = 0.5 + ((fontHeight * length) / 2.0)
        i = 0
        for c in label:
            glRasterPos2f(-0.13, start - i * fontHeight)
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            i += 1

        if self.name == "":
            return
        # Draw the name of the variable
        start = (self.numClass * self.classWidth) / self.size.width
        offset = 0.1
        for i in range(len(self.name)):
            label = self.name[i] + ' (' + self.unit + ')'
            l = GetLabelWidth(label) + 0.02
            if l > self.lineLength:
                self.lineLength = l
            glColor3fv(self.colors[i])
            glBegin(GL_LINES)
            glVertex3f(1.01, 1.0 - start - (i * offset), 0.0)
            glVertex3f(1.03, 1.0 - start - (i * offset), 0.0)
            glEnd()
            glColor3f(0.0, 0.0, 0.0)
            glRasterPos2f(1.04, 1.0 - start - (i * offset))
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    def setName(self, nName):
        """ Set the name of the variable """
        assert type(nName) is str, "Incorrect type"
        self.name.append(nName)

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
        self.lp.setData(self.data, self.axis)
        self.lp.setUnit(self.units[self.axis])

    def initComboBox(self):
        """ Initialize and fill the combobox with the name and number of the axis. """
        axes = []
        for i in range(self.data.dataLength()):
            if self.category[i] == 0:
                axes.append(Axes(i, self.labels[i]))

        self.cb1 = wx.ComboBox(self, size=wx.DefaultSize, choices=[])
        self.cbline = wx.ComboBox(self, size=wx.DefaultSize, choices=[])
        for axis in axes:
            self.cb1.Append(axis.axisName, axis)
            if self.units[axis.axisNumber] == self.units[self.axis] and axis.axisNumber != self.axis:
                self.cbline.Append(axis.axisName, axis)

    def initCtrls(self):
        """ Group all the controls for the lineplot """
        label = wx.StaticText(self, -1, "Change Axis: ")
        label2 = wx.StaticText(self, -1, "Add line: ")
        self.initComboBox()

        axesSizer = wx.BoxSizer(wx.HORIZONTAL)
        axesSizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_LEFT)
        axesSizer.Add(self.cb1, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_HORIZONTAL)
        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        lineSizer.Add(label2, 0, wx.ALIGN_CENTER_VERTICAL)
        lineSizer.Add(self.cbline, 0, wx.ALIGN_CENTER_VERTICAL)
        ctrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrlSizer.Add(axesSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        ctrlSizer.Add(lineSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.lp, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.sizer.Add(ctrlSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(self.sizer)

    def bindEvents(self):
        """ Bind the event to the combobox """
        self.cb1.Bind(wx.EVT_COMBOBOX, self.onCBSelected)
        self.cbline.Bind(wx.EVT_COMBOBOX, self.onNewLineSelected)

    def onCBSelected(self, event):
        """ Manage the combobox events. When the axis is changed, make the 
        appropiate changes to graph """
        selection = self.cb1.GetClientData(self.cb1.GetSelection())
        self.axis = selection.axisNumber
        self.lp.clearData()
        self.lp.setData(self.data, self.axis)
        self.lp.setName(self.labels[self.axis])
        self.lp.setUnit(self.units[self.axis])
        self.lp.reDraw()
        self.cbline.Clear()
        self.cbline.SetValue('')

        axes = []
        for i in range(self.data.dataLength()):
            if self.category[i] == 0:
                axes.append(Axes(i, self.labels[i]))
        for axis in axes:
            if self.units[axis.axisNumber] == self.units[self.axis] and axis.axisNumber != self.axis:
                self.cbline.Append(axis.axisName, axis)

    def onNewLineSelected(self, event):
        """ When a new line is selected """
        selection = self.cbline.GetClientData(self.cbline.GetSelection())
        axis = selection.axisNumber
        self.lp.addNewLine(self.data, axis)
        self.lp.setName(selection.axisName)
        del data

    def close(self):
        """ Close all the controls """
        self.DestroyChildren()
        self.lp = None
