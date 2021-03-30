# Author: HTC 02/21/21
# A basic synchronous gradient descent scheme
# 1. "Random" data matrix sent to workers
# 2. workers compute gradient vectors send to agg
# 3. Agg combines gradient vectors, normalizes then sends back to nodes
# 4. Process repeats until iteration limit hit


from matrix_b_fr import matrix_b_fr
from matrix_b_cyc import matrix_b_cr
from matrix_a import matrix_a
from aggr_client_v1_3 import client
from aggr_server import aggr_server as server
from eigen_decomp import build_random_matrix
from matrix_operations import matrix_merge, matrix_split, partition
import threading
import queue
import numpy as np
import time

# Program timer
start = time.time()

# rp_addresses defines the number of clients participating in the experiment including stragglers



class Agg:
    # Constructor
    def __init__(self):
        # beginning time stamp
        time_init_start = time.time()

        # This queue holds information that we need to send
        self._sendingQueue = queue.Queue(maxsize=40)

        # Initialize variables
        self._laptop_address = '192.168.0.6'
        self._rp_addresses = ['192.168.0.18', '192.168.0.19', '192.168.0.17']
        self._item = []         # variable for received data
        self._length = 1200      # variable for length of dataset
        self._iterations = 150  # variable to specify how many iterations to carry out
        self._count = 0         # variable for tracking how many iterations have been complete
        self._time_init = 0
        self._time_send_list = []
        self._time_receive_list = []
        self._action_time_list = []
        self._ready_to_process = False

        # Threads for sending and receiving information from the other nodes
        self._sendingThread = threading.Thread(target=self.sending_loop)
        self._sendingThread.start()
        self._receivingThread = threading.Thread(target=self.receiving_loop)
        self._receivingThread.start()
        self._actionThread = threading.Thread(target=self.action_loop)
        self._actionThread.start()

        # Generate a random data matrix
        self._n = len(self._rp_addresses)
        self._s = 0   # No stragglers in this vanilla model
        print("n: ", self._n)
        print("s: ", self._s)
        self._rand_data = build_random_matrix(self._length, np.array([1, 0.85, 0.8, 0.82, 0.7, 0.6, 0.5, 0.4, 0.3]))
        print("rand_data: \n", self._rand_data[0:6, 0:6], "\n shape of rand_data: ", np.shape(self._rand_data))

        # Partition random dataset column-wise
        parts = partition(self._rand_data, self._n, by_rows=0)
        print("partition 1: ", parts[0][0:5, 0:5], "\nShape of partition 1: ", np.shape(parts[0]))
        print("partition 2: ", parts[1][0:5, 0:5], "\nShape of partition 2: ", np.shape(parts[1]))
        print("partition 3: ", parts[2][0:5, 0:5], "\nShape of partition 3: ", np.shape(parts[2]))

        # Place worker vectors in the queue
        self._sendingQueue.put(parts[0])
        self._sendingQueue.put(parts[1])
        self._sendingQueue.put(parts[2])

        # Time stamp
        time_init_end = time.time()
        self._time_init = time_init_end - time_init_start
        print("Constructor time: ", self._time_init)

    # A loop to send messages to aggregator
    def sending_loop(self):
        index = 0
        while True:
            if not self._sendingQueue.empty():
                send_time_start = time.time()
                tup = self._sendingQueue.get()
                print("Sending to worker", index)
                try:
                    client(self._rp_addresses[index], tup)
                except ConnectionRefusedError:
                    time.sleep(.5)
                    client(self._rp_addresses[index], tup)
                print("Finished Sending")
                index += 1
                print("index: ", index)
                if index == (self._n - self._s):
                    print("Index reset")
                    index = 0
                # Time stamp
                send_time_end = time.time()
                self._time_send_list.append(send_time_end - send_time_start)
                print("Sending iteration time: ", send_time_end - send_time_start)
            else:
                time.sleep(3)

    # A loop to receive messages from nodes
    def receiving_loop(self):
        while True:
            receive_time_start = time.time()
            self._item = server(self._laptop_address, 3, self._length, naive=True)
            print("received data from nodes")
            print("item.fn:", self._item.fn, "\nitem.w", self._item.w)
            self._ready_to_process = True

            # Time stamp
            receive_time_end = time.time()
            self._time_receive_list.append(receive_time_end - receive_time_start)
            print("Receiving iteration time: ", receive_time_end - receive_time_start)
            time.sleep(3)

    # A loop to perform actions on the received data
    def action_loop(self):
        while True:
            if self._ready_to_process:
                start_time = time.time()
                # Get the sum of the gradients
                grad_sum = self._item.w[:, 0] + self._item.w[:, 1] + self._item.w[:, 2]
                print("g_1 + g_2 + g_3 = \n", grad_sum, "\nShape of sum: ", np.shape(grad_sum))
                b = np.reshape(grad_sum, (np.shape(grad_sum)[0], 1))
                print("b: \n", b[0:10, :], "\nshape of b: ", np.shape(b))

                # Normalize
                b_norm = np.linalg.norm(b)
                b_new = b/b_norm
                print("b_k+1 = \n", b_new[0:10, :], "\nShape of new vector: ", np.shape(b_new))

                # Partition vector
                vector_parts = partition(b_new, self._n, by_rows=1, vect=1)
                print("vect part 1: ", vector_parts[0][0:10, :], "\n shape of part 1: ", np.shape(vector_parts[0]))
                print("vect part 2: ", vector_parts[1][0:10, :], "\n shape of part 2: ", np.shape(vector_parts[1]))
                print("vect part 3: ", vector_parts[2][0:10, :], "\n shape of part 3: ", np.shape(vector_parts[2]))
                vector_send = [vector_parts[0], vector_parts[1], vector_parts[2]]
                print("\n shape of vector send: ", np.shape(vector_send))

                # Place the new vector in the que n times to be sent and update counters
                print("count: ", self._count)
                if self._count == self._iterations:
                    print("Experiment completed")
                    for i in range(self._n):
                        self._sendingQueue.put("All done")
                    end = time.time()
                    print("runtime (seconds): ", end - start)
                    print("\nfinal gradient vector:", b_new[0:10, :])
                    print("\nSending time list: ", self._time_send_list)
                    print("\nreceiving list: ", self._time_receive_list)
                    print("\naction time list: ", self._action_time_list)
                else:
                    for i in range(self._n - self._s):
                        self._sendingQueue.put(vector_send[i])
                        print("Queue size: ", self._sendingQueue.qsize())
                    self._count += 1
                    # Time stamp
                    end_time = time.time()
                    self._action_time_list.append(end_time - start_time)
                    print("Processing iteration time: ", end_time - start_time)
                self._ready_to_process = False
            else:
                time.sleep(3)

    # A function to return time stamp data
    def return_time(self):
        return self._time_send_list, self._time_receive_list, self._action_time_list


if __name__ == "__main__":
    agg = Agg()
    list_1, list_2, list_3 = agg.return_time()
