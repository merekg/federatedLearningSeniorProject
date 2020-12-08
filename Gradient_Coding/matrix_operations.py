# Houses some of the frequent matrix operations the node and agg will need to do
# HTC 11/09/20

import numpy as np

# matrix merge operation
# Inputs: mat_1, mat_2, and axis (axis=1 merges about columns, axis=0 merges about rows)
# Note that mat_1 and mat_2 must have the same shape except in the dimension corresponding to the axis
# Outputs: matrix, the merged form of mat_1 and mat_2


def matrix_merge(mat_1, mat_2, axis):
    matrix_out = np.concatenate((mat_1, mat_2), axis=axis)
    print("matrix merged. Final dimensions: \n", np.shape(matrix_out))
    return matrix_out


# matrix split operation using array slicing. Slices by rows. Only splits into 2 matrices
# Inputs: a matrix (e.g. 1000 x 1000)
# Outputs: mat_1 and mat_2 each of identical dimensions (e.g. 500 x 1000)
def matrix_split(matrix):
    mat_1 = matrix[:, 0:int(np.shape(matrix)[1] / 2)]
    mat_2 = matrix[:, int(np.shape(matrix)[1] / 2):int(np.shape(matrix)[1])]
    print("Matrix split in 2 matrices of shape: \n", np.shape(mat_1), np.shape(mat_2))
    return mat_1, mat_2



