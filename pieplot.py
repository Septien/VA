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
        # Colors for the sectors
        self.colors = []
        self.category = 0
        self.name = []
        self.value = []

    def InitGL(self):
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.1, 1.3, -0.1, 1.1, 1.0, 10.0)
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
        i = 0
        for freq in sortedFrequencies:
            arcAngle = 360.0 * freq[1]
            glColor3f(0.0, 0.0, 0.0)
            labelAngle = (arcAngle / 2.0) + startAngle
            radious = 1.2
            glPushMatrix()
            glTranslatef(-0.1, 0.0, 0.0)
            label = str(freq[0])
            if self.category == 1:  # A categorical
                k = 0
                for val in self.value:
                    if freq[0] == val:
                        label = self.name[k]
                        break
                    k += 1
            self.drawLabels(labelAngle, label, radious, freq[1])
            glPopMatrix()
            glColor3fv(self.colors[i])
            self.DrawFilledArc(0, 0, 1, startAngle, arcAngle)
            startAngle += arcAngle
            i += 1
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

    def setCategory(self, cat):
        """ Set the category of each variable """
        self.category = cat

    def setDescription(self, value, descr):
        """ Set the description of each variable """
        self.name = descr
        self.value = value

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

        # Compute colors
        for i in range(N):
            self.colors.append([r.random(), r.random(), r.random()])
		
        # Set drawing event if required
        if draw:
            wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

    def drawLabels(self, angle, label, radious, freq):
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
        height = glutBitmapHeight(GLUT_BITMAP_HELVETICA_18)
        height /= self.size.height
        label = '{:.2f}%'.format(100*freq)
        glRasterPos2f(x, y - (2 * height))
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # Draw the name of the variable
        label = self.labels[self.axis]
        length = GetLabelWidth(label)
        length /= self.size.width
        glRasterPos2f(-length, 1.25)
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
        super(PPWidget, self).__init__(parent, style=wx.RAISED_BORDER)

        self.data = None
        self.labels = None
        self.category = None
        self.description = None

        self.pp = PiePlot(self)
        self.pp.SetMinSize((400, 400))

    def create(self, data, labels, axis, category, description):
        """ Create the graph and pass the data """
        self.data = data
        self.labels = labels
        self.category = category
        self.description = description
        self.initPiePlot(axis)
        self.initCtrls()
        self.groupCtrls()

    def initPiePlot(self, axis):
        self.pp.setData(self.data)
        self.pp.setLabels(self.labels)
        self.pp.setCategory(self.category[axis])
        values = []
        names = []

        for row in self.description:
            if row[axis] == '':
                break
            value, name = row[axis].split('=')
            values.append(int(value))
            names.append(name)

        self.pp.setDescription(values, names)
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
        axis = cbSelection.axisNumber
        self.pp.setAxis(axis)
        self.pp.setCategory(self.category[axis])
        values = []
        names = []

        for row in self.description:
            if row[axis] == '':
                break
            value, name = row[axis].split('=')
            values.append(int(value))
            names.append(name)

        self.pp.setDescription(values, names)
        self.pp.computeFrequencies(True)
