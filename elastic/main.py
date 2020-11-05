import numpy as np
from MasterClient import *
from MasterServer import *
from node import *
import sys


def main():
    IP_ADDRESSES = ["10.0.0.176", "10.0.0.159"]

    # Check that the user gave the correct number of inputs
    if(len(sys.argv)!=3):
        print("USE: main <number of requested nodes> <recovery threshold>")
        return

    nodes = int(sys.argv[1])
    recoveryThreshold = int(sys.argv[2])

    # Create a matrix and a vector to be multiplied
    print("Generating a random matrix of size: [100,100]")
    A = np.random.rand(100,100)
    x = np.random.rand(100,1)

    # Split the matrix A into n parts using the node
    # method
    print("Splitting the matrix into " + str(recoveryThreshold) + " parts.")
    node = Node()
    node.addMatrix(A)
    node.matrixSplit(recoveryThreshold)

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

    print("Exiting...")


if(__name__ == "__main__"):
    main()
