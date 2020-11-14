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
from enum import IntEnum
class Message(IntEnum):
    PREEMPT = 1
    RESTART = 2
    MATRICES = 3
    PING = 4
    PONG = 5

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
    print("Encoding the data...")
    _g = np.zeros((nodes,recoveryThreshold))
    A_encoded = np.zeros((nodes,int(len(A)/nodes),len(A[0])))
    for i in range(0,nodes):
        _g[i] = node.generateMatrixOfRank(recoveryThreshold,1,recoveryThreshold)
        A_encoded[i] = encode(A,_g)
    

    # Create an aggr_server to send 
    # then send the data to each device
    print(node._partitions)
    for i in range(0,nodes):
        print("Sending matrix of size " + str(len(A_encoded[i]))+ " to the node at " + IP_ADDRESSES[i])
        data = np.concatenate((np.transpose(x),A_encoded[i]))
        msg = types.SimpleNamespace(messageType = Message.MATRICES, data = data)
        client1 = master_client(IP_ADDRESSES[i], msg)

    print("Sending complete!")


    # Wait to hear a response
    print("Waiting for results...")
    serv = master_server("10.0.0.97",1)

    # Reassemble the received data
    print("reassembling received data...")
    AB_encoded = serv.data
    _h = 1 / (np.transpose(_g))

    # Compare the result with the local computation to verify accuracy
    print("Comparing results with locally computed multiplication to verify...")

    # Test again with preemption
    print("testing again with preemption...")

    print("Exiting...")

# Encode the matrix A with the vector g
def encode(A, g):

    n = len(g)
    partitions = np.linspace(0,len(A),num=n+1,dtype=int)
    sumA = np.zeros((int(len(A)/n), len(A[0])))
    for i in range(0,n):
        A[partitions[i]:partitions[i+1],:] = A[partitions[i]:partitions[i+1],:] * g[i]
        sumA = sumA + A[partitions[i]:partitions[i+1],:]

    return(sumA)

if(__name__ == "__main__"):
    main()
