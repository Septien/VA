"""
Module for measuring the performance of the pieplot.
"""

import dataIterator as dI
import wx
import pieplot as pp
import time as t
import unittest

class PPElNinocsv(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('/media/phantom/B/Tesis/Data/elnino/elnino.csv')#'../../../Data/elnino/elnino.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.pp = pp.PiePlot(None)
        self.pp.setData(self.cursor)
        self.pp.setAxis(6)
        self.pp.setLabels(a)

    def test_computeFreq(self):
        """ """
        with open('testPPFreqElNino.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_pie(self):
        """ """
        self.pp.computeFrequencies(False)
        with open('testPPpieElNino.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.DrawPie()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PPForest10csv(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('/media/phantom/B/Tesis/Data/ForestCoverType10/forestcovertype.csv')#'../../../Data/ForestCoverType10/forestcovertype10.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.pp = pp.PiePlot(None)
        self.pp.setData(self.cursor)
        self.pp.setAxis(6)
        self.pp.setLabels(a)

    def test_computeFreq(self):
        """ """
        with open('testPPFreqForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_pie(self):
        """ """
        self.pp.computeFrequencies(False)
        with open('testPPpieForest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.DrawPie()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PPForestcsv(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('/media/phantom/B/Tesis/Data/ForestCoverType/forestcovertype.csv')#'../../../Data/ForestCoverType/forestcovertype.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.pp = pp.PiePlot(None)
        self.pp.setData(self.cursor)
        self.pp.setAxis(6)
        self.pp.setLabels(a)

    def test_computeFreq(self):
        """ """
        with open('testPPFreqForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_pie(self):
        """ """
        self.pp.computeFrequencies(False)
        with open('testPPForest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.DrawPie()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PPElNinodb(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="elnino_db")
        a, b, c, d = self.cursor.getDBDescription()
        self.pp = pp.PiePlot(None)
        self.pp.setData(self.cursor)
        self.pp.setAxis(6)
        self.pp.setLabels(a)

    def test_computeFreq(self):
        """ """
        with open('testPPFreqElNinodb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_pie(self):
        """ """
        self.pp.computeFrequencies(False)
        with open('testPPpElNinodb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.DrawPie()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PPForest10db(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype10")
        a, b, c, d = self.cursor.getDBDescription()
        self.pp = pp.PiePlot(None)
        self.pp.setData(self.cursor)
        self.pp.setAxis(6)
        self.pp.setLabels(a)

    def test_computeFreq(self):
        """ """
        with open('testPPFreqForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_pie(self):
        """ """
        self.pp.computeFrequencies(False)
        with open('testPPForest10db.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.DrawPie()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class PPForestdb(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype")
        a, b, c, d = self.cursor.getDBDescription()
        self.pp = pp.PiePlot(None)
        self.pp.setData(self.cursor)
        self.pp.setAxis(6)
        self.pp.setLabels(a)

    def test_computeFreq(self):
        """ """
        with open('testPPFreqForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.computeFrequencies(False)
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def test_pie(self):
        """ """
        self.pp.computeFrequencies(False)
        with open('testPPForestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.pp.DrawPie()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()


#----------------------------------------------------------------------------------------------------

def PPElNinocsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PPElNinocsv('test_computeFreq'))
    suite.addTest(PPElNinocsv('test_pie'))

    return suite

def PPForest10csv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PPForest10csv('test_computeFreq'))
    suite.addTest(PPForest10csv('test_pie'))

    return suite

def PPForestcsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PPForestcsv('test_computeFreq'))
    suite.addTest(PPForestcsv('test_pie'))

    return suite

#----------------------------------------------------------------------------------------------------

def PPElNinodb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PPElNinodb('test_computeFreq'))
    suite.addTest(PPElNinodb('test_pie'))

    return suite

def PPForest10db_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PPForest10db('test_computeFreq'))
    suite.addTest(PPForest10db('test_pie'))

    return suite

def PPForestdb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(PPForestdb('test_computeFreq'))
    suite.addTest(PPForestdb('test_pie'))

    return suite
