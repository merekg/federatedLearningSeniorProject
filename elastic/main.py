import numpy as np
from MasterClient import *
from MasterServer import *
from node import *
import sys

MAX_NODES = 6
MIN_NODES = 1
MIN_MATRIX_SIZE = 1
MAX_MATRIX_SIZE = 10000

# Enumerate the message types
from enum import Enum
class Message(Enum):
    PREEMPT = 1
    RESTART = 2
    MATRICES = 3
    PING = 4

def main():
    # whenever new devices are added to the network, make sure that the IP addresses are added
    IP_ADDRESSES = ["10.0.0.176", "10.0.0.159"]

    # Check that the user gave the correct number of inputs
    if(len(sys.argv)!=4):
        print("USE: main <number of requested nodes> <recovery threshold> <matrix size>")
        return

    nodes = int(sys.argv[1])
    recoveryThreshold = int(sys.argv[2])
    matrixSize = int(sys.argv[3])

    # check that the passed parameters are within the range we expected
    assert nodes >= MIN_NODES and nodes <= MAX_NODES
    assert recoveryThreshold >= MIN_NODES and recoveryThreshold <= nodes
    assert matrixSize >= MIN_MATRIX_SIZE and matrixSize <= MAX_MATRIX_SIZE

    # Create a matrix and a vector to be multiplied
    print("Generating a random matrix of size: " + str(matrixSize) + "x" + str(matrixSize) + "...")
    A = np.random.rand(matrixSize, matrixSize)
    x = np.random.rand(matrixSize,1)

    # Split the matrix A into n parts using the node method
    print("Splitting the matrix into " + str(recoveryThreshold) + " parts.")
    node = Node()
    node.addMatrix(A)
    node.matrixSplit(recoveryThreshold)

    # Encode the data

    # Create an aggr_server to send 
    # then send the data to each device
    print(node._partitions)
    for i in range(0,nodes):
        print("Sending matrix of size " + str(len(A[:,:node._partitions[i]])) + " to the node at " + IP_ADDRESSES[i])
        if i == 0:
            client1 = master_client(IP_ADDRESSES[i], np.concatenate((x,A[:,:node._partitions[i]]),axis=1))
        else:
            client1 = master_client(IP_ADDRESSES[i], np.concatenate((x,A[:,node._partitions[i-1]:node._partitions[i]]),axis=1))

    print("Sending complete!")


    # Wait to hear a response
    print("Waiting for results...")
    serv = master_server("10.0.0.97",1)

    # Reassemble the received data
    print("reassembling received data...")

    # Compare the result with the local computation to verify accuracy
    print("Comparing results with locally computed multiplication to verify...")

    # Test again with preemption
    print("testing again with preemption...")

    print("Exiting...")


if(__name__ == "__main__"):
    main()
