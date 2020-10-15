# A simple main file to verify all the RPs can communicate with the laptop
# Meant to be uploaded and executed on each of the nodes
#   Steps:
#   1. begin threads
#   2. Call mcast_node_client file
#   3. Call mcast_node_server file

from node_server import server
from node_client import client
import threading
import numpy as np

laptop_address = '192.168.0.6'
wout = "Hello Aggregator"   # basic text message for testing purposes
fn = np.zeros(2)            # Not sure what this value should be...
thread_recv = threading.Thread(target=server, args=laptop_address)
thread_send = threading.Thread(target=client, args=(wout, fn, laptop_address))
thread_recv.start()
thread_send.start()


