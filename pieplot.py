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
		self.frequencies = {}
		self.data = None
		self.axis = -1
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
		# Get the frequencies ordered
		import operator
		sortedFrequencies = sorted(self.frequencies.items(), key=operator.itemgetter(1))
		r.seed()
		glPushMatrix()
		glTranslatef(0.5, 0.5, 0.0)
		glScalef(0.45, 0.45, 0.0)
		startAngle = 0.0
		for freq in sortedFrequencies:
			arcAngle = 360.0 * freq[1]
			glColor3f(0.0, 0.0, 0.0)
			labelAngle = (arcAngle / 2.0) + startAngle
			radious = 1.15
			glPushMatrix()
			glTranslatef(-0.1, 0.0, 0.0)
			self.drawLabels(labelAngle, str(freq[0]), radious)
			glPopMatrix()
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

	def setData(self, data):
		""" Sets the data """
		# Store a reference
		self.data = data

		assert self.data, "Data not copied"

	def setLabels(self, labels):
		""" Set the labels for the graph """
		assert type(labels) is list, "Incorrect input type: is " + str(type(labels)) + " must be list."

		self.labels = labels

		assert self.labels, "Labels not set"
		if self.data:
			assert self.data.dataLength() == len(self.labels), "Incorrect number of labels"

	def setAxis(self, axis):
		""" Set the number of the axis to analize """
		assert type(axis) is int, "Incorrect input type: is " + str(type(axis)) + " must be integer."
		assert axis > -1, "Axis must be greater than zero"
		if self.data:
			assert axis < self.data.dataLength(), "Axis must be less than: " + str(self.data.dataLength())

		self.axis = axis

	def computeFrequencies(self, draw):
		""" Compute the relative frequencies of the data """
		if not (self.data and self.labels):
			return

		# Clear any previous values
		self.frequencies.clear()
		# Get the data
		datum = [d[self.axis] for d in self.data]
		self.data.rewind()
		# Compute absolute frequencies
		for d in datum:
			self.frequencies[d] = self.frequencies.get(d, 0) + 1
		# Get the total number of elements
		N = len(datum)

		# Compute relative frequencies
		for f in self.frequencies:
			self.frequencies[f] /= N

		# Set drawing event if required
		if draw:
			wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

	def drawLabels(self, angle, label, radious):
		""" Draw the labels of the pieplot.
				-angle: Angle at which the label is to be drawn.
				-label: label to draw.
		"""
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

		# Draw the value variables
		lenght = GetLabelWidth(label)
		x = radious * m.cos(m.radians(angle))
		y = radious * m.sin(m.radians(angle))
		glRasterPos2f(x, y)
		for c in label:
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

#------------------------------------------------------------------------------------------------------------------

class Axes:
    """ Simple class containing the axes name and number """
    def __init__(self, number, name):
        self.axisNumber = number
        self.axisName = name

#------------------------------------------------------------------------------------------------------------------

class PPWidget(wx.Panel):
    """
        Widget containing all the controls necessary for interacting with the pieplot.
    """
    def __init__(self, parent):
        super(PPWidget, self).__init__(parent)

        self.data = None
        self.labels = None

        self.pp = PiePlot(self)
        self.pp.SetMinSize((400, 400))

    def create(self, data, labels, axis):
        """ Create the graph and pass the data """
        self.data = data
        self.labels = labels
        self.initPiePlot(axis)
        self.initCtrls()
        self.groupCtrls()

    def initPiePlot(self, axis):
        self.pp.setData(self.data)
        self.pp.setLabels(self.labels)
        self.pp.setAxis(axis)
        self.pp.computeFrequencies(False)

    def initCtrls(self):
        axes = []
        for i in range(self.data.dataLength()):
            axes.append(Axes(i, self.labels[i]))

        self.cb = wx.ComboBox(self, size=wx.DefaultSize, choices=[])

        # Fill the cb
        for axis in axes:
            self.cb.Append(axis.axisName, axis)

        # Bind event
        self.cb.Bind(wx.EVT_COMBOBOX, self.OnCBChange)

    def groupCtrls(self):
        label = wx.StaticText(self, -1, "Change axis:")

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL)
        sizer1.Add(self.cb, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.pp, 0,  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.SHAPED | wx.ALL, 5)
        self.sizer.Add(sizer1, 0, wx.ALIGN_LEFT)

        self.SetSizer(self.sizer)

    def OnCBChange(self, event):
        """ Handle the events for the combo box """
        cbSelection = self.cb.GetClientData(self.cb.GetSelection())
        self.pp.setAxis(cbSelection.axisNumber)
        self.pp.computeFrequencies(True)
