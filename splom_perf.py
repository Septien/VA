"""
Module for measuring the performance of the splom.
"""

import dataIterator as dI
import wx
import splom
import time as t
import unittest

class SPLOMElNinocsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/elnino/elnino.csv')
        self.splom = splom.SPLOM(None)
        self.splom.setData(self.cursor)

    def test_draw(self):
        """ """
        with open('testsplomdrawelnino.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SPLOMForest10csv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType10/forestcovertype10.csv')
        self.splom = splom.SPLOM(None)
        self.splom.setData(self.cursor)

    def test_draw(self):
        """ """
        with open('testsplomdrawforest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SPLOMForestcsv(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(1)
        self.cursor.loadCSV('../../../Data/ForestCoverType/forestcovertype.csv')
        self.splom = splom.SPLOM(None)
        self.splom.setData(self.cursor)

    def test_draw(self):
        """ """
        with open('testsplomdrawforest.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SPLOMElNinodb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="elnino_db")
        self.splom = splom.SPLOM(None)
        self.splom.setData(self.cursor)

    def test_draw(self):
        """ """
        with open('testsplomdrawelninodb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SPLOMForest10db(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype10")
        self.splom = splom.SPLOM(None)
        self.splom.setData(self.cursor)

    def test_draw(self):
        """ """
        with open('testsplomdrawforest10.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

class SPLOMForestdb(unittest.TestCase):
    """ """
    def setUp(self):
        self.cursor = dI.Data(0)
        self.cursor.loadDB(host="localhost", user="root", passwd="12345", dbName="forestcovertype")
        self.splom = splom.SPLOM(None)
        self.splom.setData(self.cursor)

    def test_draw(self):
        """ """
        with open('testsplomdrawforestdb.txt', 'a') as file:
            for i in range(1):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

def SPLOMELNinocsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMElNinocsv('test_loadData'))
    suite.addTest(SPLOMElNinocsv('test_PearsCoeff'))
    suite.addTest(SPLOMElNinocsv('test_draw'))

    return suite

def SPLOMForest10csv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForest10csv('test_loadData'))
    suite.addTest(SPLOMForest10csv('test_PearsCoeff'))
    suite.addTest(SPLOMForest10csv('test_draw'))

    return suite

def SPLOMForestcsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForestcsv('test_loadData'))
    suite.addTest(SPLOMForestcsv('test_PearsCoeff'))
    suite.addTest(SPLOMForestcsv('test_draw'))

    return suite

#----------------------------------------------------------------------------------------------------

def SPLOMELNinodb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMElNinodb('test_loadData'))
    suite.addTest(SPLOMElNinodb('test_PearsCoeff'))
    suite.addTest(SPLOMElNinodb('test_draw'))

    return suite

def SPLOMForest10db_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForest10db('test_loadData'))
    suite.addTest(SPLOMForest10db('test_PearsCoeff'))
    suite.addTest(SPLOMForest10db('test_draw'))

    return suite

def SPLOMForestdb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForestdb('test_loadData'))
    suite.addTest(SPLOMForestdb('test_PearsCoeff'))
    suite.addTest(SPLOMForestdb('test_draw'))

    return suite
