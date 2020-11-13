# Node:
# Author: MCG

# the node object represents the work done on each machine in the network.

import queue
import time
import types
import threading
import sys
import numpy as np
from client import *
from server import *
# Add the folders above
sys.path.append('../')
#import node_client.py

# The max number of devices in the network
MAX_DEVICES = 8

# Enumerate the message types
from enum import Enum
class Message(Enum):
    PREEMPT = 1
    RESTART = 2
    MATRICES = 3
    PING = 4

class Node:

    # Constructor
    def __init__(self):

        # Get the device's IP address.
        f = open("/opt/cec/ip.txt", "r")
        self._ipAddr = f.read().replace('\n','')
        
        # Get rid of the periods, cast to int
        #self._ipAddr = int(ipAddr.replace('.', ''))

        # Set a variable that will keep track of whether or not we have work to do
        self._matrixReady = False

        # Determine the node index based on the ip address.
        #if(self._ipAddr == 100097):
            #self._nodeID = 0; # desktop
        #if(self._ipAddr == 1000236):
            #self._nodeID = 1;
        #if(self._ipAddr == 1000219):
            #self._nodeID = 2;

        # This queue holds information that we need to send
        self._sendingQueue = queue.Queue(maxsize = 40)

        # Signal a preempt
        self._preempted = False;

        # Threads for sending and receiving information from the other nodes
        self._sendingThread = threading.Thread(target=self.sendingLoop, daemon=False)
        self._sendingThread.start()
        self._receivingThread = threading.Thread(target=self.receivingLoop, daemon=False)
        self._receivingThread.start()

        # Thread for doing the matrix multiplication work
        self._multThread = threading.Thread(target=self.multLoop, daemon=True)
        self._multThread.start()

        # The _partitions object keeps track of the partitions of the matrix.
        # Each element in the array corresponds to the index the partition ends on
        self._partitions = []

    def sendingLoop(self):
        while(not self._preempted):
            # if there is something to be sent, then send it
            if(not self._sendingQueue.empty()):
                print("Sending...")
                tup = self._sendingQueue.get()
                client(tup[0],tup[1], "10.0.0.97")
            time.sleep(1)

    # These are the types of messages that could be sent and need to be handled:
        # Preempt
        # Restart
        # Matrices
        # ping
        # shut down?
    def receivingLoop(self):
        # this thread stays alive the whole time, even if preempted. 
        while(True):
            item = server(str(self._ipAddr))
            if(item.messageType == PING):
                # Send a response to the master node
                print("Received a ping from master. Sending pong...")
                self._sendingQueue.put(types.SimpleNamespace(messageType = PING))
            elif(item.messageType == PREEMPT):
                print("Received a preempt from master. Calling preempt..")
                self._preempt()
            elif(item.messageType == RESTART):
                print("Received a restart command from master. Calling restart...")
                self._restart()
            elif(item.messageType == MATRICES):
                print("Received matrix message.")

                print("Updating based on recieved information...")

                # For now, just assume that the first column is the x array and the rest is the matrix
                print("Shape of received item:")
                print(np.array(item).shape)
                print("Item:")
                print(item)
                self._x = item[:,0]
                self._matrix = item[:,1:]
                self._matrixReady = True
            else:
                print("WARNING: Received an unknown command from master node.")

    def multLoop(self):
        while(not self._preempted):
            
            # Wait until there is a matrix to be multiplied.
            if(self._matrixReady):

                # Compute the matrix multiplication, then add it to the sending queue
                self._sendingQueue.put(types.SimpleNamespace(messageType = MATRICES, data = np.matmul(self._x,self._matrix)))
                print("Matrix multiplication complete.")
                self._matrixReady = False
            else:
                time.sleep(1)

    # This script will take a matrix and divide it into n parts.
    # It will make the parts as evenly sized as possible while still maintaining the rows and columns.
    def matrixSplit(self, n):

        diff = 0
        fraction = len(self._matrix)/n
        self._partitions = []
        for i in range(0,n):
            split  = round(fraction + diff)
            self._partitions.append(split)
            diff = diff + fraction - split

        part = np.zeros(n)
        for i in range(0,n):
            part[i] = np.sum(self._partitions[:i+1])

        self._partitions = np.array(part, dtype=np.uint)
        newMatrix = np.array([], dtype=object)
        for i in range(0,len(self._partitions)):
            if(i==0):
                #print("index: " +str(self._partitions[i]))
                #print("sub matrix: " +str(self._matrix[:self._partitions[i]]))
                np.append(newMatrix, self._matrix[:self._partitions[i]])
            else:
                #print("index: " +str(self._partitions[i]))
                #print("sub matrix: " +str(self._matrix[self._partitions[i-1]:self._partitions[i]]))
                np.append(newMatrix, self._matrix[self._partitions[i-1]:self._partitions[i]])

        print("newmatrix:")
        print(newMatrix)

    def addMatrix(self, matrix):
        self._matrix = matrix


    # Matrix is the original data, partitioned into l partitions
    # where l is the recovery threshold, ie minimum number of machines
    # n is the number of machines to send to
    def distributeData(self,matrix,n):

        l = len(matrix)

        # generate a full rank matrix
        # l should always be less than or equal to n
        A = generateMatrixOfRank(l,n,l) 

        # For each machine in the system, send them their data, which is (matrix*dist_mat)[i] 
        # where i is the index of the machine
        
        result = np.matmul(matrix, dist_mat)
        for i in range(0, MAX_DEVICES):
            # send to device i result[i]
            i;

    # This function isn't being used right now, but it may be in use for milestone 2
    def generateMatrixOfRank(self,rows,columns,r):
        assert rows >= r and columns >= r

        # this is a python do while
        while(True):

            A = np.random.rand(rows,columns)
            if(np.linalg.matrix_rank(A) == r):
                break

        return A

    # Preempt this node
    def preempt(self):
        self._preempted = True
        print("Node preempted. Stopping sending and multiplying...")

    # Restart this node after preemption
    def restart(self):
        self._preempted = False

        print("Node restarted. Beginning sending and multiplying...")

        # Restart the stopped threads
        self._sendingThread = threading.Thread(target=self.sendingLoop, daemon=False)
        self._sendingThread.start()
        self._multThread = threading.Thread(target=self.multLoop, daemon=True)
        self._multThread.start()



if (__name__ == "__main__"):
    node = Node()
    node.addMatrix(np.random.rand(20,20))
    node.matrixSplit(100)

