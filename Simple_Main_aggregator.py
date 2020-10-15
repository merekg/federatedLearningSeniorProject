# A simple file to verify the laptop can communicate with the RPs
# Meant to be executed on the device acting as the aggregator
# Steps:
#   1. Begin Threads
#   2. Call aggr_client_v1_3 client function
#   3. Call aggr_server function

from aggr_client_v1_3 import client
from aggr_server import aggr_server
import threading
import numpy as np

laptop_address = '192.168.0.6'
pi_address = '192.168.0.17'         # corresponds to RP no. 1

