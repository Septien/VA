"""
A module that implements an iterator for retrieving data from either a database or
a .cvs file (posible a stream). The iterator abstracts the need for a generator 
for each kind of data source, and handles all differences.
"""

import pymysql.cursors

class Data(object):
    """
    Class for retrieving the data. Handles the differences between a database and an csv file.
    """
    def __init__(self, flag):
        """ Constructor of the class.
            -flag: Indicates if a database or an csv is to be loaded (0 -> database, 1 -> csv).
        """
        self.sourceFlag = flag
        self.dbCursor = None
        self.dbConnection = None
        self.File = None
        self.data = None
        self.name = None
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
        if self.sourceFlag == 0:
            # If the source is a database
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

        elif self.sourceFlag == 1:
            # If the source is a csv.
            # Get the variables name of the csv
            line = self.File.readline()
            row = line.split(',')
            labels = row.copy()
            # Get the types
            line = self.File.readline()
            row = line.split(',')
            for r in row:
                category.append(int(r))
        
        self.length = len(labels)
        assert len(labels) == len(category), "Incorrect number of labels and category"
        assert len(category) == self.length, "Incorrect number of categories"
        return labels, category

    def length(self):
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
            notNoisy = True
            while notNoisy:
                line = self.File.readline()
                if line == "":
                    raise StopIteration()
            
                row = line.split(',')
                for r in row:
                    if r != '?':
                        data.append(float(r))
                    else:
                        # Incomplete data, dismiss row
                        data.clear()
                        continue
                break

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
            # Read the first two lines
            line = self.File.readline()
            line = self.File.readline()

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