# Node:
# Author: MCG

# the node object represents the work done on each machine in the network.

import queue
import time
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

class Node:

    # Constructor
    def __init__(self):

        # Get the device's IP address.
        f = open("/opt/cec/ip.txt", "r")
        ipAddr = f.read()
        
        # Get rid of the periods, cast to int
        self._ipAddr = int(ipAddr.replace('.', ''))

        # Set a variable that will keep track of whether or not we have work to do
        self._matrixReady = False

        # Determine the node index based on the ip address.
        if(self._ipAddr == 100097):
            self._nodeID = 0; # desktop
        if(self._ipAddr == 1000236):
            self._nodeID = 1;
        if(self._ipAddr == 1000219):
            self._nodeID = 2;

        # This queue holds information that we need to send
        self._sendingQueue = queue.Queue(maxsize = 40)
        self._sendingQueue.put(("first message to be sent","fn"))
        self._sendingQueue.put(("second message to be sent","fn"))

        # Threads for sending and receiving information from the other nodes
        #self._sendingThread = threading.Thread(target=self.sendingLoop, daemon=True)
        #self._sendingThread.start()
        #self._receivingThread = threading.Thread(target=self.receivingLoop, daemon=True)
        #self._receivingThread.start()
        #print("the main thread continues")

        # Thread for doing the matrix multiplication work
        self._multThread = threading.Thread(target=self.multLoop, daemon=True)
        self._multThread.start()

        # The _partitions object keeps track of the partitions of the matrix.
        # Each element in the array corresponds to the size of the partition
        self._partitions = []

    def sendingLoop(self):
        while(True):
            # if there is something to be sent, then send it
            if(not self._sendingQueue.empty()):
                print("sending")
                tup = self._sendingQueue.get()
                client(tup[0],tup[1], "1000176")
            time.sleep(3)

    def receivingLoop(self):
        while(True):
            print("receiving")
            item = server("10.0.0.159")
            print("Updating based on recieved information...")

            # For now, just assume that the first column is the x array and the rest is the matrix
            print("Shape of received item:")
            print(np.array(item).shape)
            print("Item:")
            print(item)
            self._x = item[:,0]
            self._matrix = item[:,1:]
            self._matrixReady = True
            time.sleep(3)

    def multLoop(self):
        while(True):
            
            # Wait until there is a matrix to be multiplied.
            if(self._matrixReady):

                # Compute the matrix multiplication, then add it to the sending queue
                self._sendingQueue.put(np.matmul(self._x,self._matrix))
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


    def addMatrix(self, matrix):
        self._matrix = matrix


    def distributeData(matrix):

        # This matrix is how we will spread the data, which has 3 parts, onto six machines
        dist_mat = [[1, 0, 0, 1, 1, 1],
                    [0, 1, 0, 1, 2, 4],
                    [0, 0, 1, 1, 3, 9]]

        # For each machine in the system, send them their data, which is (matrix*dist_mat)[i] 
        # where i is the index of the machine
        
        result = np.matmul(matrix, dist_mat)
        for i in range(0, MAX_DEVICES):
            # send to device i result[i]
            i;

if (__name__ == "__main__"):
    node = Node()
    node.addMatrix(np.random.rand(20,20))
    node.matrixSplit(100)

