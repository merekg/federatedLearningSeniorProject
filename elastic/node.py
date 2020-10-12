# Node:
# Author: MCG

# the node object represents the work done on each machine in the network.

import queue
import time
import threading
import sys
import numpy as np
# Add the folders above
sys.path.append('../')
#import node_client.py

# The max number of devices in the network
MAX_DEVICES = 8

class Node:

    # queue of all things that need to be sent
    _sendingQueue = queue.SimpleQueue()

    # Constructor
    def __init__(self):

        # Get the device's IP address.
        f = open("/opt/cec/ip.txt", "r")
        ipAddr = f.read()
        
        # Get rid of the periods, cast to int
        self._ipAddr = int(ipAddr.replace('.', ''))

        # Determine the node index based on the ip address.
        if(self._ipAddr == 100097):
            self._nodeID = 0; # desktop
        if(self._ipAddr == 1000236):
            self._nodeID = 1;
        if(self._ipAddr == 1000219):
            self._nodeID = 2;

        # Threads for sending and receiving information from the other nodes
        self._sendingThread = threading.Thread(target=Node.sendingLoop, daemon=True)
        self._sendingThread.start()
        self._receivingThread = threading.Thread(target=Node.receivingLoop, daemon=True)
        self._receivingThread.start()
        print("the main thread continues")

        # The _partitions object keeps track of the partitions of the matrix.
        # Each element in the array corresponds to the size of the partition
        self._partitions = np.zeros(MAX_DEVICES) - 1

    def sendingLoop():
        while(True):
            print("sending")
            time.sleep(3)

    def receivingLoop():
        while(True):
            print("receiving")
            time.sleep(3)

    # This script will take a matrix and divide it into n parts.
    # It will make the parts as evenly sized as possible while still maintaining the rows and columns.
    def matrixSplit(self, n):

        diff = 0
        fraction = len(self._matrix)/n
        for i in range(0,n):
            split  = round(fraction + diff)
            self._partitions[i] = split
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
        for i in range(0, MAX_DEVICES)):
            # send to device i result[i]

if (__name__ == "__main__"):
    node = Node()
    node.addMatrix(np.random.rand(20,20))
    node.matrixSplit(100)

