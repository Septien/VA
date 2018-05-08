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
        self.divisions = 5
        self.databaseName = None
        self.numAxis = 0
        self.xDisplacement = 0.0
        self.yDisplacement = 0.0

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

    def SetData(self, newData):
        """Loads the data to be displayed"""
        def EqualLenght(inputArray):
            """Verifies that all the elements in the input are of equal length"""
            for i in range(1, len(inputArray)):
                if len(inputArray[i-1]) != len(inputArray[i]):
                    return False
            return True
        #
        assert newData, "Data cannot be empty"
        assert EqualLenght(newData), "All rows must be the same length"

        self.data = newData
        self.numAxis = len(newData[0])

        # Init scroll bar
        # if self.numAxis > 

        assert self.data, "Data is empty"
        assert EqualLenght(self.data), "Data is not the same length"
        assert self.numAxis > 0, "Number of dimensions must greater than zero"

    def SetLabels(self, newVarNames):
        """Loads the names of each of the variables to be displayed."""
        assert newVarNames, "Variable name labels cannot be empty"
        if self.data:
            assert len(newVarNames) == len(self.data[0]), "Unequal size: " + str(len(newVarNames)) + " " + str(len(self.data[0]))

        self.variablesName.clear()
        self.variablesName = newVarNames

        assert self.variablesName, "Labels not loaded"
        if self.data:
            assert len(self.variablesName) == len(self.data[0]), "Number of labels must be the same as the number of dimension"

    def LoadDatabaseName(self, dbName):
        """Load the name of the database to be displayed"""
        assert type(dbName) is str, "Incorrect name format: " + str(type(dbName))

        self.databaseName = dbName

        assert self.databaseName, "Name of database not initialized"
        assert type(self.databaseName) is str, "Incorrect database name format: " + str(type(self.databaseName))

    def GetNumAxes(self):
        """Returns the number of axes on the points"""
        return self.points

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
        

    def DrawSCPM(self):
        """Draws the matrix of plots"""
        # Iterate over all axes
        count = 1
        for i in range(self.numAxis):
            x1 = [x[i] for x in self.data]
            for j in range(self.numAxis):                
                if i == j:
                    # if i == j, draw the name of the variable
                    glPushMatrix()
                    glTranslatef(1.0 / (2.0 * self.numAxis), -1.0 / (2.0 * self.numAxis), 0.0)
                    glTranslatef(j / self.numAxis, 1.0 - (i / self.numAxis), 0.0)
                    self.DrawNames(i)
                    glPopMatrix()
                    continue
                # Draw the graphs
                x2 = [x[j] for x in self.data]
                self.points = [x1, x2]
                self.GetRanges()
                glPushMatrix()
                glTranslatef(0.125, 0.125, 0.0)
                glTranslatef(j / self.numAxis, 1.0 - ((i + 1) / self.numAxis), 0.0)
                glScalef(0.2, 0.2, 0.0)
                glTranslatef(-0.5, -0.5, 0.0)
                super(SPLOM, self).DrawGrid()
                super(SPLOM, self).DrawPoints(0.03)
                glPopMatrix()

    def DrawNames(self, i):
        """Draw the names of the variable.
            i: The position of the name on the labels array """
        assert type(i) is int, "Incorrect type: " + str(type(i))
        assert 0 <= i <= len(self.variablesName)
        label = self.variablesName[i]
        glRasterPos2f(0.0, 0.0)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

#----------------------------------------------------------------------------------------------

class SPLOMWidget(wx.Panel):
    """ Widget para la matriz de gráficas de dispersión """
    def __init__(self, parent, data, labels):
        super(SPLOMWidget, self).__init__(parent)

        self.data = data
        self.labels = labels
        self.initSPLOM()
        self.groupCtrls()

    def initSPLOM(self):
        """ Initialize the SPLOM """
        self.splom = SPLOM(self)
        self.splom.SetData(self.data)
        self.splom.SetLabels(self.labels)
        self.splom.SetMinSize((500, 500))

    def groupCtrls(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.splom, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
