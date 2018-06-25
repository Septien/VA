"""
A module that implements an iterator for retrieving data from either a database or
a .cvs file (posible a stream). The iterator abstracts the need for a generator 
for each kind of data source, and handles all differences.
"""
import wx
import pymysql.cursors
import threading
import queue
import time as t
# For the streaming
import dataStreaming as dS

class Data(object):
    """
    Class for retrieving the data. Handles the differences between a database and an csv file.
    """
    def __init__(self, flag):
        """ Constructor of the class.
            -flag: Indicates if a database or an csv is to be loaded (0 -> database, 1 -> csv, 2 -> stream).
        """
        self.sourceFlag = flag
        self.dbCursor = None
        self.dbConnection = None
        self.File = None
        self.descrFile = None
        self.data = None
        self.name = None
        # For the streaming
        self.stream = None
        self.exitQ = None
        self.exitQLock = None
        self.workQueue = None
        self.workQLock = None
        self.numVar = None
        self.connectionClosed = False
        self.variables = None
        self.thread = None

        self.length = 0

    def loadDB(self, host="", user="", passwd="", dbName=""):
        """
        Connects to a mysql server.
            -user: A valid user for connecting to the database.
            -passwd: Password.
            -dbName: Database to connect.
        """
        # If a database is not selected, return
        if self.sourceFlag != 0:
            return
        # Connect
        try:
            self.dbConnection = pymysql.connect(host=host, user=user, password=passwd, db=dbName, 
                                            charset='utf8mb4', cursorclass=pymysql.cursors.SSCursor)
            # Get the cursor
            self.dbCursor = self.dbConnection.cursor()
        except:
            return False

        return True

    def loadCSV(self, filename):
        """
        Loads a cvs file.
            -filename: The path to the file.
        """
        if self.sourceFlag != 1:
            return
        self.name = filename
        # Open
        self.File = open(self.name, 'r')
        # Get the description file
        descrfilename = self.name.split('.csv')[0] + '_descr.csv'
        try:
            self.descrFile = open(descrfilename, 'r')
        except:
            return False
        else:
            return True

    def connectToStream(self, address, ctype):
        """ 
        Connects to a stream.
            -address: (host, port) to connect to/from
            -type: If the object will work as server or client
        """
        # For communicating between processes
        self.workQueue = queue.Queue(1000)
        self.exitQ = queue.Queue(1)
        self.workQLock = threading.Lock()
        self.exitQLock = threading.Lock()
        self.stream = dS.Streaming(ctype)

        # connect
        if ctype == 0:
            # As server
            self.stream.recvConnections(address[1])
        elif ctype == 1:
            # As client
            self.stream.connectToServer(address)

        # Get description
        self.numVar, self.variables = self.stream.recvVariablesDescr()
        # Create listening thread
        self.thread = dS.StreamingThread(1, "Thread1", self.workQueue, self.workQLock, 
            self.stream, self.exitQ, self.exitQLock)
        self.thread.start()

    def getDBDescription(self):
        """ Returns the description of the database:
            -The types of the variables.
            -The name of the variables.
        """
        def isNumeric(dataType):
            """ Returns true if the type of the datum is numeric """
            types = ['float', 'real', 'double precision', 'int', 'integer', 'smallint', 'decimal', 'numeric',
                    'dec', 'fixed']
            numeric = 1
            for t in types:
                if dataType == t:
                    numeric = 0
            return numeric
        #
        labels = []
        category = []
        description = []
        units = []

        # If the source is a database
        if self.sourceFlag == 0:
            if not self.dbCursor:
                return

            sqlcmd = "SHOW TABLES"
            self.dbCursor.execute(sqlcmd)
            # Get the first table
            table = self.dbCursor.fetchone()
            self.name = table[0]
            # Get the description of the table
            sqlcmd = "DESCRIBE " + self.name
            self.dbCursor.execute(sqlcmd)
            descr = self.dbCursor.fetchall_unbuffered()

            # Get the description of each variable
            for variable in descr:
                # Name
                labels.append(variable[0])
                # Type
                category.append(isNumeric(variable[1]))

            # Get the description of the variables, from the descr table
            sqlcmd = "SELECT * FROM descr"
            self.dbCursor.execute(sqlcmd)
            table = self.dbCursor.fetchall_unbuffered()
            # Get the units of the numerical variables
            line = next(table)
            i = 0
            row = []
            for r in line:
                if category[i] == 0:
                    units.append(r)
                    row.append('')
                else:
                    units.append('')
                    row.append(r)
                i += 1
            description.append(row)
            for line in table:
                row = []
                for r in line:
                    row.append(r)
                description.append(row.copy())

        # If the source is a csv.
        elif self.sourceFlag == 1:
            # Get the variables name from the description file
            line = self.descrFile.readline()
            row = line.split(',')
            labels = row.copy()
            # Get the types
            line = self.descrFile.readline()
            row = line.split(',')
            for r in row:
                category.append(int(r))
            # Get the units of each numeric variable
            line = self.descrFile.readline()
            row = line.split(',')
            for i in range(len(row)):
                if category[i] == 0:
                    units.append(row[i])
                    row[i] = ''
                else:
                    units.append('')
            description.append(row)
            # Get the description of each of the values for the categorical variabless
            for row in self.descrFile:
                r = row.split(',')
                description.append(r)
        
        # If the source is a stream
        elif self.sourceFlag == 2:
            labels = self.variables
            self.length = self.numVar
            for i in range(self.numVar):
                category.append(0)
        
        self.length = len(labels)
        assert len(labels) == len(category), "Incorrect number of labels and category"
        assert len(category) == self.length, "Incorrect number of categories"
        return labels, category, description, units

    def dataLength(self):
        """ Returns the number of axes in the database """
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        """ support for the next() function """
        return self.next()
    
    def next(self):
        """ Returns the next data """
        data = None
        if self.sourceFlag == 0:
            # For a db
            if not self.data:
                sqlcmd = "SELECT * FROM " + self.name
                self.dbCursor.execute(sqlcmd)
                self.data = self.dbCursor.fetchall_unbuffered()
            try:
                data = []
                ndata = next(self.data)
                for d in ndata:
                    data.append(float(d))
            except StopIteration as e:
                raise e

        elif self.sourceFlag == 1:
            data = []
            noisy = False
            while True:
                noisy = False
                line = self.File.readline()
                if line == "":
                    raise StopIteration()
            
                row = line.split(',')
                for r in row:
                    try:
                        float(r)
                    except ValueError:
                        # Incomplete data, dismiss row
                        data.clear()
                        noisy = True
                        break
                    else:
                        data.append(float(r))
                # Read next row
                if not noisy:
                    break
        
        elif self.sourceFlag == 2:
            data = []
            i = 0
            if self.connectionClosed:
                raise TypeError("Connection closed")
            while i < 10:
                if self.exitQLock.acquire(blocking=False):
                    # Check if there are some errors:
                    if not self.exitQ.empty() and not self.connectionClosed:
                        r = self.exitQ.get()
                        style = wx.OK | wx.CENTER | wx.ICON_INFORMATION
                        result = wx.MessageBox("Connection with client closed", "Connection closed", style)
                        self.exitQLock.release()
                        self.connectionClosed = True
                        raise StopIteration()
                self.exitQLock.release()
                if not self.workQLock.acquire(blocking=False):
                    i += 1
                    continue
                if self.workQueue.empty():
                    i += 1
                    self.workQLock.release()
                    continue
                else:
                    data = self.workQueue.get()
                    self.workQLock.release()
                    break
                if self.connectionClosed:
                    raise StopIteration()
                # self.workQLock.release()
            if data == []:
                raise StopIteration()

        return data

    def rewind(self):
        """ Return to the first data """
        if self.sourceFlag == 0:
            self.dbCursor.close()
            self.dbCursor = self.dbConnection.cursor()
            sqlcmd = "SELECT * FROM " + self.name
            self.dbCursor.execute(sqlcmd)
            self.data = self.dbCursor.fetchall_unbuffered()

        if self.sourceFlag == 1:
            self.File.close()
            self.File = open(self.name, 'r')

        if self.sourceFlag == 2:
            # Stream in use, no possible to rewind
            return

    def copy(self):
        """ Returns a copy of the iterator """
        newIter = Data(self.sourceFlag)
        newIter.name = self.name
        
        if self.sourceFlag == 0:
            newIter.dbConnection = self.dbConnection
            newIter.dbCursor = newIter.dbConnection.cursor()
        
        if self.sourceFlag == 1:
            newIter.File = open(self.name, 'r')
            line = newIter.File.readline()
            line = newIter.File.readline()

        return newIter

    def close(self):
        """ Close the appropiate variables """
        if self.File:
            self.File.close()
        if self.dbConnection and self.dbCursor:
            self.dbCursor.close()
            self.dbConnection.close()
        if self.stream and self.thread:
            self.exitQLock.acquire(blocking=False)
            self.exitQ.put(1)
            self.exitQLock.release()
            # Wait to thread to finish
            t.sleep(1)
            self.stream.close()
