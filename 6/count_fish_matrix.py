import numpy as np

cur = np.array([0,145, 39, 53, 33, 30, 0, 0, 0], dtype=np.int64)

T = np.matrix([[0,0,0,0,0,0,1,0,1],
               [1,0,0,0,0,0,0,0,0],
               [0,1,0,0,0,0,0,0,0],
               [0,0,1,0,0,0,0,0,0],
               [0,0,0,1,0,0,0,0,0],
               [0,0,0,0,1,0,0,0,0],
               [0,0,0,0,0,1,0,0,0],
               [0,0,0,0,0,0,1,0,0],
               [0,0,0,0,0,0,0,1,0]])

def power(T, n):
    if n == 0:
        return np.eye(9).astype(int)
    if n == 1:
        return T
    else:
        return power(T,n//2) * power(T,(n +1)//2)

print(f'After 80 steps we have {(cur * power(T, 80)).sum()}')
print(f'After 256 steps we have {(cur * power(T, 256)).sum()}')
