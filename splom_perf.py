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
        self.cursor.loadCSV('/Users/Septien/Documents/Tesis/Data/elnino/elnino.csv')#'/media/phantom/B/Tesis/Data/elnino/elnino.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.splom = splom.SPLOM(None)
        self.splom.SetData(self.cursor)
        self.splom.SetLabels(a)
        self.splom.SetCategory(b)

    def test_draw(self):
        """ """
        with open('testsplomdrawelnino.txt', 'a') as file:
            for i in range(30):
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
        self.cursor.loadCSV('/Users/Septien/Documents/Tesis/Data/ForestCoverType10/forestcovertype.csv')#'/media/phantom/B/Tesis/Data/ForestCoverType10/forestcovertype.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.splom = splom.SPLOM(None)
        self.splom.SetData(self.cursor)
        self.splom.SetLabels(a)
        self.splom.SetCategory(b)

    def test_draw(self):
        """ """
        with open('testsplomdrawforest10.txt', 'a') as file:
            for i in range(30):
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
        self.cursor.loadCSV('/Users/Septien/Documents/Tesis/Data/ForestCoverType/forestcovertype.csv')#'/media/phantom/B/Tesis/Data/ForestCoverType/forestcovertype.csv')
        a, b, c, d = self.cursor.getDBDescription()
        self.splom = splom.SPLOM(None)
        self.splom.SetData(self.cursor)
        self.splom.SetLabels(a)
        self.splom.SetCategory(b)

    def test_draw(self):
        """ """
        with open('testsplomdrawforest.txt', 'a') as file:
            for i in range(30):
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
        a, b, c, d = self.cursor.getDBDescription()
        self.splom = splom.SPLOM(None)
        self.splom.SetData(self.cursor)
        self.splom.SetLabels(a)
        self.splom.SetCategory(b)

    def test_draw(self):
        """ """
        with open('testsplomdrawelninodb.txt', 'a') as file:
            for i in range(30):
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
        a, b, c, d = self.cursor.getDBDescription()
        self.splom = splom.SPLOM(None)
        self.splom.SetData(self.cursor)
        self.splom.SetLabels(a)
        self.splom.SetCategory(b)

    def test_draw(self):
        """ """
        with open('testsplomdrawforest10.txt', 'a') as file:
            for i in range(30):
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
        a, b, c, d = self.cursor.getDBDescription()
        self.splom = splom.SPLOM(None)
        self.splom.SetData(self.cursor)
        self.splom.SetLabels(a)
        self.splom.SetCategory(b)

    def test_draw(self):
        """ """
        with open('testsplomdrawforestdb.txt', 'a') as file:
            for i in range(30):
                start = t.time()
                self.splom.DrawSCPM()
                end = t.time()
                exTime = '{:f}\n'.format(end - start)
                file.write(exTime)

    def tearDown(self):
        """ """
        self.cursor.close()

#----------------------------------------------------------------------------------------------------

def SPLOMElNinocsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMElNinocsv('test_draw'))

    return suite

def SPLOMForest10csv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForest10csv('test_draw'))

    return suite

def SPLOMForestcsv_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForestcsv('test_draw'))

    return suite

#----------------------------------------------------------------------------------------------------

def SPLOMElNinodb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMElNinodb('test_draw'))

    return suite

def SPLOMForest10db_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForest10db('test_draw'))

    return suite

def SPLOMForestdb_suite():
    """ """
    suite = unittest.TestSuite()
    suite.addTest(SPLOMForestdb('test_draw'))

    return suite
