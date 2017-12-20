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

class OsciloscopeCanvas(oglC.OGLCanvas):
    """
    Draw 'osciloscope' on canvas using OpenGL.
    The 'osciloscope' draws the media of the data, and shows it behaviour over time
    """
    def __init__(self, parent):
        super(OsciloscopeCanvas, self).__init__(parent)
        self.media = [0.5]
        self.minValue = 0
        self.maxValue = 1

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
        #glTranslatef(0.0, 0.0, -2.0)
        #glPolygonMode(GL_FRONT, GL_FILL)
        #glLineWidth(2.0)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw osciloscope area
        glPolygonMode(GL_FRONT, GL_LINE)
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
        self.DrawMedia()
        #
        self.SwapBuffers()

    def DrawMedia(self):
        """Draw the mean"""
        glColor3f(0, 0, 1, 1)
        glBegin(GL_LINE_STRIP)
        # Begin drawing the last value
        glVertex3f(0.5, self.media[0], 0)
        for i in range(1, len(self.media)):
            glVertex3f(0.5 - (0.1 * i), self.media[i], 0)
        glEnd()

    def SetMedia(self, nMedia):
        """
        Insert the media at the front of the list of media.
        The purpose is to have a media history
        """
        # Insert at front most recent value
        self.media.insert(0, nMedia)
        # Send event for redrawing (update)
        wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
