"""
Osciloscope plot
"""

# wxPython
import wx

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# OpenGL canvas
import oglCanvas as oglC

class Osciloscope(oglC.OGLCanvas):
    """
    Draw 'osciloscope' on canvas using OpenGL.
    The 'osciloscope' draws the media of the data, and shows it behaviour over time
    """
    def __init__(self, parent):
        super(Osciloscope, self).__init__(parent)
        self.data = []
        self.Range = [0, 0]
        self.varName = ""
        self.numDivisions = 10

    def InitGL(self):
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.1, 1.01, -0.05, 1.05, 1.0, 10.0)
        #
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glutInit(sys.argv)
        
    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.DrawGrid()
        #
        self.DrawData()
        #
        self.DrawLabels()
        self.SwapBuffers()

    def DrawGrid(self):
        """ Draw the grid of the osciloscope """
        # Draw osciloscope area
        glPolygonMode(GL_FRONT, GL_LINE)
        glColor3f(0.5, 0.5, 0.5, 1)
        # Dotted line
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glRecti(0, 0, 1, 1)
        glBegin(GL_LINES)
        for i in range(self.numDivisions):
            glVertex3f(0.0, 0.1 * (i + 1), 0)
            glVertex3f(1, 0.1 * (i + 1), 0)
            glVertex3f(0.1 * (i + 1), 0.0, 0.0)
            glVertex3f(0.1 * (i + 1), 1.0, 0.0)
        glEnd()
        glPopAttrib()

    def DrawData(self):
        """Draw the mean"""
        glColor3f(0, 0, 1, 1)
        r = (self.Range[1] - self.Range[0])
        y = (self.data[0] - self.Range[0]) / r
        glBegin(GL_LINE_STRIP)
        # Begin drawing the last value
        glVertex3f(0.99, y, 0)
        for i in range(1, len(self.data)):
            y = (self.data[i] - self.Range[0]) / r
            x = 0.99 - (0.1 * i)
            if x < -0.03:
                continue
            glVertex3f(x, y, 0)
        glEnd()

    def SetData(self, nData):
        """
        Insert the media at the front of the list of data.
        The purpose is to have a data history
        """
        if nData <= self.Range[0]:
            self.Range[0] = nData - 1
        if nData >= self.Range[1]:
            self.Range[1] = nData + 1
        # Insert at front most recent value
        self.data.insert(0, nData)
        # Send event for redrawing (update)
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

    def SetRange(self, nrange):
        """ Sets the range of the variable """
        self.Range = nrange.copy()

    def SetVariableName(self, varName):
        """ Set the name of the variable """
        self.varName = varName

    def DrawLabels(self):
        """ Draw the values of each axis and the name of the variable """
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
        def lerp(a, b, t):
            """For interpolating between the range [a, b], according to the formula:
            value = (1 - t) * a + t * b, for t in [0, 1]"""
            assert 0.0 <= t <= 1.0
            value = (1 - t) * a + t * b

            assert a <= value <= b, "Out of range"
            return value
        #
        # Draw the name of the variable
        length = GetLabelWidth(self.varName)
        if self.size:
            length /= self.size.width
        glColor3f(0.0, 0.0, 0.0)
        glRasterPos2f(0.5 - length / 2, 1.015)
        for c in self.varName:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # Draw the values of the range
        divWidth = 1.0 / self.numDivisions
        for i in range(self.numDivisions + 1):
            x = lerp(self.Range[0], self.Range[1], i / self.numDivisions)
            xLabel = '{:.1f}'.format(x)
            length = GetLabelWidth(xLabel)
            if self.size:
                length /= self.size.width
            glRasterPos2f(-0.09, i * divWidth)
            for c in xLabel:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

#------------------------------------------------------------------------------------------------------------------

class OsciloscopeWidget(wx.Panel):
    """ Handles the widget of the osciloscope """
    def __init__(self, parent):
        super(OsciloscopeWidget, self).__init__(parent, style=wx.RAISED_BORDER)

        self.osc = Osciloscope(self)
        self.osc.SetMinSize((400, 400))

    def create(self, varName):
        self.osc.SetVariableName(varName)
        self.osc.SetRange([0, 1])
        self.initCtrls()

    def initCtrls(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.osc, 0, wx.ALIGN_CENTER | wx.SHAPED | wx.ALL, 5)
        self.SetSizer(sizer)

    def Next(self, value):
        """ Inserts the next value of the stream """
        self.osc.SetData(value)
