"""
Histogram and frequencies polygon plot
"""

# wxPython
import wx

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

    TODO:
        Add labels to histogram
    """
    def __init__(self, parent):
        super(HistogramPlot, self).__init__(parent)
        self.numBins = 5
        self.frequencies = []
        self.rect = []
        self.color = []
        self.maxFreq = 10
        self.maxXValue = 10

        # Drawing area width = 1.0 unit
        self.rectWidth = 1.0 / self.numBins
        for i in range(self.numBins):
            self.frequencies.append(0.5)
        self.UpdateRect()

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

        #Draw rectangles and axes
        glLineWidth(1.0)
        self.DrawRect()
        glLineWidth(2.0)
        self.DrawAxes()
        glLineWidth(1.0)
        self.DrawFreqPol()

        self.SwapBuffers()

    def DrawAxes(self):
        """
        Draw the axes of the histogram.
        """
        glColor3f(0, 0, 0, 1)
        glBegin(GL_LINES)
        # x axis
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(1.05, 0.0, 0.0)
        # y axis
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.05, 0.0)
        glEnd()

    def DrawRect(self):
        """Draw each rectangle of the histogram"""
        # Interior of the rectangles
        for i in range(self.numBins):
            glColor3f(1.0, 1.0, 1.0)
            glPolygonMode(GL_FRONT, GL_FILL)
            glRectfv(self.rect[i][0], self.rect[i][1])
        # Contour
        for i in range(self.numBins):
            glColor3f(1.0, 1.0, 0.0)
            glPolygonMode(GL_FRONT, GL_LINE)
            glRectfv(self.rect[i][0], self.rect[i][1])
            #glRecti(self.rect[i].top, self.rect[i].left, self.rect[i].bottom, self.rect[i].right)

    def DrawFreqPol(self):
        """Draws the frequency polygone"""
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 0, 0)
        for i in range(self.numBins):
            glVertex3f((self.rect[i][0][0] + self.rect[i][1][0]) / 2.0, self.frequencies[i], 0)
        glVertex3f(1, 0, 0)
        glEnd()

    def UpdateRect(self):
        if not self.frequencies:
            return
        #
        self.rect.clear()
        for i in range(self.numBins):
            rect = ((self.rectWidth * i, 0), (self.rectWidth * (1 + i), self.frequencies[i]))
            self.rect.append(rect)

    def SetFrequencies(self, freq):
        """
        Set the frequencies of the histogram. Such frequencies could not be in the range [0, 1],
        so it normalize them. Such frequency is the height of the rectangle. If the number of 
        frequencies is different to the number of bins, the latter is updated.
        """
        assert type(freq) == list, "'freq' parameter is not a list"
        # Check for consistency with bins size
        size = len(freq)
        if size != self.numBins:
            self.SetNumBins(len(freq))
        
        # Update frequencies
        self.frequencies.clear()
        self.frequencies = freq.copy()
        size = len(self.frequencies)

        # Normalize
        maxF = 0
        for i in range(size):
            if self.frequencies[i] > maxF:
                maxF = self.frequencies[i]
        
        for i in range(size):
            self.frequencies[i] /= maxF

        # Update rectangles and redraw
        self.UpdateRect()
        # For sending events:
        # https://stackoverflow.com/questions/747781/wxpython-calling-an-event-manually
        # https://www.blog.pythonlibrary.org/2010/05/22/wxpython-and-threads/
        # https://stackoverflow.com/questions/25299745/how-to-programmatically-generate-an-event-in-wxpython
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
    
    def SetNumBins(self, numB):
        """ """
        self.numBins = numB;
        #print(self.numBins)
        self.rectWidth = 1.0 / self.numBins

#------------------------------------------------------------------------------------------------------------------

class PolygonPlot(oglC.OGLCanvas):
    """Draws the frequencies polygone associated with the histogram"""
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

    def DrawPolygone(self, freqRect):
        """Draws the frequency polygone"""
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 0, 0)
        for i in range(self.numBins):
            glVertex3f((self.rect[i][0][0] + self.rect[i][1][0]) / 2.0, self.frequencies[i], 0)
        glVertex3f(1, 0, 0)
        glEnd()

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)