import numpy as np
import threading
import copy
import time
import itertools

def work(p,q):
    for i in range(0,1000):
        A = np.random.rand(p, q)
        x = np.random.rand(1, p)
        np.matmul(x,A)

# Set up matrices and other values
print("Generating random matrices and setting up...")

input("Done. Press enter when you are ready to run power iteration.")

# Run the program with no encoding
print("Naive method (no encoding)")
startTime = time.time()

work(100,100)

endTime = time.time()
print("Total time: " + str(endTime - startTime))
input("Press enter when you are ready to run power iteration.")

# Run the program with encoding
print("Smart method (with encoding)")
startTime = time.time()

thread1 = threading.Thread(target=work, args=(100,50),daemon=True)
thread2 = threading.Thread(target=work, args=(100,50),daemon=True)
thread1.start()
thread2.start()
thread1.join()
thread2.join()

endTime = time.time()
print("Total time: " + str(endTime - startTime))

