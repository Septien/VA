"""
Module for measuring the performance of the histogram.
"""

import dataIterator as dI
import wx
import histogramplot as h
import time as t
import unittest

class HElNinocsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('/Users/Septien/Documents/Tesis/Data/elnino/elnino.csv')#'/media/phantom/B/Tesis/Data/elnino/elnino.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.hist = h.HistogramPlot(None)
        self.data = [d[6] for d in self.cursor]
        self.hist.setData(self.data)
        self.hist.SetNumBins(20)
        self.hist.computeClassesInterval()
        self.cursor.rewind()

    def test_dataloadTime(self):
        """ """
        with open('testHLoaddata.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_freqComputation(self):
        """ """
        with open('testHFreComp.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.hist.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class HForest10csv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('/Users/Septien/Documents/Tesis/Data/ForestCoverType10/forestcovertype.csv')#'/media/phantom/B/Tesis/Data/ForestCoverType10/forestcovertype.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.hist = h.HistogramPlot(None)
        self.data = [d[6] for d in self.cursor]
        self.hist.setData(self.data)
        self.hist.SetNumBins(20)
        self.hist.computeClassesInterval()
        self.cursor.rewind()

    def test_dataloadTime(self):
        """ """
        with open('testHLoaddataForest10.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                data = [d[i % 10] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_freqComputation(self):
        """ """
        with open('testHFreCompForest10.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.hist.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class HForestcsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('/Users/Septien/Documents/Tesis/Data/ForestCoverType/forestcovertype.csv')#'/media/phantom/B/Tesis/Data/ForestCoverType/forestcovertype.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.hist = h.HistogramPlot(None)
        self.data = [d[6] for d in self.cursor]
        self.hist.setData(self.data)
        self.hist.SetNumBins(20)
        self.hist.computeClassesInterval()
        self.cursor.rewind()

    def test_dataloadTime(self):
        """ """
        with open('testHLoaddataForest.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_freqComputation(self):
        """ """
        with open('testHFreCompForest.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.hist.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class HElNinodb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="elnino_db")
        a, b, c, d = self.cursor.getDBDescription()
        self.hist = h.HistogramPlot(None)
        self.data = [d[6] for d in self.cursor]
        self.hist.setData(self.data)
        self.hist.SetNumBins(20)
        self.hist.computeClassesInterval()
        self.cursor.rewind()

    def test_dataloadTime(self):
        """ """
        with open('testHLoaddatadb.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_freqComputation(self):
        """ """
        with open('testHFreCompdb.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.hist.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class HForest10db(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype10")
        a, b, c, d = self.cursor.getDBDescription()
        self.hist = h.HistogramPlot(None)
        self.data = [d[6] for d in self.cursor]
        self.hist.setData(self.data)
        self.hist.SetNumBins(20)
        self.hist.computeClassesInterval()
        self.cursor.rewind()

    def test_dataloadTime(self):
        """ """
        with open('testHLoaddataForest10db.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                data = [d[i % 10] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_freqComputation(self):
        """ """
        with open('testHFreCompForest10db.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.hist.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class HForestdb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype")
        a, b, c, d = self.cursor.getDBDescription()
        self.hist = h.HistogramPlot(None)
        self.data = [d[6] for d in self.cursor]
        self.hist.setData(self.data)
        self.hist.SetNumBins(20)
        self.hist.computeClassesInterval()
        self.cursor.rewind()

    def test_dataloadTime(self):
        """ """
        with open('testHLoaddataForestdb.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                data = [d[i % 12] for d in self.cursor]
                end = t.time()
                self.cursor.rewind()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_freqComputation(self):
        """ """
        with open('testHFreCompForestdb.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.hist.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

def HElNinocsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(HElNinocsv('test_dataloadTime'))
    suite.addTest(HElNinocsv('test_freqComputation'))

    return suite

def HForest10csv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(HForest10csv('test_dataloadTime'))
    suite.addTest(HForest10csv('test_freqComputation'))

    return suite

def HForestcsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(HForestcsv('test_dataloadTime'))
    suite.addTest(HForestcsv('test_freqComputation'))

    return suite

#----------------------------------------------------------------------------------------------------

def HElNinodb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(HElNinodb('test_dataloadTime'))
    suite.addTest(HElNinodb('test_freqComputation'))

    return suite

def HForest10db_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(HForest10db('test_dataloadTime'))
    suite.addTest(HForest10db('test_freqComputation'))

    return suite

def HForestdb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(HForestdb('test_dataloadTime'))
    suite.addTest(HForestdb('test_freqComputation'))

    return suite
