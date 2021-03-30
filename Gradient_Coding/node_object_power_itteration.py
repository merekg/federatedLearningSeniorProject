# Adapted from MCG's node.py
# Additions by HTC
# Test to show that the partition recovery matrices work

import queue
import threading
import time
import numpy as np
from matrix_operations import *
from node_client import client
from node_server import server

# Initialize global variables
laptop_address = '192.168.0.6'


class Node:

    # CONSTRUCTOR
    def __init__(self):
        # Define the device's IP_address.
        self._ipAddr = '192.168.0.17'   # update on each node locally

        # when a matrix is ready for grad calc toggle to True
        self._matrixReady = False

        # initialize the private variables that will be used in sending, receiving, multiplying and timekeeping
        self._g = []
        self._matrix = []
        self._count = 0
        self._vect = []
        self._time_send = []
        self._time_receive = []
        self._time_mult = []

        # This queue holds information that we need to send
        self._sendingQueue = queue.Queue(maxsize=40)

        # Threads for sending and receiving information from the other nodes
        self._sendingThread = threading.Thread(target=self.sending_loop)
        self._sendingThread.start()
        self._receivingThread = threading.Thread(target=self.receiving_loop)
        self._receivingThread.start()

        # Thread for doing the matrix gradient work
        self._gradThread = threading.Thread(target=self.mult_loop)
        self._gradThread.start()

    # A loop to send messages to aggregator

    def sending_loop(self):
        while True:
            if not self._sendingQueue.empty():
                time_start = time.time()
                time.sleep(.5)
                print("Sending...")
                tup = self._sendingQueue.get()
                # include this try except loop to catch any socket errors
                try:
                    client(tup, self._ipAddr, laptop_address)
                except ConnectionRefusedError:
                    time.sleep(2)
                    try:
                        client(tup, self._ipAddr, laptop_address)
                    except ConnectionRefusedError:
                        time.sleep(2)
                        client(tup, self._ipAddr, laptop_address)
                time_end = time.time()
                self._time_send.append(time_end - time_start)
                print("Sending time: ", time_end - time_start)
            time.sleep(3)

    # A loop to receive messages from aggregator

    def receiving_loop(self):
        while True:
            if self._count == 0:
                time_start = time.time()
                self._matrix = server(self._ipAddr)
                print("Updating based on received information...")
                print("item: \n", self._matrix)
                print("Shape of received item:", np.shape(self._matrix))
                self._vect = np.ones((int(np.shape(self._matrix)[1]/2), 1))
                self._matrixReady = True

                # Time Stamp
                time_end = time.time()
                self._time_receive.append(time_end - time_start)
                print("Receiving time: ", time_end - time_start)
                time.sleep(3)
            else:
                time_start = time.time()
                self._vect = server(self._ipAddr)
                print("Updating based on received information...")
                print("item: \n", self._vect)
                print("Shape of received item:", np.shape(self._vect))
                if self._vect == "All done":
                    print("All done")
                    exit()
                self._matrixReady = True

                # Time Stamp
                time_end = time.time()
                self._time_receive.append(time_end - time_start)
                print("Receiving time: ", time_end - time_start)
                time.sleep(3)
    # Calculate matrix multiplication for each partition

    def mult_loop(self):
        while True:
            # do nothing until a matrix is received
            if self._matrixReady:
                # calculate the gradient for each partition
                if self._count == 0:
                    time_start = time.time()
                    mat_1, mat_2 = matrix_split(self._matrix, rows=0)
                    print("mat split 1:\n", mat_1, "\nShape mat 1: ", np.shape(mat_1))
                    print("mat split 2:\n", mat_2, "\nShape mat 2: ", np.shape(mat_2))
                    print("vector: \n", self._vect, "\nShape of Vect: ", np.shape(self._vect))
                    g_1 = mat_1 @ self._vect
                    print("g_1: \n", g_1, "\n", np.shape(g_1))
                    g_2 = mat_2 @ self._vect
                    print("g_2: \n", g_2, "\n", np.shape(g_2))

                else:
                    time_start = time.time()
                    print("Shape of mat_1:", np.shape(mat_1), "\nShape of vect:", np.shape(self._vect))
                    g_1 = mat_1 @ self._vect[:, 0]
                    g_1 = np.reshape(g_1, (np.shape(g_1)[0], 1))
                    print("g_1: \n", g_1, "\n", np.shape(g_1))
                    g_2 = mat_2 @ self._vect[:, 1]
                    g_2 = np.reshape(g_2, (np.shape(g_2)[0], 1))
                    print("g_2: \n", g_2, "\n", np.shape(g_2))

                # merge the gradients together (for sending purposes), send back, and update counter
                self._g = matrix_merge(g_1, g_2, 1)
                print("self._g: \n", self._g, "\n", np.shape(self._g))
                self._sendingQueue.put(self._g)
                self._count += 1
                print("count: ", self._count)
                self._matrixReady = False

                # Time Stamp
                time_end = time.time()
                self._time_mult.append(time_end - time_start)
                print("Receiving time: ", time_end - time_start)
            else:
                time.sleep(1)


if __name__ == "__main__":
    node = Node()
