import numpy as np

matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Combining slicing along rows and columns
sub_matrix = matrix[0:3, 0:3]
print(sub_matrix)