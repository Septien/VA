"""
Implementation of the SPLOM (Scatter Plot Matrix) graph.
Based on the sacatter plot graph. Each scatterplot displays Xi-axis vs the Xj-axis,
showing the correlation between the variables. This means that each row and each column 
corresponds to one dimension, and each cell displays two dimensions.
"""

import wx

import scatterplot_2D as sc

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class SPLOM(sc.ScatterPlot2D):
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
        self.numericVariables = 0
        self.divisions = 5
        self.databaseName = None
        self.numAxis = 0
        self.xDisplacement = 0.0
        self.yDisplacement = 0.0

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

    def SetData(self, newData):
        """Loads the data to be displayed"""
        assert newData, "Data cannot be empty"

        self.data = newData
        self.numAxis = newData.dataLength()

        assert self.data, "Data is empty"
        assert self.numAxis > 0, "Number of dimensions must greater than zero"

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

    def OnDraw(self):
        """Draw"""
        glClear(GL_COLOR_BUFFER_BIT)
        if not self.data:
            return
        # Change the viewport size in function of the number of numerical variables
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        numCells = self.numericVariables
        cellWidth = 1.0/numCells
        cellHeight = 1.0/numCells
        h = (numCells / 2.0) * (numCells - 1) * cellWidth
        k = (numCells / 2.0) * (numCells - 1) * cellHeight
        glOrtho(-0.15, h, (-k / 2.0), 1.15, 1.0, 10.0)

        glMatrixMode(GL_MODELVIEW)
        self.DrawSCPM()

        self.SwapBuffers()

    def DrawSCPM(self):
        """Draws the matrix of plots"""
        # The screen will be divided in cells, each one containing a scatterplot. All
        # cells have the same width and height, which is 1/3 (a total of 9 windows on the screen).
        numCells = self.numericVariables
        cellWidth = 1.0/numCells
        cellHeight = 1.0/numCells
        # For the numerical variables
        h, k = 1, 1
        # Iterate over all axes
        for i in range(self.numAxis):
            # If the variable type is not numeric
            if self.variablesCategory[i] != 0:
                continue
            x1 = [x[i] for x in self.data]
            self.data.rewind()
            k = 1
            for j in range(self.numAxis):
                # If the variable type is not numeric
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
                # Draw the graphs
                x2 = [x[j] for x in self.data]
                self.data.rewind()
                self.points = [x1, x2]
                self.GetRanges()
                glPushMatrix()
                glTranslatef(-cellWidth / 2.0, -cellHeight / 2.0, 0.0)
                glTranslatef(k * (cellWidth / 2.0), 1.0 - ( h * (cellHeight / 2.0)), 0.0)
                glScalef(cellWidth, cellHeight, 0.0)
                self.DrawGrid()
                self.DrawPoints(0.01)
                if i == 0:
                    glTranslatef(0.0, 1.1, 0.0)
                    self.DrawRange(self.range[1], 1)
                if j == 0:
                    glTranslatef(-0.6, 0.0, 0.0)
                    self.DrawRange(self.range[0], 0)
                glPopMatrix()
                # Increas only if the variable is numerical
                k += (numCells - 1)
                del x2
            h += (numCells - 1)
            del x1

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

    def DrawRange(self, Range, orientation):
        """ Draw the values of each axes. 
                -Range: the range of the variable.
                -Orientation: 0 -> Vertical, 1 -> horizontal.
        """
        def lerp(a, b, t):
            """For interpolating between the range [a, b], according to the formula:
            value = (1 - t) * a + t * b, for t in [0, 1]"""
            assert 0.0 <= t <= 1.0
            value = (1 - t) * a + t * b

            assert a <= value <= b, "Out of range"
            return value
        
        # Number of values to draw.
        divisions = 3
        # Horizontal
        glColor3f(0.0, 0.0, 0.0)
        for i in range(divisions):
            value = lerp(Range[0], Range[1], i / divisions)
            strValue = '{:.1f}'.format(value)
            if orientation == 0:
                glRasterPos2f(0.0, 0.5 * i)
            elif orientation == 1:
                glRasterPos2f(0.5 * i, 0.0)
            for c in strValue:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(c))


#----------------------------------------------------------------------------------------------

class SPLOMWidget(wx.Panel):
    """ Widget for the scatterplot matrix """
    def __init__(self, parent):
        super(SPLOMWidget, self).__init__(parent, -1, style=wx.RAISED_BORDER)

        self.data = None
        self.labels = None
        self.category = None

        self.splom = SPLOM(self)
        self.splom.SetMinSize((500, 500))

    def create(self, data, labels, category):
        """ Create the graph """
        if not self.splom:
            self.splom = SPLOM(self)
            self.splom.SetMinSize((500, 500))

        self.data = data
        self.labels = labels
        self.category = category
        self.initSPLOM()
        self.groupCtrls()

    def initSPLOM(self):
        """ Initialize the SPLOM """        
        self.splom.SetData(self.data)
        self.splom.SetLabels(self.labels)
        self.splom.SetCategory(self.category)

    def groupCtrls(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.splom, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        self.SetSizer(self.sizer)

    def close(self):
        """ Close all controls """
        self.DestroyChildren()
        self.splom = None
