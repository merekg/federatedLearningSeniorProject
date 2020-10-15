# Author: HTC

# This function generates a_mat such that A_mat @ B_mat = 1
# Inputs: b_mat: 2D array, number of stragglers (s): int, number of clients (n): int
# Outputs: a_mat: 2D array

import itertools
import numpy as np
import math as m


def matrix_a(b_mat, n, s):
    # Create all the possible subsets
    n_list = list(range(0, n))
    length_subset = n - s
    sub_list = list(itertools.combinations(n_list, length_subset))
    # Solve for Matrix A s.t. AB = 1 (f x k)
    f = m.comb(n, s)
    a_mat = np.zeros(np.array([f, n]))
    for i in n_list:
        a = np.zeros(np.array([1, n]))[0]
        ones = np.ones(n)
        rows_b = b_mat[np.asarray(sub_list[i])]
        rows_b_t = np.transpose(rows_b)
        x = np.linalg.lstsq(rows_b_t, ones)
        a[np.asarray(sub_list[i])] = x[0]
        a_mat[n - 1 - i] = a

    # print("a_mat: \n", a_mat)
    # print("b_mat: \n", b_mat)
    # print("a_mat @ b_mat: \n", a_mat @ b_mat)
    return a_mat

# sample code
# b_mat = np.asarray([[.5, 1, 0], [0, 1, -1], [0.5, 0, 1]])
# n = 3
# s = 1
# a_mat(b_mat, n, s)
