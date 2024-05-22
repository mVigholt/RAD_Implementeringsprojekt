from ctypes import *

b = 89 # (89 / 8) = 12 bytes
m = 2**64 #k = m = 2t
a0 = 0x478ad369f6852eac0de7ccf7
a1 = 0xd472f7b830cf473f771bf810
a2 = 0x695b4252f2c52ba0031649c4
a3 = 0xd4e0ab8bb4907f43b1ede881
A = [a0,a1,a2,a3]

#Opgave 4
def q_universal_hash(b, A, x):
    p = (2**b)-1 #0x01FFFFFFFFFFFFFFFFFFFFFF
    q = len(A)
    a = list(map(lambda x: p&x, A))

    y = a[q-1] 
    for i in range(q-2, -1, -1): 
        y = y*x + a[i]  
        y = (y&p) + (y>>b)  
    if (y >= p):  
        y = y-p 
    return y

#Opgave 5
def sign_and_hash(k, b, A, x):
    #q_universal_hash(x) mod k
    g = q_universal_hash(b, A, x) 
    h = g & (k - 1)
    b = g >> (b - 1)
    s = 1 - (2*b)
    return (s,h)