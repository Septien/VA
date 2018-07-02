"""
Generic OpenGL canvas.
"""
# wxPython
import wx
import wx.glcanvas as glcanvas

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class OGLCanvas(glcanvas.GLCanvas):
    """
    Generic OpenGL canvas for wxPython.
    Defines an abstract class for using the canvas.
    The child class should implement at least the InitGL method
    (for personalizing the canvas), and the OnDraw method.
    """

    def __init__(self, parent):
        """
        Initialize the canvas for drawing and get a context, for indicating 
        which canvas is currently in use.
        """
        glcanvas.GLCanvas.__init__(self, parent, id=wx.ID_ANY)

        self.init = False
        self.context = glcanvas.GLContext(self)
        self.size = None

        # Diminish flicker
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # # Handle events
        self.Bind(wx.EVT_SIZE, self.OnSize)                     # Resizing the window
        self.Bind(wx.EVT_PAINT, self.OnPaint)                   # Draw on canvas

    def OnSize(self, event):
        wx.CallAfter(self.SetViewPort)
        self.OnDraw()
        event.Skip()

    def SetViewPort(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, self.size.width, self.size.height)

    def OnPaint(self, event):
        # Constructs a dc object for painting on the client area
        #dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):
        """
        Initialize OpenGL. Abstract method in parent class.
        """
        raise NotImplementedError("Must override InitGL")

    def OnDraw(self):
        """
        Draw. Abstract method in parent class.
        """
        raise NotImplementedError("Must override OnDraw")
