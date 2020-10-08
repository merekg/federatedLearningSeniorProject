# Node:
# Author: MCG

# the node object represents the work done on each machine in the network.

import queue
import time
import threading
import sys
# Add the folders above
sys.path.append('../')
#import node_client.py

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

        time.sleep(40)

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
    def matrixSplit(matrix, n):

        diff = 0
        fraction = len(matrix)/n
        for i in range(0,n):
            split  = round(fraction + diff)
            print(split)
            diff = diff + fraction - split
            print(diff)

    def addMatrix(self, matrix):

        self._matrix = matrix


if (__name__ == "__main__"):
    node = Node()

