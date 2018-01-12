"""
A gauge is an instrument that displays the measurement of a variable.
Such variable may be mechanical, electrical, or even logical (comming from a software).
A gauge plot is the implementation of a gauge via software.
For the gauge plot.
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

class GaugePlot(oglC.OGLCanvas):
    """
    Class for drawing the gauge plot. It will hold the range within which the
    variable to be displayed is define (the range). It will be possible to change such range.
    It will be displayed the beginning and end of the range, as well as marks 
    at regular intervals (to be defined). It will hold an arrow, which will point to 
    a the value of the input data at the moment. Animiations are to be done.
    """
    def __init__(self, parent):
        # ctor
        super(GaugePlot, self).__init__(parent)
        # The value of the data to be displayed
        self.data = None
        # Range of the data
        self.range = []
        self.marksSpacer = None
        # Angle of rotation
        self.theta = 0.0

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

    def SetRange(self, nRange):
        """Stablishes the range of the variable"""
        assert type(nRange) is list, "Invalid input type"
        assert self.data in nRange, "Current variable out of range"

        if self.range:
            self.range.clear()
        self.range = nRange.copy()
        # TODO: Change orientation of arrow (theta).

        assert self.data in self.range, "Variable out of current range"

    def SetValue(self, nValue):
        """Sets the value of the data"""
        assert type(nValue) is int, "Incorret input format"
        assert nValue in self.range, "Variable out of range"

        self.data = nValue
        # TODO: Calculate the rotating angle of the arrow

        assert self.data in self.range, "Data out of range"


    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Draw outer circle
        glColor3f(0.8, 0.8, 0.8)
        glPushMatrix()
        glTranslatef(0.5, 0.5, 0.0)
        glScale(0.5, 0.5, 1.0)
        self.DrawCircle(GL_TRIANGLE_FAN)

        # Draw border
        glColor3f(0.0, 0.0, 0.0)
        self.DrawCircle(GL_LINE_LOOP)
        
        # Draw inner circle
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glScale(0.95, 0.95, 1.0)
        self.DrawCircle(GL_TRIANGLE_FAN)
        glPopMatrix()
        glPopMatrix()
        
        # Draw marks
        glLineWidth(1.0)
        glColor3f(0.0, 0.0, 0.0)
        self.DrawMainMarks()
        glLineWidth(0.5)
        self.DrawSecondaryMarks()
        
        # Arrow
        glPushMatrix()
        glScale(0.5, 0.6, 1.0)
        glTranslatef(0.5, 0.5, 0.0)
        glRotatef(self.theta, 0.0, 1.0, 0.0)
        #self.DrawArrow()
        glPopMatrix()
        self.SwapBuffers()

    def DrawArrow(self):
        """Draws the arrow that indicates the current value of the data
        The arrow must be scalated to fit within the gauge, and rotated to point to the apropiate position"""
        # Rectangle part: -
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(0.5, 0.0, 0.0)
        glEnd()
        # Triangle part: >
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.25, 0.5, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(0.75, 0.5, 0.0)
        glEnd()

    def DrawBigStick(self):
        """Draws the stick corresponding to the main marks"""
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.125, 0.0)
        # glVertex3f(0.0, 0.875, 0.0)
        # glVertex3f(0.0, 1.0, 0.0)
        # glVertex3f(0.5, 0.875, 0.0)
        # glVertex3f(0.5, 1.0, 0.0)
        glEnd()

    def DrawSmallStick(self):
        """"""
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.9375, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glEnd()

    def DrawMainMarks(self):
        """Draw the marks on the circle based on the interval.
        The marks are on a circle with radious less than one."""
        numMarks = 5
        theta = -144.0
        incTheta = 72.0
        glRotatef(-45.0, 0.0, 1.0, 0.0)
        self.DrawBigStick()
        glPushMatrix()
        glTranslatef(0.5, 0.5, 0.0)
        #self.DrawBigStick()
        glPopMatrix()
        # for i in range(numMarks):
        #     glPushMatrix()
        #     glTranslatef(0.5, 0.5, 0.0)
        #     glRotatef(theta, 0.0, 1.0, 0.0)
        #     self.DrawBigStick()
        #     glPopMatrix()
        #     theta += incTheta 

    def DrawSecondaryMarks(self):
        """These marks are smaller in length and width"""
        numMarks = 20
        theta = -144.0
        incTheta = 18.0
        for i in range(numMarks):
            glPushMatrix()
            #glRotatef(theta, 0.0, 1.0, 0.0)
            self.DrawSmallStick()
            glPopMatrix()
            theta += incTheta

    def DrawCircle(self, mode):
        """Draws a circle of radious 1"""
        assert mode == GL_LINE_LOOP or mode == GL_TRIANGLE_FAN, "Incorrect drawing mode"
        glBegin(mode)
        # Draw upper arc
        for x in np.arange(1.0, -1.0, -0.01):
            y = m.sqrt(1 - x * x)
            glVertex3f(x, y, 0.0)
        # Draw lowwer arc
        for x in np.arange(-1.0, 1.0, 0.01):
            y = m.sqrt(1 - x * x)
            glVertex3f(x, -y, 0.0)
        glEnd()
