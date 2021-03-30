# This script generates a random matrix based on eigenvalue decomposition
# based off Mingyue Ji's Uncoded_CEC_Power_Iteration.py file

import numpy as np


def build_random_matrix(length, eig_values=np.array([1, 0.94, 0.7, 0.6, 0.5])):
    num_eigs = len(eig_values)
    if num_eigs != length:
        eig_values = np.append(eig_values, np.zeros(length - num_eigs))
        # print(eig_values)
        num_eigs = len(eig_values)

    # Gram-Schmidt process to create orthogonal eigen vectors
    B = np.random.rand(num_eigs, length)  # used to define eigen vectors
    # print(B)
    for i in range(num_eigs):
        for j in range(i):
            B[i] -= B[j] * np.dot(B[j], B[i]) / np.linalg.norm(B[j])
        B[i] = B[i] / np.linalg.norm(B[i])

    # Multiply matrices to build final matrix
    mat = B @ np.diag(eig_values) @ np.transpose(B)
    return mat

'''
# Test Code
rand = build_random_matrix(1200, [0.95, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])
print("Rand: \n", rand, "\nShape of Rand: ", np.shape(rand))

# Find eigen vectors
eig_vals, eig_vect = np.linalg.eig(rand)
index = np.where(eig_vals == np.max(eig_vals))
print('loc of max eigen value: ', index)


b = np.ones((np.shape(rand)[0]))
print('Starting b: ', b)
num_iter = range(100)

for i in num_iter:
    b_new = np.dot(rand, b)
    print('b_new: ', b_new)

    b_norm = np.linalg.norm(b_new)
    print('b_norm: ', b_norm)

    b = b_new / b_norm
    print('b: ', b)

    error = np.linalg.norm(eig_vect[:, index] - b)
    print('Error: ', error)
    print()

# print('Eigen values: ', eig_vals)
# print('Eigen vectors: ', eig_vect)
# print('Max Eigen Val: ', eig_vals[-1])
print('Max Eigen vect: ', eig_vect[:, index])

# do a comparison between b and the max eigen vector
no_wrong = 0
tol = .1
for count, j in enumerate(eig_vect[:, index]):
    if abs(j - b[count]) >= tol:
        print("Found a wrong value")
        no_wrong += 1
print('no_wrong: ', no_wrong)
'''


