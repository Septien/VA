"""
Module for measuring the computing time of the parallel coordinates plot.
"""

import dataIterator as dI
import wx
import parallelcoord as pc
import time as t
import unittest

class PCElNinocsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/elnino/elnino.csv')
        self.pc = pc.ParallelCoordinates(None)
        self.pc.SetData(self.cursor)

    def test_computeRanges(self):
        """ """
        with open('testPCRangesElNino.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.ComputeRanges()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_DrawLines(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCLinesElNino.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_AxisChange(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCChangeElNino.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_Filter(self):
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterElNino.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_FilterChange(self):
        """ """
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterChangeElNino.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PCForestCoverType10csv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType10/forestcovertype10.csv')
        self.pc = pc.ParallelCoordinates(None)
        self.pc.SetData(self.cursor)

    def test_computeRanges(self):
        """ """
        with open('testPCRangesForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.ComputeRanges()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_DrawLines(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCLinesForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_AxisChange(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCChangeForest10.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_Filter(self):
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_FilterChange(self):
        """ """
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterChangeForest10.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PCForestCoverTypecsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType/forestcovertype.csv')
        self.pc = pc.ParallelCoordinates(None)
        self.pc.SetData(self.cursor)

    def test_computeRanges(self):
        """ """
        with open('testPCRangesForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.ComputeRanges()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_DrawLines(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCLinesForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_AxisChange(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCChangeForest.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_Filter(self):
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_FilterChange(self):
        """ """
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterChangeForest.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PCElNinodb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="elnino_db")
        self.pc = pc.ParallelCoordinates(None)
        self.pc.SetData(self.cursor)

    def test_computeRanges(self):
        """ """
        with open('testPCRangesElNinodb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.ComputeRanges()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_DrawLines(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCLinesElNinodb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_AxisChange(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCChangeElNinodb.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_Filter(self):
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterElNinodb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_FilterChange(self):
        """ """
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterChangeElNinodb.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PCForestCoverType10db(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype10")
        self.pc = pc.ParallelCoordinates(None)
        self.pc.SetData(self.cursor)

    def test_computeRanges(self):
        """ """
        with open('testPCRangesForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.ComputeRanges()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_DrawLines(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCLinesForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_AxisChange(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCChangeForest10db.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_Filter(self):
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_FilterChange(self):
        """ """
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterChangeForest10db.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PCForestCoverTypedb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype")
        self.pc = pc.ParallelCoordinates(None)
        self.pc.SetData(self.cursor)

    def test_computeRanges(self):
        """ """
        with open('testPCRangesForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.ComputeRanges()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_DrawLines(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCLinesForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_AxisChange(self):
        """ """
        self.pc.ComputeRanges()
        with open('testPCChangeForestdb.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_Filter(self):
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_FilterChange(self):
        """ """
        self.pc.ComputeRanges()
        self.pc.setFilterAxis(11)
        self.pc.setFilterRange([20, 26])
        with open('testPCFilterChangeForestdb.txt', 'a') as file:
            for i in range(1):
                if i % 2 == 0:
                    self.pc.changeAxes(6, 11)
                else:
                    self.pc.changeAxes(11, 6)
                start = t.time()
                self.pc.DrawLines()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

def PCElNinocsvsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PCElNinocsv('test_computeRanges'))
    suite.addTest(PCElNinocsv('test_DrawLines'))
    suite.addTest(PCElNinocsv('test_AxisChange'))
    suite.addTest(PCElNinocsv('test_Filter'))
    suite.addTest(PCElNinocsv('test_FilterChange'))

    return suite

def PCForest10csvsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PCForestCoverType10csv('test_computeRanges'))
    suite.addTest(PCForestCoverType10csv('test_DrawLines'))
    suite.addTest(PCForestCoverType10csv('test_AxisChange'))
    suite.addTest(PCForestCoverType10csv('test_Filter'))
    suite.addTest(PCForestCoverType10csv('test_FilterChange'))

    return suite

def PCForestcsvsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PCForestCoverTypecsv('test_computeRanges'))
    suite.addTest(PCForestCoverTypecsv('test_DrawLines'))
    suite.addTest(PCForestCoverTypecsv('test_AxisChange'))
    suite.addTest(PCForestCoverTypecsv('test_Filter'))
    suite.addTest(PCForestCoverTypecsv('test_FilterChange'))

    return suite

#----------------------------------------------------------------------------------------------------

def PCElNinodbsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PCElNinodb('test_computeRanges'))
    suite.addTest(PCElNinodb('test_DrawLines'))
    suite.addTest(PCElNinodb('test_AxisChange'))
    suite.addTest(PCElNinodb('test_Filter'))
    suite.addTest(PCElNinodb('test_FilterChange'))

    return suite

def PCForest10dbsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PCForestCoverType10db('test_computeRanges'))
    suite.addTest(PCForestCoverType10db('test_DrawLines'))
    suite.addTest(PCForestCoverType10db('test_AxisChange'))
    suite.addTest(PCForestCoverType10db('test_Filter'))
    suite.addTest(PCForestCoverType10db('test_FilterChange'))

    return suite

def PCForestdbsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PCForestCoverTypedb('test_computeRanges'))
    suite.addTest(PCForestCoverTypedb('test_DrawLines'))
    suite.addTest(PCForestCoverTypedb('test_AxisChange'))
    suite.addTest(PCForestCoverTypedb('test_Filter'))
    suite.addTest(PCForestCoverTypedb('test_FilterChange'))

    return suite
