"""
For the parallel coordinates. A graph for visualizing high-dimensional data whitout informaiton lost.
"""

import wx

import oglCanvas as oglC

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class ParallelCoordinates(oglC.OGLCanvas):
    """
    This class contains the implementation of the parallel coordinates graph.
    It has several attributes:
        -Data: The data to be visualized. This contains all the dataset.
        -Number of axes: The dimension of the data.
        -Labels: What represents each axis.
        -Axis range: Each coordinate is (linearly) interpolated between the maximum and minimum value among all
            the possible values of that axis

    """
    def __init__(self, parent):
        super(ParallelCoordinates, self).__init__(parent)

        self.data = []
        self.dimensions = None
        self.labels = []
        self.axesRange = []

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
        glEnable(GL_TEXTURE_2D)
        glutInit(sys.argv)

    def SetData(self, newData):
        """Sets the data to be displayed and calculates the range"""
        def EqualLength(matrix):
            """Verifies that all rows of the matrix have the same length"""
            for i in range(1, len(matrix)):
                if len(matrix[i-1]) != len(matrix[i]):
                    return False
            return True

        assert newData, "Empty input"
        assert type(newData) is list, "Incorrect input type"
        assert len(newData) > 0, "Data must have length than zero"
        assert EqualLength(newData), "All rows must be the same lenght"
        if self.labels:
            assert len(self.Labels) == len(newData[0]), "Labels must be the same length as the number of dimensions"

        self.data.clear()

        # Copy data
        self.data = newData.copy()
        # Set number of dimensions
        self.dimensions = len(self.data[0])

        self.ComputeRanges()

        assert self.data, "No data copied"
        assert EqualLength(self.data), "All rows must be the same lenght"
        if self.labels:
            assert len(self.labels) == len(self.data[0]), "Labels must be the same length as the number of dimensions"
            assert self.dimensions == len(self.labels)

    def ComputeRanges(self):
        """Computes the range of each axis"""
        assert self.data, "Data must be initialized"
        assert self.dimensions != 0, "Dimensions must be initialized"

        self.axesRange.clear()
        for i in range(len(self.data[0])):
            minV = maxV = self.data[i][0]
            for j in range(len(self.data)):
                if self.data[j][i] < minV:
                    minV = self.data[j][i]
                elif self.data[j][i] > maxV:
                    maxV = self.data[j][i]
            self.axesRange.append([minV, maxV])

        assert len(self.axesRange) == len(self.data[0]), "Incorrect number of ranges " + str(len(self.axesRange)) + " " + str(len(self.data))
        assert len(self.axesRange) == self.dimensions, "Incorrect number of ranges"


    def SetLabels(self, newLabels):
        """Sets the labels of the data"""

        assert newLabels, "Labels data can not be empty"
        assert len(newLabels) > 0, "Labels can not be empty"
        if self.data:
            assert len(newLabels[0]) == len(self.data[0]), "Number of labels must be the same as the number of axes"
            assert len(newLabels[0]) == self.dimensions, "Incorrect number of labels: " % self.dimensions % ", " % len(newLabels)

        self.labels.clear()
        self.labels = newLabels[0].copy()

        assert self.labels, "Labels array empty"
        assert len(self.labels) == len(self.data[0]), "Different number of dimensions"

    def OnDraw(self):
        """Draw the graph"""
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(0.0, 0.0, 0.0)
        self.DrawBoundingBox()
        self.DrawParallelAxes()
        glColor3f(0.0, 0.0, 1.0)
        self.DrawLines()
        glColor3f(0.0, 0.5, 0.9)
        self.DrawLabels()

        self.SwapBuffers()

    def DrawBoundingBox(self):
        """Draws the bounding box of the coordinates"""
        glBegin(GL_LINE_LOOP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)
        glEnd()

    def DrawParallelAxes(self):
        """Draws the axes of the plot"""
        assert self.data, "Data must be initialized"
        assert self.dimensions > 0, "Dimensions must be greater than zero"

        # Calculate the spacing between ||-lines
        spacing = 1.0 / self.dimensions
        
        glBegin(GL_LINES)
        for i in range(self.dimensions):
            glVertex3f(i * spacing, 0.0, 0.0)
            glVertex3f(i * spacing, 1.0, 0.0)
        glEnd()

    def DrawLines(self):
        """Draws the lines representing the data"""
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
        #
        assert self.data, "Data must be initialized"
        assert self.dimensions > 0, "Dimensions must be greater than zero"
        assert len(self.data[0]) == self.dimensions, "Dimensions in data must be the same as in the variable"
        assert len(self.axesRange) > 0, "Range must be initialized"

        spacing = 1.0 / self.dimensions
        # Iterate over all rows
        for row in self.data:
            i = 0
            glBegin(GL_LINE_STRIP)
            for coord in row:
                coordNorm = Map(coord, self.axesRange[i])
                glVertex3f(i * spacing, coordNorm, 0.0)
                i += 1
            glEnd()

    def DrawLabels(self):
        """Print the labels on screen"""
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
        #
        assert self.labels, "Labels empty"
        
        spacing = 1.0 / self.dimensions
        i = 0
        for label in self.labels:
            width = GetLabelWidth(label)
            width /= self.size.width
            if i % 2 == 0:
                y = -0.04
            else:
                y = -0.08
            glRasterPos2f(i * spacing - width / 2.0, y)
            for c in label:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
            i += 1