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
        self.relFrequencies = []
        self.data = None
        self.axis = -1
        # Labels corresponding to the ith frequency
        self.labels = []
        # Colors for the sectors
        self.colors = []
        self.category = 0
        self.name = []
        self.value = []
        self.unit = ''
        self.nonDrawn = []
        self.N = 0

    def InitGL(self):
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.1, 1.35, -0.1, 1.35, 1.0, 10.0)
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
        maxClass = 10
        total = 0
        frequencies = []
        # sortedFrequencies = sorted(self.frequencies.items(), key=operator.itemgetter(1), reverse=True)
        n = len(self.frequencies)
        # if n > 10:
        #     for i in range(maxClass):
        #         frequencies.append(self.frequencies[i])
        #         total += self.frequencies[i][1]
        # else:
        #     total = self.N
        frequencies = self.frequencies
        total = self.N
        frequencies.reverse()
        # glPushMatrix()
        # glTranslatef(0.5, 0.5, 0.0)
        # glScalef(0.45, 0.45, 0.0)
        startAngle = 0.0
        i = 0
        for freq in frequencies:
            arcAngle = 360.0 * (freq[1] / total)
            # glColor3f(0.0, 0.0, 0.0)
            labelAngle = (arcAngle / 2.0) + startAngle
            radious = 1.2
            # glPushMatrix()
            # glTranslatef(-0.1, 0.0, 0.0)
            label = str(freq[0])
            if self.category == 1:  # A categorical
                k = 0
                for val in self.value:
                    if freq[0] == val:
                        label = self.name[k]
                        break
                    k += 1
            # self.drawLabels(labelAngle, label, radious, freq[1] / self.N)
            # glPopMatrix()
            # glColor3fv(self.colors[i])
            # self.DrawFilledArc(0, 0, 1, startAngle, arcAngle)
            startAngle += arcAngle
            i += 1
        # glPopMatrix()
        del freq
        del frequencies

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

    def setUnit(self, unit):
        """ Set the unit of the axis """
        self.unit = unit

    def getNonDrawnClasses(self):
        """ Return the data of the clases not drawn on the graph """
        return self.nonDrawn

    def computeFrequencies(self, draw):
        """ Compute the relative frequencies of the data """
        if not (self.data and self.labels):
            return

        # Clear any previous values
        self.frequencies.clear()
        self.frequencies = {}
        # Get the data
        datum = [d[self.axis] for d in self.data]
        self.data.rewind()
        # Compute absolute frequencies
        for d in datum:
            self.frequencies[d] = self.frequencies.get(d, 0) + 1
        # Get the total number of elements
        self.N = len(datum)
        # Compute relative frequencies
        self.relFrequencies = self.frequencies.copy()
        for f in self.relFrequencies:
            self.relFrequencies[f] /= self.N

        # Compute colors
        for i in range(self.N):
            self.colors.append([r.random(), r.random(), r.random()])

        import operator
        sortedFrequencies = sorted(self.frequencies.items(), key=operator.itemgetter(1), reverse=True)
        n = len(sortedFrequencies)
        maxClass = 10
        self.nonDrawn = []
        if n > 10:
            for i in range(n):
                self.nonDrawn.append(sortedFrequencies[i])
        else:
            total = self.N
        self.frequencies = sortedFrequencies

        # Set drawing event if required
        if draw:
            wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))

        del datum
        del sortedFrequencies
        return self.nonDrawn, self.N, self.colors[:10]  # The first 10 colors

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
        length = GetLabelWidth(label)
        x = radious * m.cos(m.radians(angle))
        y = radious * m.sin(m.radians(angle))
        if 90 <= angle <= 200:
            y += 0.2
        if y >= 1.3:
            y = 1.2
        glRasterPos2f(x, y)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        height = 25 #glutBitmapHeight(GLUT_BITMAP_HELVETICA_18)
        height /= self.size.height
        label = '{:.1f}%'.format(freq*100)
        glRasterPos2f(x, y - (2 * height))
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # Draw the name of the variable
        if self.unit != '':
            label = self.labels[self.axis] + ' (' + self.unit + ')'
        else:
            label = self.labels[self.axis]
        length = GetLabelWidth(label)
        length /= self.size.width
        glRasterPos2f(-length, 1.35)
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
        self.units = None
        self.nonDrawn = None
        self.axis = -1
        self.lvData = None
        self.colors = []
        self.N = 0
        self.values = []
        self.names = []

        self.pp = PiePlot(self)
        self.pp.SetMinSize((400, 400))

    def create(self, data, labels, axis, category, description, units):
        """ Create the graph and pass the data """
        if not self.pp:
            self.pp = PiePlot(self)
            self.pp.SetMinSize((400, 400))

        self.data = data
        self.labels = labels
        self.category = category
        self.description = description
        self.units = units
        self.axis = axis
        self.initCtrls()
        self.initPiePlot(axis)
        self.groupCtrls()

    def initPiePlot(self, axis):
        self.pp.setData(self.data)
        self.pp.setLabels(self.labels)
        self.pp.setCategory(self.category[axis])
        self.pp.setUnit(self.units[axis])
        self.values = []
        self.names = []

        for row in self.description:
            if row[axis] == '':
                break
            value, name = row[axis].split('=')
            self.values.append(int(value))
            self.names.append(name)

        self.pp.setDescription(self.values, self.names)
        self.pp.setAxis(axis)
        self.nonDrawn, self.N, self.colors = self.pp.computeFrequencies(False)
        if self.nonDrawn:
            self.initListView()

    def initListView(self):
        """ Initialize the list view for displaying the missing data """
        self.lvData.InsertColumn(0, self.labels[self.axis])
        self.lvData.InsertColumn(1, "Number of elements")
        self.lvData.InsertColumn(2, "frequency")
        self.lvData.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.lvData.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        i = 0
        n = len(self.nonDrawn)
        name = ""
        for data in self.nonDrawn:
            if self.category[self.axis] == 1:
                k = 0
                for val in self.values:
                    if data[0] == val:
                        name = self.names[k]
                        break
                    k += 1
            else:
                name = str(data[0])
            pos = self.lvData.InsertItem(i, name)
            self.lvData.SetItem(pos, 1, str(data[1]))
            f = '{:.1f}%'.format((data[1] / self.N) * 100)
            self.lvData.SetItem(pos, 2, f)
            if i < 10:
                self.lvData.SetItemBackgroundColour(pos, wx.Colour(self.colors[-1-i][0] * 255, self.colors[-1-i][1] * 255, self.colors[-1-i][2] * 255))
            i += 1

    def initCtrls(self):
        axes = []
        for i in range(self.data.dataLength()):
            axes.append(Axes(i, self.labels[i]))

        self.cb = wx.ComboBox(self, size=wx.DefaultSize, choices=[])
        self.lvData = wx.ListCtrl(self, -1, style=wx.LC_REPORT)

        # Fill the cb
        for axis in axes:
            self.cb.Append(axis.axisName, axis)

        # Bind event
        self.cb.Bind(wx.EVT_COMBOBOX, self.OnCBChange)

    def groupCtrls(self):
        label = wx.StaticText(self, -1, "Change axis:")

        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer1.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer1.Add(self.cb, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer1.Add(self.lvData, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL, 5)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.pp, 0,  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.SHAPED | wx.ALL, 5)
        self.sizer.Add(self.sizer1, 0, wx.ALIGN_LEFT)

        self.SetSizer(self.sizer)

    def OnCBChange(self, event):
        """ Handle the events for the combo box """
        cbSelection = self.cb.GetClientData(self.cb.GetSelection())
        self.axis = cbSelection.axisNumber
        self.pp.setAxis(self.axis)
        self.pp.setCategory(self.category[self.axis])
        self.pp.setUnit(self.units[self.axis])
        values = []
        names = []

        for row in self.description:
            if row[self.axis] == '':
                break
            value, name = row[self.axis].split('=')
            values.append(int(value))
            names.append(name)

        self.pp.setDescription(values, names)
        self.nonDrawn, self.N, self.colors = self.pp.computeFrequencies(True)
        if self.nonDrawn:
            # https://stackoverflow.com/questions/46818112/how-to-delete-items-on-wx-listctrl-from-another-frame
            self.lvData.DeleteAllItems()
            self.lvData.DeleteAllColumns()
            self.initListView()
            self.sizer1.Show(self.lvData, True)
        else:
            self.sizer1.Show(self.lvData, False)


    def close(self):
        """ Close all the controls """
        self.DestroyChildren()
        self.pp = None
