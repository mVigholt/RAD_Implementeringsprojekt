import pathlib
import numpy as np

#Opgave 4
def q_universal_hash(b: int, A: list, x: int):
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
def sign_and_hash(k: int, b: int, A: list, x: int):
    #q_universal_hash(x) mod k
    g = q_universal_hash(b, A, x) 
    h = g & (k - 1)
    b = g >> (b - 1)
    s = 1 - (2*b)
    return (s,h)

#Opgave 6
class CountSketch:
    def __init__(self, t: int, b: int, A: list):
        self.t = t
        self.b = b
        self.A = A
        self.m = 2**t
        self.table = np.zeros(self.m, dtype=int) # Initialize a table with m zeros
    
    def update(self, x: int, s: int) -> None:
        s, h = sign_and_hash(self.m, self.b, self.A, x)
        self.table[h] += s # Update the table at position h by adding s
    
    def estimate(self) -> np.signedinteger:
        return np.sum(self.table**2) # Estimate by summing squares of the table entries

#Opgave 7 
def hashing_parameters(path: pathlib.Path) -> list:
    #Generate parameters for 100 random 4-universal hashfunctions:
    file = open(path,'r') ##4800 byte in hex from https://www.random.org/bytes/
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

def GenerateCountSketch(stream: list, 
                        t: int, b: int, 
                        path=pathlib.Path("./RandomHex.txt")):
    AA = hashing_parameters(path)
    X = []
    for i in range(0,len(AA),1):
        count_sketch = CountSketch(t, b, AA[i])
        for x, s in stream:
            count_sketch.update(x, s)
        X.append(count_sketch.estimate())
    Xe = np.mean(X)
    return X, Xe

