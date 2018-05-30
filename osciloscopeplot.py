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

    def InitGL(self):
        glClearColor(0.9, 0.9, 0.9, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 1.0, 0.0, 1.0, 1.0, 10.0)
        #
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glutInit(sys.argv)
        
    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw osciloscope area
        glPolygonMode(GL_FRONT, GL_FILL)
        glColor3f(0.5, 0.5, 0.5, 1)
        glRecti(0, 0, 1, 1)
        for i in range(5):
            glBegin(GL_LINES)
            glVertex3f(0.0, 0.2 * (i + 1), 0)
            glVertex3f(1, 0.2 * (i + 1), 0)
            glVertex3f(0.2 * (i + 1), 0.0, 0.0)
            glVertex3f(0.2 * (i + 1), 1.0, 0.0)
            glEnd()
        #
        self.DrawData()
        #
        self.SwapBuffers()

    def DrawData(self):
        """Draw the mean"""
        glColor3f(0, 0, 1, 1)
        r = (self.Range[1] - self.Range[0])
        y = self.data[0] / r
        glBegin(GL_LINE_STRIP)
        # Begin drawing the last value
        glVertex3f(0.5, y, 0)
        for i in range(1, len(self.data)):
            y = self.data[i] / r
            glVertex3f(0.5 - (0.1 * i), y, 0)
        glEnd()

    def SetData(self, nData):
        """
        Insert the media at the front of the list of data.
        The purpose is to have a data history
        """
        if nData <= self.Range[0]:
            self.Range[0] = nData + 20
        if nData <= self.Range[1]:
            self.Range[1] = nData + 20
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
