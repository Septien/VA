"""
Histogram and frequencies polygon plot
"""

# wxPython
import wx

import math as m

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# OpenGL canvas
import oglCanvas as oglC

from multiprocessing import Process, Queue, Lock

class HistogramPlot(oglC.OGLCanvas):
    """
    This class handles the drawing of the histogram. It has as member the number
    of rectangles on the graph, the rectangles, the maximum frequency, and the maximum x value. The width 
    of the rectangles is the same for all, and depends on the number of bins the histogram have. 
    It draw the contour and then draw the rectagle. Draw histogram on canvas using OpenGL.
        -numBins: number of classes on the histogram.
        -binWidth: the width of each class.
        -frequencies: The frecuency of each class.
        -range: The range of each class.
        -maxFrequency.
        -axis: Name of the axis in analysis.
        -data: The data.
        -numDivisions: Number of divisions on the grid.
    """
    def __init__(self, parent):
        super(HistogramPlot, self).__init__(parent)
        self.numBins = 5
        self.binWidth = 1 / self.numBins
        self.frequencies = []
        self.binIntervals = []
        self.range = []
        self.rect = []
        self.maxFrequency = 0
        self.axis = -1
        self.axisName = ''
        self.data = []
        self.numDivisions = 10
        self.unit = ""
        self.category = ""
        self.name = []
        self.value = []
        self.values = []

    def InitGL(self):
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.3, 1.3, -0.1, 1.1, 1.0, 10.0)
        #
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glShadeModel(GL_SMOOTH)
        # Enable alpha channel
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glutInit(sys.argv)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        #Draw rectangles and axes
        glLineWidth(1.0)
        glPushMatrix()
        glTranslatef(0.03, 0.0, 0.0)
        self.drawGrid()
        self.DrawRect()
        glPopMatrix()
        self.DrawAxes()
        self.drawLabels()

        self.SwapBuffers()

    def DrawAxes(self):
        """
        Draw the axes of the histogram.
        """
        glColor3f(0, 0, 0, 1)
        glLineWidth(1.0)
        # Dotted line
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINES)
        # x axis
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(1.05, 0.0, 0.0)
        # y axis
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.05, 0.0)
        glEnd()
        glPopAttrib()

    def DrawRect(self):
        """Draw each rectangle of the histogram"""
        # Interior of the rectangles
        glColor4f(0.0, 0.36, 0.9, 0.8)
        glPolygonMode(GL_FRONT, GL_FILL)
        for i in range(self.numBins):
            glRectfv(self.rect[i][0], self.rect[i][1])
        # Contour
        glColor3f(0.0, 0.0, 1.0)
        glPolygonMode(GL_FRONT, GL_LINE)
        for i in range(self.numBins):
            glRectfv(self.rect[i][0], self.rect[i][1])

    def DrawFreqPol(self):
        """Draws the frequency polygone"""
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 0, 0)
        for i in range(self.numBins):
            glVertex3f((self.rect[i][0][0] + self.rect[i][1][0]) / 2.0, self.frequencies[i], 0)
        glVertex3f(1, 0, 0)
        glEnd()

    def UpdateRect(self):
        """ Update the width and height of the bars according to the number of bins """
        def inRange(array):
            """ Verifies that all the elements in 'array' are within the [0, 1] interval """
            for e in array:
                if not 0 <= e <= 1:
                    return False
            return True
        if not self.frequencies:
            return
        assert inRange(self.frequencies), "Frecuencies out of range"
        #
        self.rect.clear()
        self.rectWidth = 1.0 / self.numBins
        for i in range(self.numBins):
            rect = ((self.rectWidth * i, 0), (self.rectWidth * (1 + i), self.frequencies[i]))
            self.rect.append(rect)

    def setData(self, data):
        """ Stores a reference to the data in use """
        # Store a reference
        self.data = data
        # Set the range
        if self.category == 0:
            self.setRange()

    def computeFrequencies(self, draw):
        """
        Compute the frequencies of the histogram. Such frequencies could not be in the range [0, 1],
        so it normalize them. Such frequency is the height of the rectangle. If the number of 
        frequencies is different to the number of bins, the latter is updated.
        """
        def parallelCompute(data, axis, category, intervals, startPosition, endPosition, q, lock):
            data.setDataSetPosition(startPosition)
            total = 0
            if category == 0:
                f = []
                for i in range(len(intervals)):
                    f.append(0)
                for x in data:
                    i = 0
                    for interval in intervals:
                        if interval[0] <= x[axis] <= interval[1]:
                            f[i] += 1
                            break
                        i += 1
                    total += 1
                    if total >= (endPosition - startPosition):
                        break
            else:
                f = {}
                for x in data:
                    f[x[axis]] = f.get(x[axis], 0) + 1
                    total += 1
                    if total >= (endPosition - startPosition):
                        break
            lock.acquire()
            q.put(f)
            lock.release()

        # Create a queue
        q = Queue()
        qLock = Lock()
        nRow = self.data.getNumberRows()
        p1 = Process(target=parallelCompute, args=(self.data.copy(), self.axis, self.category, self.binIntervals, 0.0, nRow / 3.0, q, qLock))
        p2 = Process(target=parallelCompute, args=(self.data.copy(), self.axis, self.category, self.binIntervals, nRow / 3.0, (2 * nRow) / 3.0, q, qLock))
        p3 = Process(target=parallelCompute, args=(self.data.copy(), self.axis, self.category, self.binIntervals, (2 * nRow) / 3.0, nRow, q, qLock))
        # Compute absolute frequencies
        # Start threads
        p1.start()
        p2.start()
        p3.start()
        # Wait for threads
        p1.join()
        p2.join()
        p3.join()

        if self.category == 0:
            self.initFrequencies()
            while not q.empty():
                result = q.get()
                i = 0
                for r in result:
                    self.frequencies[i] += r
                    i += 1

        else:
            f = {}
            while not q.empty():
                result = q.get()
                for r in result:
                    f[r] = f.get(r, 0) + result[r]
            self.frequencies.clear()
            self.SetNumBins(len(f))
            self.initFrequencies()
            i = 0
            for d in f:
                self.frequencies[i] = f[d]
                self.values.append(d)
                i += 1
            del f

        # Normalize
        self.maxFrequency = self.frequencies[0]
        for f in self.frequencies:
            if f > self.maxFrequency:
                self.maxFrequency = f
        
        for i in range(len(self.frequencies)):
            self.frequencies[i] /= self.maxFrequency

        # Update rectangles and redraw
        self.UpdateRect()
        # For sending events:
        # https://stackoverflow.com/questions/747781/wxpython-calling-an-event-manually
        # https://www.blog.pythonlibrary.org/2010/05/22/wxpython-and-threads/
        # https://stackoverflow.com/questions/25299745/how-to-programmatically-generate-an-event-in-wxpython
        if draw:
            wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
        self.data.rewind()
    
    def setRange(self):
        """
        Set the range of the x axis
        """
        def parallelComputeR(data, axis, startPosition, endPosition, lock, q):
            """ Get the maximum and minimum of the axis """
            data.setDataSetPosition(startPosition)
            minR, maxR = float('inf'), -float('inf')
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
        nRow = self.data.getNumberRows()
        p1 = Process(target=parallelComputeR, args=(self.data.copy(), self.axis, 0.0, nRow / 3.0, lock, q))
        p2 = Process(target=parallelComputeR, args=(self.data.copy(), self.axis, nRow / 3.0, (2 * nRow) / 3.0, lock, q))
        p3 = Process(target=parallelComputeR, args=(self.data.copy(), self.axis, (2 * nRow) / 3.0, nRow, lock, q))
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
        self.range = [minR, maxR]
        self.data.rewind()

    def setUnits(self, unit):
        """ Sets the units of the variable """
        self.unit = unit

    def setCategory(self, category):
        """ """
        self.category = category

    def SetNumBins(self, numB):
        """ Sets the number of bins for the histogram """
        self.numBins = numB;
        self.computeBinWidth()

    def setDescription(self, value, descr):
        """ Set the description of each variable """
        self.name = descr
        self.value = value

    def getNumBins(self):
        """
        Returns the number of bins
        """
        return self.numBins

    def computeBins(self):
        """
        Computes the number of classes based on the formula by Freedman-Diaconis:
            c = 2(IQ)*n^-1/3
        where IQ is the interquartile range, and n is the number of data
        """

        # Get the number of points
        n = self.data.getNumberRows()
        # Compute quartiles
        fQpos = ( (n - 1) / 4 ) + 1
        tQpos = ( 3 * (n - 1) / 4 ) + 1
        # Compute the quartiles
        firstQ = 0.0
        thirdQ = 0.0
        # First quartile
        if fQpos == round(fQpos):
            i = 0
            for row in self.data:
                i += 1
                if i >= int(fQpos):
                    break
            firstQ = row[self.axis]
        else:
            i = 0
            up = round(fQpos)
            for row in self.data:
                i += 1
                if i >= up - 1:
                    break
            row2 = next(self.data)
            firstQ = row[self.axis] + ( (row2[self.axis] - row[self.axis]) / 4.0 )

        self.data.rewind()
        # Third quartile
        if tQpos == round(tQpos):
            i = 0
            for row in self.data:
                i += 1
                if i >= int(tQpos):
                    break
            thirdQ = row[self.axis]
        else:
            up = round(tQpos)
            for row in self.data:
                i += 1
                if i >= up - 1:
                    break
            row2 = next(self.data)
            thirdQ = row[self.axis] + ( 3 * ( row2[self.axis] - row[self.axis]) / 4.0 )
        # Compute IQR
        IQR = thirdQ - firstQ
        self.data.rewind()
        numB = int(2 * IQR * m.pow(n, -1/3)) + 1
        self.SetNumBins(numB)

        assert self.numBins > 0, "Bins not set"
        assert self.binWidth > 0, "Incorrect class width"

    def computeBinWidth(self):
        """
        Computes the width of each class.
        """
        self.binWidth = (self.range[1] - self.range[0]) / self.numBins
        # Fill the frequencies array with zeros
        self.initFrequencies()

    def initFrequencies(self):
        """ Initialize the frequency array with zeros """
        del(self.frequencies)
        self.frequencies = []
        for i in range(self.numBins):
            self.frequencies.append(0)

    def computeClassesInterval(self):
        """
        Computes the interval for each class
        """
        lower = 0
        upper = 0
        x0 = self.range[0]
        x = x0
        self.binIntervals.clear()
        for i in range(self.numBins):
            lower = x
            x = x0 + (i + 1) * self.binWidth
            upper = x
            interval = [lower, upper]
            self.binIntervals.append(interval.copy())
            del interval
        self.data.rewind()

    def getMaxBins(self):
        """ Return the maximum number of bins """
        return 50

    def setAxis(self, axisName, axis):
        """ Set the axis name to analize """
        assert type(axisName) is str, "Incorrect type."
        self.axisName = axisName
        self.axis = axis

    def drawGrid(self):
        """ Draw a grid on the canvas """
        start = 1.0 / self.numDivisions
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for i in range(self.numDivisions + 1):
            x = i * start
            glVertex3f(x, 0.0, 0.0)
            glVertex3f(x, 1.0, 0.0)
            glVertex3f(0.0, x, 0.0)
            glVertex3f(1.0, x, 0.0)
        glEnd()
        glPopAttrib()

    def drawLabels(self):
        """ Draw labels for x and y axis """
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

        # Draw the value of the ranges
        a = self.range[0]
        glPushMatrix()
        glTranslatef(0.03, 0.0, 0.0)
        for i in range(self.numBins+1):
            if self.category == 0:
                x = a + i * self.binWidth
                xLabel = '{:.1f}'.format(x)
            else:
                if i < self.numBins:
                    for v in self.value:
                        if v == self.value[i]:
                            xLabel = self.name[i]
                else:
                    break

            length = GetLabelWidth(xLabel)
            length /= self.size.width
            if i % 2 == 0:
                y = -0.04
            else:
                y = -0.08
            if self.category == 1:
                glPushMatrix()
                self.binWidth = 1.0 / self.numBins
                glTranslatef(self.binWidth / 2.0, 0.0, 0.0)
            glRasterPos2f(i * self.rectWidth - length / 2.0, y)
            for c in xLabel:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))
            if self.category == 1:
                glPopMatrix()
        glPopMatrix()

        # Draw the value of the frequencies
        minFreq = 0
        divWidth = 1.0 / self.numDivisions
        for i in range(self.numDivisions+1):
            y = lerp(minFreq, self.maxFrequency, i / self.numDivisions)
            yLabel = '{:.1f}'.format(y)
            length = GetLabelWidth(yLabel)
            length /= self.size.width
            glRasterPos2f(-0.12, i * divWidth)
            for c in yLabel:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

        # Draw the name of the variable
        label = self.axisName
        length = GetLabelWidth(label)
        length /= self.size.width
        glRasterPos2f(0.5 - length, 1.05)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # Draw the y-axis label
        label = 'Frequencies'
        length = len(label)
        fontHeight = 18#glutBitmapHeight(GLUT_BITMAP_HELVETICA_18)
        fontHeight /= self.size.height
        i = 0
        start = 1.0#0.5 + ((fontHeight * length) / 2.0)
        for c in label:
            glRasterPos2f(-0.25, start - i * fontHeight)
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            i += 1
        
        label = self.unit
        glRasterPos2f(1.06, 0.0)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


#------------------------------------------------------------------------------------------------------------------

class HistogramWidget(wx.Panel):
    """
    The panel containing the histogram plot and all of its controls
    """
    def __init__(self, parent):
        super(HistogramWidget, self).__init__(parent, style=wx.RAISED_BORDER)

        self.data = None
        self.axis = -1
        self.axisName = None
        self.units = None
        self.category = None
        self.description = None
        self.values = []
        self.names = []

        self.histogram = HistogramPlot(self)
        self.histogram.SetMinSize((400, 400))

    def create(self, data, axis, axisName, units, category, description):
        """ Pass the data to the graph and intialize it. Type: if categorical or numerical """
        if not self.histogram:
            self.histogram = HistogramPlot(self)
            self.histogram.SetMinSize((400, 400))

        self.data = data
        self.axis = axis
        self.units = units
        self.category = category
        self.axisName = axisName
        self.description = description
        self.initHistogram()
        self.initCtrls()
        self.groupControls()
        self.bindEvets()
        self.sliderMinValue = 1

    def initHistogram(self):
        """ Initialize the class for the histogram """
        # Initialize the canvas for histogram
        self.histogram.setAxis(self.axisName, self.axis)
        self.histogram.setCategory(self.category[self.axis])
        self.histogram.setData(self.data)
        if self.category[self.axis] == 0:
            # Compute the defaul number of bins
            self.histogram.computeBins()
            self.histogram.computeClassesInterval()
        else:
            self.values.clear()
            self.names.clear()
            for row in self.description:
                if row[self.axis] == '':
                    break
                value, name = row[self.axis].split('=')
                self.values.append(int(value))
                self.names.append(name)
            self.histogram.setDescription(self.values, self.names)
    
        self.histogram.computeFrequencies(False)
        self.histogram.setUnits(self.units[self.axis])

    def initCtrls(self):
        """
        Initializer the gui controls for the histogram
        """
        # Get the number of bins
        bins = self.histogram.getNumBins()
        maxBins = self.histogram.getMaxBins()
        if self.category[self.axis] == 0:
            # For selecting the number of bins
            self.binsLabel = wx.StaticText(self, -1, "Bins:")
            self.tbxBins = wx.TextCtrl(self, -1, size=(50, 25))
            self.slBins = wx.Slider(self, -1, value=bins, minValue=0,
                maxValue=maxBins, name="Bins", style=wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_AUTOTICKS)
            #
            self.SetSldMaxValue(maxBins)
            self.tbxBins.ChangeValue(str(bins))

    def groupControls(self):
        """
        Group the controls of the class
        """
        # Group controls
        if self.category[self.axis] == 0:
            # Group textbox and label
            binsSizer = wx.BoxSizer(wx.HORIZONTAL)
            binsSizer.Add(self.binsLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
            binsSizer.Add(self.tbxBins, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

            # Group slider and binsSizer
            sliderSizer = wx.BoxSizer(wx.VERTICAL)
            sliderSizer.Add(self.slBins, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_TOP | wx.EXPAND)
            sliderSizer.Add(binsSizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM)

        # Group controls with glcanvas
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.histogram, 5, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        if self.category[self.axis] == 0:
            self.sizer.Add(sliderSizer, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.SetSizer(self.sizer)

    def bindEvets(self):
        """
        Bind the events for the slider and text box
        """
        if self.category[self.axis] == 0:
            self.Bind(wx.EVT_TEXT, self.OnTxtChange, self.tbxBins)
            self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSldScroll, self.slBins)

    def SetSldMaxValue(self, value):
        self.sliderMaxValue = value
        self.slBins.SetMax(value)

    def OnTxtChange(self, event):
        """
        Response to the change of the text whithin the textbox. The user may enter the size of the
        bins directly in the textbox (which will also be desplayed here if the slider position changes).
        If so, the position of the slider is automatically changed.
        """
        prevValue = self.slBins.GetValue()
        value = self.tbxBins.GetLineText(0)                                          # Get the content of the textbox
        if not value.isdecimal():
            self.tbxBins.ChangeValue("")
            self.tbxBins.ChangeValue(str(value))
            return
        value = int(value)
        # Verify that number of bins is within range.
        if self.sliderMinValue <= value and value <= self.sliderMaxValue:
            self.slBins.SetValue(value)
            self.updateHistFreqs(value)

        else:
            #wx.MessageBox("Number of bins must be in [" + str(self.sliderMinValue) + "," +
            # str(self.sliderMaxValue) + "]", "Help", wx.OK | wx.ICON_INFORMATION)
            self.slBins.SetValue(prevValue)
            self.tbxBins.ChangeValue("")    # Clear
            self.tbxBins.ChangeValue(str(prevValue))

    def OnSldScroll(self, event):
        """
        When the slider is moved. It changes the value displayed on the text box as well.
        """
        value = self.slBins.GetValue()
        self.tbxBins.ChangeValue("")
        self.tbxBins.ChangeValue(str(value))
        self.updateHistFreqs(int(value))

    def updateHistFreqs(self, bins):
        """ When the number of bins change"""
        assert type(bins) is int, "Incorrect type"

        # Set the bins
        self.histogram.SetNumBins(bins)
        self.histogram.computeClassesInterval()
        self.histogram.computeFrequencies(True)

    def close(self):
        """ Close all controls """
        self.DestroyChildren()
        self.histogram = None
