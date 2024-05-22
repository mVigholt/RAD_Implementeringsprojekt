from ctypes import *

def q_universal_hash(x):
    q = 4
    b = 89
    p = (2**b)-1 #0x01FFFFFFFFFFFFFFFFFFFFFF
    a0 = p & 0x478ad369f6852eac0de7ccf7
    a1 = p & 0xd472f7b830cf473f771bf810
    a2 = p & 0x695b4252f2c52ba0031649c4
    a3 = p & 0xd4e0ab8bb4907f43b1ede881
    A = [a0,a1,a2,a3]
    
    y = A[q-1] # y ← aq−1;
    for i in range(q-2, -1, -1): # for i = q − 2, . . . , 0 do
        y = y*x + A[i] # y ← yx + ai 
        y = (y&p) + (y>>b) # y ← (y&p) + (y>>b) 
    if (y >= p): # if y ≥ p then 
        y = y-p #y ← y − p;
    return y
