import numpy as np

# a = np.array([i for i in range(10)])
#
# b = np.array([j for j in reversed(range(10))])
#
# index = abs(a - b) <= 1

# c = np.array([[j for j in range(10)], [j for j in range(10)]])
# print(c[[False, True]])
#
# for i in range(100):
#     min = 10
#     max = 60
#     a = 0.3
#     b = 0.5
#
#     if i < min:
#         cur = a
#     elif i >= max:
#         cur = b
#     else:
#         cur = a + round((b - a) / (max - min) * (i-min), 2)
#     print(i, " : ", cur)


import time

current_GMT = int(time.time())


print(current_GMT)

