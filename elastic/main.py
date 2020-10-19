import numpy as np
from MasterClient import *
from node import *

def main():
    #print("llo world")

    # Create a matrix and a vector to be multiplied
    A = np.random.rand(100,100)
    x = np.random.rand(100,1)

    # Split the matrix A into 2 parts using the node
    # method
    node = Node()
    node.addMatrix(A)
    node.matrixSplit(2)
    print(node._partitions)

    # Send x and submatrices of A to the two worker nodes
    # The IP addresses of the worker nodes
    ip1 = "10.0.0.159"
    ip2 = "10.0.0.176"

    # Create an aggr_server to send 
    # then send the data to each device
    client1 = master_client(ip1, np.concatenate((x,A[:,:node._partitions[0]]),axis=1))
    #client2 = master_client(ip2,(x,A[:,node._partitions[0]:]))


if(__name__ == "__main__"):
    main()
