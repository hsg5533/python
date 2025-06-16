import numpy as np

x, y, z, r, w = map(int, input('x1: ').split())
depth = int(input('depth: '))

def one_hot(i):
    a = np.zeros(depth, 'float32')
    a[i] = 1
    return a

a = one_hot(x)
b = one_hot(y)
c = one_hot(z)
d = one_hot(r)
e = one_hot(w)

d = np.array([a,b,c,d,e])
print(d,'dtype=',d.dtype)

