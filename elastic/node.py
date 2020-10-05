# Node:
# Author: MCG

# the node object represents the work done on each machine in the network.

import queue
import time
import threading
import sys
# Add the folders above
sys.path.append('../')
import node_client.py

class Node:

    # Which machine is this
    _nodeID = -1
    _ipAddr = -1

    # queue of all things that need to be sent
    _sendingQueue = queue.SimpleQueue()

    # Constructor
    def __init__(self):

        # Get the device's IP address.
        f = open("/opt/cec/ip.txt", "r")
        ipAddr = f.read()
        
        # Get rid of the periods, cast to int
        _ipAddr = int(ipAddr.replace('.', ''))

        # Determine the node index based on the ip address.
        if(_ipAddr == 100097):
            _nodeID = 0; # desktop
        if(_ipAddr == 1000236):
            _nodeID = 1;
        if(_ipAddr == 1000219):
            _nodeID = 2;

        # Threads for sending and receiving information from the other nodes
        _sendingThread = threading.Thread(target=Node.sendingLoop, daemon=True)
        _sendingThread.start()
        _receivingThread = threading.Thread(target=Node.receivingLoop, daemon=True)
        _receivingThread.start()

        time.sleep(40)

    def sendingLoop():
        while(True):
            print("sending")
            time.sleep(3)

    def receivingLoop():
        while(True):
            print("receiving")
            time.sleep(3)


if (__name__ == "__main__"):
    node = Node()

