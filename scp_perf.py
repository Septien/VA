"""
Module for measuring the performance of the scatterplot.
"""

import dataIterator as dI
import wx
import scatterplot_2D as scp
import time as t
import unittest

class SCPElNinocsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/elnino/elnino.csv')
        self.scp = scp.ScatterPlot2D(None)
        xA = [ x[6] for x in self.cursor ]
        yA = [ x[7] for x in self.cursor ]
        self.data = [xA, yA]
        self.scp.setData(self.data)

    def test_loadData(self):
        """ """
        with open('testSCPLoadData.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                xA = [ x[i % 12] for x in self.cursor ]
                self.cursor.rewind()
                yA = [ x[(i + 1) % 12] for x in self.cursor ]
                self.cursor.rewind()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_PearsCoeff(self):
        """ """
        with open('testSCPPearsCoeff.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_draw(self):
        """ """
        with open('testSCPDraw.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.DrawPoints()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SCPForest10csv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType10/forestcovertype10.csv')
        self.scp = scp.ScatterPlot2D(None)
        xA = [ x[6] for x in self.cursor ]
        yA = [ x[7] for x in self.cursor ]
        self.data = [xA, yA]
        self.scp.setData(self.data)

    def test_loadData(self):
        """ """
        with open('testSCPLoadDataForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                xA = [ x[i % 12] for x in self.cursor ]
                self.cursor.rewind()
                yA = [ x[(i + 1) % 12] for x in self.cursor ]
                self.cursor.rewind()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_PearsCoeff(self):
        """ """
        with open('testSCPPearsCoeffForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_draw(self):
        """ """
        with open('testSCPDrawForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SCPForestcsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType/forestcovertype.csv')
        self.scp = scp.ScatterPlot2D(None)
        xA = [ x[6] for x in self.cursor ]
        yA = [ x[7] for x in self.cursor ]
        self.data = [xA, yA]
        self.scp.setData(self.data)

    def test_loadData(self):
        """ """
        with open('testSCPLoadDataForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                xA = [ x[i % 12] for x in self.cursor ]
                self.cursor.rewind()
                yA = [ x[(i + 1) % 12] for x in self.cursor ]
                self.cursor.rewind()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_PearsCoeff(self):
        """ """
        with open('testSCPPearsCoeffForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_draw(self):
        """ """
        with open('testSCPDrawForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SCPElNinodb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="elnino_db")
        self.scp = scp.ScatterPlot2D(None)
        xA = [ x[6] for x in self.cursor ]
        yA = [ x[7] for x in self.cursor ]
        self.data = [xA, yA]
        self.scp.setData(self.data)

    def test_loadData(self):
        """ """
        with open('testSCPLoadDatadb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                xA = [ x[i % 12] for x in self.cursor ]
                self.cursor.rewind()
                yA = [ x[(i + 1) % 12] for x in self.cursor ]
                self.cursor.rewind()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_PearsCoeff(self):
        """ """
        with open('testSCPPearsCoeffdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_draw(self):
        """ """
        with open('testSCPDrawdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SCPForest10db(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcover10")
        self.scp = scp.ScatterPlot2D(None)
        xA = [ x[6] for x in self.cursor ]
        yA = [ x[7] for x in self.cursor ]
        self.data = [xA, yA]
        self.scp.setData(self.data)

    def test_loadData(self):
        """ """
        with open('testSCPLoadDataForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                xA = [ x[i % 12] for x in self.cursor ]
                self.cursor.rewind()
                yA = [ x[(i + 1) % 12] for x in self.cursor ]
                self.cursor.rewind()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_PearsCoeff(self):
        """ """
        with open('testSCPPearsCoeffForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_draw(self):
        """ """
        with open('testSCPDrawForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SCPForestdb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype")
        self.scp = scp.ScatterPlot2D(None)
        xA = [ x[6] for x in self.cursor ]
        yA = [ x[7] for x in self.cursor ]
        self.data = [xA, yA]
        self.scp.setData(self.data)

    def test_loadData(self):
        """ """
        with open('testSCPLoadDataForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                xA = [ x[i % 12] for x in self.cursor ]
                self.cursor.rewind()
                yA = [ x[(i + 1) % 12] for x in self.cursor ]
                self.cursor.rewind()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_PearsCoeff(self):
        """ """
        with open('testSCPPearsCoeffForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_draw(self):
        """ """
        with open('testSCPDrawForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.scp.computCorrCoef()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

def SCPElNinocsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SCPElNinocsv('test_loadData'))
    suite.addTest(SCPElNinocsv('test_PearsCoeff'))
    suite.addTest(SCPElNinocsv('test_draw'))

    return suite

def SCPForest10csv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SCPForest10csv('test_loadData'))
    suite.addTest(SCPForest10csv('test_PearsCoeff'))
    suite.addTest(SCPForest10csv('test_draw'))

    return suite

def SCPForestcsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SCPForestcsv('test_loadData'))
    suite.addTest(SCPForestcsv('test_PearsCoeff'))
    suite.addTest(SCPForestcsv('test_draw'))

    return suite

#----------------------------------------------------------------------------------------------------

def SCPElNinodb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SCPElNinodb('test_loadData'))
    suite.addTest(SCPElNinodb('test_PearsCoeff'))
    suite.addTest(SCPElNinodb('test_draw'))

    return suite

def SCPForest10db_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SCPForest10db('test_loadData'))
    suite.addTest(SCPForest10db('test_PearsCoeff'))
    suite.addTest(SCPForest10db('test_draw'))

    return suite

def SCPForestdb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SCPForestdb('test_loadData'))
    suite.addTest(SCPForestdb('test_PearsCoeff'))
    suite.addTest(SCPForestdb('test_draw'))

    return suite
