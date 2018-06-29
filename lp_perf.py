"""
Module for measuring the computing time if the lineplot.
"""

import dataIterator as dI
import wx
import lineplot as lp
import time as t
import unittest

class LPElNinocsv(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/elnino/elnino.csv')
        self.lp = lp.LinePLot(None)
        # compute on 6th axis
        self.data = [d[6] for d in self.cursor]
        self.cursor.rewind()

    def test_loadData(self):
        """ """
        with open('testLPLoaddata.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_computeFreq(self):
        """ """
        with open('testLPcomputeFreq.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.setData(self.data)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_newLine(self):
        """ """
        self.lp.setData(self.data)
        data = [d[5] for d in self.cursor]
        self.cursor.rewind()
        with open('testLPNewLine.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.addNewLine(data)
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()


#----------------------------------------------------------------------------------------------------

class LPForest10csv(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType10/forestcovertype10.csv')
        self.lp = lp.LinePLot(None)
        # compute on 6th axis
        self.data = [d[6] for d in self.cursor]
        self.cursor.rewind()

    def test_loadData(self):
        """ """
        with open('testLPLoaddataForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_computeFreq(self):
        """ """
        with open('testLPcomputeFreqForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.setData(self.data)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_newLine(self):
        """ """
        self.lp.setData(self.data)
        data = [d[5] for d in self.cursor]
        self.cursor.rewind()
        with open('testLPNewLineForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.addNewLine(data)
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class LPForestcsv(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType/forestcovertype.csv')
        self.lp = lp.LinePLot(None)
        # compute on 6th axis
        self.data = [d[6] for d in self.cursor]
        self.cursor.rewind()

    def test_loadData(self):
        """ """
        with open('testLPLoaddataForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_computeFreq(self):
        """ """
        with open('testLPcomputeFreqForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.setData(self.data)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_newLine(self):
        """ """
        self.lp.setData(self.data)
        data = [d[5] for d in self.cursor]
        self.cursor.rewind()
        with open('testLPNewLineForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.addNewLine(data)
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()


#----------------------------------------------------------------------------------------------------

class LPElNinodb(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="elnino_db")
        self.lp = lp.LinePLot(None)
        # compute on 6th axis
        self.data = [d[6] for d in self.cursor]
        self.cursor.rewind()

    def test_loadData(self):
        """ """
        with open('testLPLoaddatadb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_computeFreq(self):
        """ """
        with open('testLPcomputeFreqdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.setData(self.data)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_newLine(self):
        """ """
        self.lp.setData(self.data)
        data = [d[5] for d in self.cursor]
        self.cursor.rewind()
        with open('testLPNewLinedb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.addNewLine(data)
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()


#----------------------------------------------------------------------------------------------------

class LPForest10db(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype10")
        self.lp = lp.LinePLot(None)
        # compute on 6th axis
        self.data = [d[6] for d in self.cursor]
        self.cursor.rewind()

    def test_loadData(self):
        """ """
        with open('testLPLoaddataForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_computeFreq(self):
        """ """
        with open('testLPcomputeFreqForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.setData(self.data)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_newLine(self):
        """ """
        self.lp.setData(self.data)
        data = [d[5] for d in self.cursor]
        self.cursor.rewind()
        with open('testLPNewLineForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.addNewLine(data)
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class LPForestdb(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype")
        self.lp = lp.LinePLot(None)
        # compute on 6th axis
        self.data = [d[6] for d in self.cursor]
        self.cursor.rewind()

    def test_loadData(self):
        """ """
        with open('testLPLoaddataForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_computeFreq(self):
        """ """
        with open('testLPcomputeFreqForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.setData(self.data)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_newLine(self):
        """ """
        self.lp.setData(self.data)
        data = [d[5] for d in self.cursor]
        self.cursor.rewind()
        with open('testLPNewLineForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.lp.addNewLine(data)
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()


#----------------------------------------------------------------------------------------------------

def LPElNinocsvsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(LPElNinocsv('test_loadData'))
    suite.addTest(LPElNinocsv('test_computeFreq'))
    suite.addTest(LPElNinocsv('test_newLine'))

    return suite

def LPForest10csvsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(LPForest10csv('test_loadData'))
    suite.addTest(LPForest10csv('test_computeFreq'))
    suite.addTest(LPForest10csv('test_newLine'))

    return suite

def LPForestcsvsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(LPForestcsv('test_loadData'))
    suite.addTest(LPForestcsv('test_computeFreq'))
    suite.addTest(LPForestcsv('test_newLine'))

    return suite

#----------------------------------------------------------------------------------------------------

def LPElNinodbsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(LPElNinodb('test_loadData'))
    suite.addTest(LPElNinodb('test_computeFreq'))
    suite.addTest(LPElNinodb('test_newLine'))

    return suite

def LPForest10dbsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(LPForest10db('test_loadData'))
    suite.addTest(LPForest10db('test_computeFreq'))
    suite.addTest(LPForest10db('test_newLine'))

    return suite

def LPForestdbsuite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(LPForestdb('test_loadData'))
    suite.addTest(LPForestdb('test_computeFreq'))
    suite.addTest(LPForestdb('test_newLine'))

    return suite
