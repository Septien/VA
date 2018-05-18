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
        self.axis = ""
        self.data = []
        self.numDivisions = 10

    def InitGL(self):
        glClearColor(0.9, 0.9, 0.9, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.2, 1.3, -0.1, 1.1, 1.0, 10.0)
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
        # glLineWidth(1.0)
        # self.DrawFreqPol()
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
        def isSort(data):
            """ Verifies if the array is sorted """
            for i in range(1, len(data)):
                if data[i - 1] > data[i]:
                    return False
            return True
        assert type(data) is list, "Incorrect input type"
        # Copy and sort
        self.data = data
        self.data.sort()
        # Set the range
        self.setRange()
        assert isSort(self.data), "The data is not sorted"

    def computeFrequencies(self, draw):
        """
        Compute the frequencies of the histogram. Such frequencies could not be in the range [0, 1],
        so it normalize them. Such frequency is the height of the rectangle. If the number of 
        frequencies is different to the number of bins, the latter is updated.
        """
        self.initFrequencies()
        #
        for x in self.data:
            i = 0
            for interval in self.binIntervals:
                if interval[0] <= x <= interval[1]:
                    self.frequencies[i] += 1
                    break
                i += 1
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
    
    def setRange(self):
        """
        Set the range of the x axis
        """
        self.range = [self.data[0], self.data[-1]]
        assert len(self.range) == 2, "Incorrect lenght of range array"

    def SetNumBins(self, numB):
        """ Sets the number of bins for the histogram """
        self.numBins = numB;
        self.computeBinWidth()

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
        n = len(self.data)
        # Compute quartiles
        fQpos = ( (n - 1) / 4 ) + 1
        tQpos = ( 3 * (n - 1) / 4 ) + 1
        # Compute the quartiles
        firstQ = 0.0
        thirdQ = 0.0
        # First quartile
        if fQpos == round(fQpos):
            firstQ = self.data[int(fQpos)]
        else:
            up = round(fQpos)
            firstQ = self.data[up - 1] + ( ( self.data[up] - self.data[up - 1]) / 4.0 )
        # Third quartile
        if tQpos == round(tQpos):
            thirdQ = self.data[int(tQpos)]
        else:
            up = round(tQpos)
            thirdQ = self.data[up - 1] + ( 3 * ( self.data[up] - self.data[up - 1]) / 4.0 )
        # Compute IQR
        IQR = thirdQ - firstQ
        numB = int(2 * IQR * m.pow(n, -1/3))
        self.SetNumBins(numB)

        assert self.numBins > 0, "Bins not set"
        assert self.binWidth > 0, "Incorrect class width"

    def computeBinWidth(self):
        """
        Computes the width of each class.
        """
        self.binWidth = (self.data[-1] - self.data[0]) / self.numBins
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
        x = self.data[0]
        self.binIntervals.clear()
        for i in range(self.numBins):
            lower = x
            x = self.data[0] + (i + 1) * self.binWidth
            upper = x
            interval = [lower, upper]
            self.binIntervals.append(interval.copy())

    def getMaxBins(self):
        """ Return the maximum number of bins """
        return len(self.data)

    def setAxis(self, axis):
        """ Set the axis name to analize """
        assert type(axis) is str, "Incorrect type."
        self.axis = axis

    def drawGrid(self):
        """ Draw a grid on the canvas """
        start = 1.0 / self.numDivisions
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
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
            x = a + i * self.binWidth
            xLabel = '{:.1f}'.format(x)
            length = GetLabelWidth(xLabel)
            length /= self.size.width
            glRasterPos2f(i * self.rectWidth - length / 2.0, -0.08)
            for c in xLabel:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))
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

        glRasterPos2f(1.08, 0.0)
        for c in self.axis:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


#------------------------------------------------------------------------------------------------------------------

class HistogramWidget(wx.Panel):
    """
    The panel containing the histogram plot and all of its controls
    """
    def __init__(self, parent, data, axis, axisName):
        super(HistogramWidget, self).__init__(parent)

        self.data = data
        self.axis = axis
        self.axisName = axisName
        self.initHistogram()
        self.initCtrls()
        self.groupControls()
        self.bindEvets()
        self.sliderMinValue = 1

    def initHistogram(self):
        """ Initialize the class for the histogram """
        # Initialize the canvas for histogram
        self.histogram = HistogramPlot(self)
        self.histogram.SetMinSize((400, 400))
        datum = [ d[self.axis] for d in self.data ]
        self.histogram.setData(datum)
        self.histogram.setAxis(self.axisName)
        # Compute the defaul number of bins
        self.histogram.computeBins()
        self.histogram.computeClassesInterval()
        self.histogram.computeFrequencies(False)

    def initCtrls(self):
        """
        Initializer the gui controls for the histogram
        """
        # Get the number of bins
        bins = self.histogram.getNumBins()
        maxBins = self.histogram.getMaxBins()
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
        self.sizer.Add(sliderSizer, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.SetSizer(self.sizer)

    def bindEvets(self):
        """
        Bind the events for the slider and text box
        """
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
