"""
Scatter plot.
"""

#wxPython
import wx

# Pygame
import pygame
from pygame.locals import *

import oglCanvas as oglC

# OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#random
import random as r

class ScatterPlot(oglC.OGLCanvas):
	"""Scatter plot."""
	def __init__(self, parent):
		super(ScatterPlot, self).__init__(parent)
		self.points = []
		self.labels = []

		self.initCube()

		# Handle keyboard events
		self.Bind(wx.EVT_CHAR, self.OnChar)

		# Sample points
		r.seed()
		for i in range(100):
			self.points.append([r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1)])


	def initCube(self):
		"""Initialize the cube on the background, it defines the grid over which
		the plot will be displayed."""
		# Face for the cube. 	Format:		[x, y, z]
		self.face = [[1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [-1.0, 1.0, 1.0]]
		# For the grid
		self.square = [[1.0, -1.0, 1.0], [1.0, -0.5, 1.0], [0.5, -1.0, 1.0], [0.5, -0.5, 1.0]]
		
	def InitGL(self):
		glClearColor(0.9, 0.9, 0.9, 1)
		glMatrixMode(GL_PROJECTION)
		# camera frustrum setup
		aspect = self.size.width / self.size.height
		fovy = 50.0
		gluPerspective(fovy, aspect, 0.5, 10.0)
		#
		glDepthFunc(GL_GREATER)
		glEnable(GL_DEPTH_TEST)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		# Enable face culling
		glEnable(GL_CULL_FACE)
		glCullFace(GL_FRONT)
		# position viewer
		glMatrixMode(GL_MODELVIEW)
		gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
		glShadeModel(GL_SMOOTH)
		glutInit(sys.argv)

	def OnDraw(self):
		""""""
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.DrawCube()
		self.SwapBuffers()
		
	def DrawCube(self):
		""" """
		glPushMatrix()
		glRotate(45.0, 0, 1, 0)
		glRotate(45.0, 1, 0, 0)

		# Draw the faces
		# Top
		self.Draw(-90.0, 1, 0, 0)
		# Bottom
		self.Draw(90.0, 1, 0, 0)
		# Front
		self.Draw(0.0, 1, 0, 0)
		# Back
		self.Draw(180.0, 1, 0, 0)
		# Left
		self.Draw(-90.0, 0, 1, 0)
		# Right
		self.Draw(90.0, 0, 1, 0)
		# Draw points
		self.DrawPoints()
		glPopMatrix()

	def DrawFace(self):
		glPolygonMode(GL_BACK, GL_FILL)
		glColor(0.0, 0.9, 0.9, 1.0)
		glBegin(GL_TRIANGLE_STRIP)
		glVertex3fv(self.face[0])
		glVertex3fv(self.face[1])
		glVertex3fv(self.face[2])
		glVertex3fv(self.face[3])
		glEnd()	

	def DrawGrid(self):
		glPolygonMode(GL_BACK, GL_LINE)
		for j in range(4):
			glPushMatrix()
			glTranslate(0.0, j * 0.5, 0.0)
			for i in range(4):
				glPushMatrix()
				glTranslate(-i * 0.5, 0.0, 0.0)
				self.DrawSquare()
				glPopMatrix()
			glPopMatrix()

	def DrawSquare(self):
		glColor(0.0, 0.0, 0.0, 1.0)
		glBegin(GL_QUADS)
		glVertex3fv(self.square[0])
		glVertex3fv(self.square[1])
		glVertex3fv(self.square[3])
		glVertex3fv(self.square[2])
		glEnd()
	
	def Draw(self, theta, x, y, z):
		"""Draw each square of the plot, along with their grid.
		Receives the axis of rotation and the angle"""
		glPushMatrix()
		glRotate(theta, x, y, z)
		self.DrawFace()
		self.DrawGrid()
		glPopMatrix()

	def OnChar(self, event):
		"""After pressing a key, get the char of the key"""
		keycode = event.GetUnicodeKey()
		if keycode == wx.WXK_NONE:
			keycode = event.GetKeyCode()
			# Special key
			if keycode == wx.WXK_LEFT:
				glRotate(10.0, 0, 1, 0)

			if keycode == wx.WXK_RIGHT:
				glRotate(-10.0, 0, 1, 0)

			if keycode == wx.WXK_UP:
				glRotate(10.0, 1, 0, 0)

			if keycode == wx.WXK_DOWN:
				glRotate(-10.0, 1, 0, 0)

			wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

	def DrawPoints(self):
		"""Draw the points in the histogram"""
		for i in range(len(self.points)):
			glPushMatrix()
			glTranslatef(self.points[i][0], self.points[i][1], self.points[i][2])
			#glColor3f(0, 1, 0)
			glutSolidSphere(0.02, 100, 100)
			glPopMatrix()
