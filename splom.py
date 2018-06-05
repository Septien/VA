"""
Implementation of the SPLOM (Scatter Plot Matrix) graph.
Based on the sacatter plot graph. Each scatterplot displays Xi-axis vs the Xj-axis,
showing the correlation between the variables. This means that each row and each column 
corresponds to one dimension, and each cell displays two dimensions.
"""

import wx
import wx.lib.scrolledpanel as scp

import numpy as np
import math as m

import scatterplot_2D as sc

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import oglCanvas as oglC

class SPLOM(oglC.OGLCanvas):
    """
    The implementation of the SPLOM graph. This class inherites from the scatterplor 2d class.
    It contains the following attributes:
        -data: the data to be plotted on screen.
        -variablesName: Corresponding to each variable.
    The data will be passed to the parent class each time the plot has to be painted.
    """

    def __init__(self, parent):
        super(SPLOM, self).__init__(parent)
        self.data = []
        self.variablesName = []
        self.variablesCategory = []
        self.ranges = []
        self.numericVariables = 0
        self.divisions = 5
        self.databaseName = None
        self.numAxis = 0
        self.xDisplacement = 0.0
        self.yDisplacement = 0.0
        self.InitCirclePoints()

    def InitGL(self):
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        #
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.01, 1.01, -0.01, 1.01, 1.0, 10.0)
        #
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glutInit(sys.argv)

    def InitCirclePoints(self):
        """
        Constructs an array containing the points for a circle centered at the origin
        and with radious 1.
        """
        self.circle = []

        x = 0.0
        y = 0.0
        # Upper half
        for x in np.arange(1.0, -1.0, -0.01):
            y = m.sqrt(1 - x * x)
            self.circle.append((x, y))
        # Lower half
        for x in np.arange(-1.0, 1.0, 0.01):
            y = - m.sqrt(1 - x * x)
            self.circle.append((x, y))

    def SetData(self, newData):
        """Loads the data to be displayed"""
        assert newData, "Data cannot be empty"

        self.data = newData
        self.numAxis = newData.dataLength()
        # Compute the ranges of each variable
        self.getRanges()

        assert self.data, "Data is empty"
        assert self.numAxis > 0, "Number of dimensions must greater than zero"

    def getRanges(self):
        """ Get the ranges of each variable """
        self.ranges.clear()
        d = next(self.data)
        # Initialize the ranges
        for i in range(self.numAxis):
            minV = maxV = d[i]
            self.ranges.append([minV, maxV])
        # Get the ranges
        j = 0
        for d in self.data:
            for i in range(self.numAxis):
                # The minimum
                if d[i] <= self.ranges[i][0]:
                    self.ranges[i][0] = d[i]
                # The maximum
                if d[i] >= self.ranges[i][1]:
                    self.ranges[i][1] = d[i]
            j += 1
        # Return to first data
        self.data.rewind()

    def SetLabels(self, newVarNames):
        """Loads the names of each of the variables to be displayed."""
        assert newVarNames, "Variable name labels cannot be empty"
        if self.data:
            assert len(newVarNames) == self.data.dataLength(), "Unequal size: " + str(len(newVarNames)) + " " + str(self.data.dataLength())

        self.variablesName.clear()
        self.variablesName = newVarNames

        assert self.variablesName, "Labels not loaded"
        if self.data:
            assert len(self.variablesName) == self.data.dataLength(), "Number of labels must be the same as the number of dimension"

    def SetCategory(self, category):
        """ Loads the category of each of the variables. Assumes one-to-one correspondance, and
        that the indexes corresponds to each other. """
        assert type(category) is list, "Incorrect input type"
        assert len(category) == self.numAxis, "Incorrect length of category array"

        # Store reference
        self.variablesCategory = category
        # Compute the number of numerica variables
        for c in self.variablesCategory:
            if c == 0:
                self.numericVariables += 1

        assert self.variablesCategory, "Category array not initilize"

    def LoadDatabaseName(self, dbName):
        """Load the name of the database to be displayed"""
        assert type(dbName) is str, "Incorrect name format: " + str(type(dbName))

        self.databaseName = dbName

        assert self.databaseName, "Name of database not initialized"
        assert type(self.databaseName) is str, "Incorrect database name format: " + str(type(self.databaseName))

    def GetNumAxes(self):
        """Returns the number of axes"""
        return self.numAxis

    def SetDisplace(self, x = 0.0, y = 0.0):
        """Set the displacement in the x and y axis of the figure"""
        self.xDisplacement = x
        self.yDisplacement = y

    def OnDraw(self):
        """Draw"""
        glClear(GL_COLOR_BUFFER_BIT)
        if not self.data:
            return
        
        glPushMatrix()
        glTranslatef(self.xDisplacement, self.yDisplacement, 0.0)
        self.DrawSCPM()
        glPopMatrix()
        
        self.SwapBuffers()

    def DrawGrid(self):
        # Grid
        start = 1.0 / self.divisions
        glColor3f(0.0, 0.0, 0.0)
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(1, 0xAAAA)
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINES)
        for i in range(self.divisions + 1):
            x = i * start
            glVertex3f(x, 0.0, 0.1)
            glVertex3f(x, 1.0, 0.1)
            glVertex3f(0.0, x, 0.1)
            glVertex3f(1.0, x, 0.1)
        glEnd()
        glPopAttrib()

    def DrawCircle(self):
        """
        Draw a circle based on the points previously calculated. Uses a triangle fan.
        """
        #glBegin(GL_LINE_LOOP)
        glBegin(GL_TRIANGLE_FAN)
        for i in range(len(self.circle)):
            glVertex3f(self.circle[i][0], self.circle[i][1], 0.0)
        glEnd()

    def DrawPoint(self, cx, cy, r):
        """
        Draw a point centered at (cx, cy) with radious r.
        It is based on the function draw circle.
        """
        glPushMatrix()
        glTranslatef(cx, cy, 0.0)
        glScalef(r, r, 0.0)
        self.DrawCircle()
        glPopMatrix()

    def DrawSCPM(self):
        """Draws the matrix of plots"""
        def Map(value, Range):
            """Map the value in range [range[0], range[1]] to the range [0, 1]"""
            # Formula for mapping [A, B] -> [a, b]:
            #
            #   (val - A) * (b - a) / (B - A) + a
            assert type(value) is (float or int), str(type(value))
            assert len(Range) > 0
            unitRange = [0.0, 1.0]

            norm = ((value - Range[0]) * (unitRange[1] - unitRange[0]) / (Range[1] - Range[0])) + unitRange[0]
            assert unitRange[0] <= norm <= unitRange[1], "Out of range: " + str(norm) + " " + str(Range) + " " + str(value)
            return norm

        numCells = self.numericVariables
        cellWidth = 1.0/numCells
        cellHeight = 1.0/numCells
        # Draw the grids and names
        k, h = 0, 0
        for i in range(self.numAxis):
            if self.variablesCategory[i] != 0:
                continue
            k = 1
            for j in range(self.numAxis):
                if self.variablesCategory[j] != 0:
                    continue
                if i == j:
                    # if i == j, draw the name of the variable
                    glPushMatrix()
                    glTranslatef(k * (cellWidth / 2.0), 1.0 - ( h * (cellHeight / 2.0)), 0.0)
                    self.DrawNames(i)
                    glPopMatrix()
                    k += (numCells - 1)
                    continue
                glPushMatrix()
                glTranslatef(-cellWidth / 2.0, -cellHeight / 2.0, 0.0)
                glTranslatef(k * (cellWidth / 2.0), 1.0 - ( h * (cellHeight / 2.0)), 0.0)
                glScalef(cellWidth, cellHeight, 0.0)
                self.DrawGrid()
                glPopMatrix()

                # Increas only if the variable is numerical
                k += (numCells - 1)
            h += (numCells - 1)
        glColor3f(0.0, 0.0, 1.0)
        for data in self.data:
            for i in range(len(data)):
                if self.variablesCategory[i] != 0:
                    continue
                for j in range(i + 1, len(data)):
                    if self.variablesCategory[j] != 0:
                        continue
                    glPushMatrix()
                    # glTranslatef(-cellWidth / 2.0, -cellHeight / 2.0, 0.0)
                    # glTranslatef(k * (cellWidth / 2.0), 1.0 - ( h * (cellHeight / 2.0)), 0.0)
                    glScalef(cellWidth, cellHeight, 0.0)
                    # Normalize x
                    x = Map(data[i], self.ranges[i])
                    # Normalize y
                    y = Map(data[j], self.ranges[j])
                    self.DrawPoint(x, y, 0.01)
                    glPopMatrix()
        self.data.rewind()

    def DrawNames(self, i):
        """Draw the names of the variable.
            i: The position of the name on the labels array """
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
        assert type(i) is int, "Incorrect type: " + str(type(i))
        assert 0 <= i <= len(self.variablesName)

        glColor3f(0.0, 0.0, 0.0)
        label = self.variablesName[i]
        length = GetLabelWidth(label)
        length /= self.size.width
        glTranslatef(-length/2.0, 0.0, 0.0)
        glRasterPos2f(0.0, 0.0)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

#----------------------------------------------------------------------------------------------

class SPLOMWidget(scp.ScrolledPanel):
    """ Widget for the scatterplot matrix """
    def __init__(self, parent):
        super(SPLOMWidget, self).__init__(parent, -1, style=wx.RAISED_BORDER, size=(500, 400))

        self.data = None
        self.labels = None
        self.category = None

        self.splom = SPLOM(self)
        self.splom.SetMinSize((500, 400))

    def create(self, data, labels, category):
        """ Create the graph """
        if not self.splom:
            self.splom = SPLOM(self)
            self.splom.SetMinSize((500, 400))

        self.data = data
        self.labels = labels
        self.category = category
        self.initSPLOM()
        self.groupCtrls()
        self.SetupScrolling()

    def initSPLOM(self):
        """ Initialize the SPLOM """        
        self.splom.SetData(self.data)
        self.splom.SetLabels(self.labels)
        self.splom.SetCategory(self.category)

    def groupCtrls(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.splom, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)

    def close(self):
        """ Close all controls """
        self.DestroyChildren()
        self.splom = None