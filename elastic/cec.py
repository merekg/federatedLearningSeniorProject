# CEC: Coded elastic computing.

# this file is based on the algorithm described in Yang et. al.
# Author: MCG

# Inputs: 
# X: the data matrix
# p: number of machines
# l: the recovery threshold
# g[i][j]: the linear combination coefficients to partition the data
# w[t]: the input vectors for each process

# Steps of the algorithm:
# 1) Partition the data X into l subsets and compute the coded subsets based on g.
# 2) For each computation with input w[t]
    # a. The master node sends w[t] to each worker.
    # b. for each group index j:
        # i. The k-th worker computes u[t][k][j] for all workers that use the j-th sub-block
        #     and obtains the matrix u[t][j] which contains the results for the j-th group (row block).
        # ii. Decode. The master node computes u[t][j](G_inv[j]) to obtain the results for the j-th
        #     group. 
    # c. The master node outputs X_W[t]
    # d. If preemption or addition of new machines: change the selected data to use based on the 
    #    current number of machines.

def main():

def partition():

def send():

def masterLoop():

def workerLoop():

def changeP(p):

if(__name__ == "__main__"):
    main()
