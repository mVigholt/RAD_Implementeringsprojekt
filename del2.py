from ctypes import *
import numpy as np
from create_stream import CreateStream

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
    a = list(map(lambda x: p&x, A)) # this ensures each coefficient is within the range [0,p−1]

    y = a[q-1] 
    for i in range(q-2, -1, -1): # starts with the highest degree coefficient
        y = y*x + a[i] # multiplies by x and adds the next coefficient
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

#Opgave 6
class CountSketch:
    def __init__(self, t, b, A):
        self.t = t
        self.b = b
        self.A = A
        self.m = 2**t
        self.table = np.zeros(self.m, dtype=int) # Initialize a table with m zeros
    
    def update(self, x, s):
        s, h = sign_and_hash(self.m, self.b, self.A, x)
        self.table[h] += s # Update the table at position h by adding s
    
    def estimate(self):
        return np.sum(self.table**2) # Estimate by summing squares of the table entries

# Example
t = 16  # Example t value (log2(m))
count_sketch = CountSketch(t, b, A)

# Generate stream and update sketch
stream = CreateStream(10000, 16)

for x, s in stream:
    count_sketch.update(x, s)

# Estimate the sum of squared counts
estimate = count_sketch.estimate()
print("Estimate:", estimate)

#Opgave 7 
def hashing_parameters():
    #Generate parameters for 100 random 4-universal hashfunctions:
    file = open('RandomHex.txt','r') ##4800 byte in hex from https://www.random.org/bytes/
    content = file.read().split()
    AA = []
    for i in range(0,len(content),12*4):
        A = []
        for j in range(0,12*4,12):
            hex_string = ""
            for k in range(12):
                hex_string += content[i+j+k]
            A.append(int(hex_string, 16))
        AA.append(A)
    return AA