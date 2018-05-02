"""
A Pie plot.
"""

# wxPython
import wx

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# OpenGL canvas
import oglCanvas as oglC

#
import random as r

#
import math as m

class PiePlot(oglC.OGLCanvas):
	"""
	Pie plot. Displays frequencies of an attribute based on the proportion of the
	carachteristic respect to the total number of them.
	"""
	def __init__(self, parent):
		"""
		"""
		super(PiePlot, self).__init__(parent)
		# Relative frequency
		self.frequencies = []
		# Labels corresponding to the ith frequency
		self.labels = []

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
		self.DrawPie()
		self.SwapBuffers()

	def DrawPie(self):
		"""
		Draw the pie based on the of frequencies. The lenght of the arc (angle) is
		proportinal to relative frequencies.
		"""
		r.seed()
		glPushMatrix()
		glTranslatef(0.5, 0.5, 0.0)
		glScalef(0.5, 0.5, 0.0)
		startAngle = 0.0
		for freq in self.frequencies:
			arcAngle = 360.0 * freq
			glColor3f(r.random(), r.random(), r.random())
			self.DrawFilledArc(0, 0, 1, startAngle, arcAngle)
			startAngle += arcAngle
		glPopMatrix()

	def DrawFilledArc(self, cx, cy, r, startAngle, arcAngle):
		"""
		Draw an arc centered at (cx, cy), and with radious r.
		Starts at start_angle with a length of arc_angle.
		Color setting is up to the caller.
		"""
		# http://slabode.exofire.net/circle_draw.shtml
		# Number of segments
		numberSegments = 1000
		theta = arcAngle / (numberSegments - 1.0)
		thetaRadians = m.radians(theta)
		
		tangentialFactor = m.tan(thetaRadians)
		radialFactor = m.cos(thetaRadians)

		rStartAngle = m.radians(startAngle)
        # Starting points
		x = r * m.cos(rStartAngle)
		y = r * m.sin(rStartAngle)

		# Draw arc using a triangle fan
		glBegin(GL_TRIANGLE_FAN)
		#glBegin(GL_LINE_STRIP)
		# Center
		glVertex3f(cx, cy, 0.0)
		for i in range(numberSegments):
			tx = -y
			ty = x

			x += tx * tangentialFactor
			y += ty * tangentialFactor

			x *= radialFactor
			y *= radialFactor

			glVertex3f(x, y, 0.0)
		glEnd()

	def computeFrequencies(self):
		""" Compute the relative frequencies of the data """
		wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
