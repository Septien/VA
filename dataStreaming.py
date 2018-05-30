"""
For handling the strema of data. Supports two modes:
    -Work as a client.
    -Work as a server.
Working as client allows the program to connect to a server, which transmits data. Uses the TCP protoco.
Working as a server allows the programm to recieve incomming data from sensors or some other devices.
"""
# Multithreading
import threading
# Socket as client
import socket as skt
import time as t

class Streaming:
    """
    Handles the recieving of data. Has a varible for holding the socket for
    work as a client and a variable for work as a server.
        -connectType: Work as a server (0) or a client (1).
        -clientSock: Socket to work as a client.
        -servSock: Socket to work as a server.
        -nVar: Number of incoming variables.
    """
    def __init__(self, connectType):
        self.connectType = connectType
        self.clientSock = None
        self.servSock = None
        self.nVar = 0

    def connectToServer(self, address):
        """ 
        Connects to a server as specified by address.
            -address: Tuple containing the (host, port)
        """
        if self.connectType != 1:
            return
        # Create a socket using the AF_INET family and the TCP protocol
        self.clientSock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        # Connect
        self.clientSock.connect(address)
        # Wait 60 seconds for incoming transmissions
        self.clientSock.settimeout(2)

    def recvConnections(self, port):
        """
        Listen to incomming connections.
        """
        if self.connectType != 0:
            return
        # Create socket
        self.servSock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        # Bind connections
        self.servSock.bind(('', port))
        # Listen to only one connection
        self.servSock.listen(1)
        # Accept the connection
        self.clientSock, addr = self.servSock.accept()
        # Wait 60 seconds for incoming transmissions
        self.clientSock.settimeout(2)

    def recieve(self, nbytes = 1024, nTries = 10):
        """ Recieve incoming data """
        itry = 0
        while itry < nTries:
            try:
                Bytes = self.clientSock.recv(nbytes)
                if Bytes == b'':
                    raise RuntimeError("socket connection broken")
            except skt.timeout as e:
                itry += 1
            except RuntimeError as e:
                raise e
            else:
                break

        if itry == nTries:
            raise TypeError("No data recieved: Number of tries exceeded.")
        return Bytes

    def recvVariablesDescr(self):
        """
        Recive the following data of the variables:
            -Number of variables.
            -Name of each variable.
        """
        bytesR = []
        bytes_read = 0
        try:
            nBytes = self.recieve()
            numB = int(nBytes.decode())
            # numB = int.from_bytes(nBytes, byteorder='little')
        except Exception as e:
            raise e

        # Get the variables
        while bytes_read < numB:
            try:
                byteR = self.recieve(min(numB - bytes_read, 1024))
            except Exception as e:
                raise e
            else:
                bytesR.append(byteR)
                bytes_read = bytes_read + len(byteR)
                bytedata = b''.join(bytesR)
        # Convert from bytes to string
        strdata = bytedata.decode()
        # Get the name of the variables
        variables = strdata.split(',')
        numberVar = len(variables)

        return numberVar, variables

    def recvData(self):
        """ Receive the incoming data """
        bytesR = []
        bytes_read = 0
        try:
            nBytes = self.recieve()
            # Decode the number of bytes
            numB = int(nBytes.decode())
            # numB = int.from_bytes(nBytes, byteorder='little')
        except RuntimeError as e:
            raise e
        except TypeError as tE:
            # Number of tries exceded
            raise tE 

        # Get the variables
        while bytes_read < numB:
            bytedata = b''
            try:
                if self.connectType == 1:
                    t.sleep(0.5)
                byteR = self.recieve(min(numB - bytes_read, 1024))
            except RuntimeError as e:
                raise e
            except TypeError as tE:
                # Number of tries exceded
                raise tE
            else:
                bytesR.append(byteR)
                bytes_read = bytes_read + len(byteR)
                bytedata = b''.join(bytesR)

        # Convert from bytes to string
        strdata = bytedata.decode()
        # Get the data
        splitdata = strdata.split(',')
        data = [float(d) for d in splitdata]

        return data

    def close(self):
        """ Close all pertinent sockets """
        if self.clientSock:
            self.clientSock.shutdown(0)
            self.clientSock.close()
        if self.servSock:
            self.servSock.shutdown(0)
            self.servSock.close()

class StreamingThread(threading.Thread):
    """
    Handles the thread that recieve the incomming transmissions
        -queue: Queue for sharing the data.
        -name: Name of the thread.
        -threadID: Id of the thread
        -stream: Object for recieving the data.
        -qLock: Lock for accessing the queue.
        -exitQ: Queue indicating to exit the thread
    """
    def __init__(self, threadID, name, q, qLock, stream, exitQ, exitQL):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = q
        self.stream = stream
        self.qLock = qLock
        self.exitQ = exitQ
        self.exitQL = exitQL

    def run(self):
        """ To be able to run the thread """
        # Number of recieved rows
        numRecvData = 0
        while True:
            self.exitQL.acquire()
            if not self.exitQ.empty():
                r = self.exitQ.get()
                self.exitQ.put(1)
                # If q is not empty, finish thread
                self.exitQL.release()
                break
            self.exitQL.release()
            # Work
            data = []
            try:
                data = self.stream.recvData()
            except RuntimeError as runE:
                # When the connection to the socket is closed
                # Indicate to the main program and exit
                self.exitQL.acquire()
                self.exitQ.put(runE)
                self.exitQL.release()
                break
            except TypeError as tE:
                self.exitQL.acquire()
                # self.exitQ.put(tE)
                if not self.exitQ.empty():
                    # If main thread ask to finish, end thread
                    self.exitQL.release()
                    break
                self.exitQL.release()
                # Keep listening
                continue
            else:
                # Store data on the queue
                self.qLock.acquire()
                self.queue.put(data.copy())
                self.qLock.release()
