import numpy as np
from MasterClient import *
from MasterServer import *
from node import *

def main():

    # Create a matrix and a vector to be multiplied
    print("Generating a random matrix of size: [100,100]")
    A = np.random.rand(100,100)
    x = np.random.rand(100,1)

    # Check how many nodes are in the network, then split the matrix based on that
    print("Checking how many nodes:")
    print("Found 1 node.")

    # Split the matrix A into 2 parts using the node
    # method
    print("Splitting the matrix into 1 parts")
    node = Node()
    node.addMatrix(A)
    node.matrixSplit(1)

    # Send x and submatrices of A to the two worker nodes
    # The IP addresses of the worker nodes
    ip1 = "10.0.0.159"
    ip2 = "10.0.0.176"

    # Create an aggr_server to send 
    # then send the data to each device
    print("Sending random matrix of size: 100")
    client1 = master_client(ip1, np.concatenate((x,A[:,:node._partitions[0]]),axis=1))
    #client2 = master_client(ip2,(x,A[:,node._partitions[0]:]))

    print("Sending complete!")


    # Wait to hear a response
    print("Waiting for results...")
    serv = master_server("10.0.0.97",1)

    print("Exiting...")


if(__name__ == "__main__"):
    main()
