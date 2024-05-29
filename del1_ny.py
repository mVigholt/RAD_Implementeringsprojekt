import numpy as np
import time
from create_stream import CreateStream
q = 89
n = 2**20
l = 11

#Opgave1
#a)
def multiply_shift(x, l):
    a = 0xbe457450e667e943 & 0x1FFFFFFFFFFFFFFF
    return (a * x) >> (64 -l)

#b)
def multiply_mod_prime(x, q, l):
    p = 2**q - 1
    a = 0x579a66a9030f158bb0fe1e9e & p
    b = 0xe4f64a81b0b65822808f0cae & p

    def f(x):
        y = (x & p) + (x >> q)
        if (y>=p):
            y-=p
        return y

    y = f(x * a) + b
    if y >= p:
        y =- p 
    return y & ((2**l) - 1)

#c)
def test(q, l):
    A = 0
    B = 0
    stream = CreateStream(n, l)
    timeStart = time.time()
    for x, s in stream:
        A += multiply_shift(x, l)
    lap = time.time() - timeStart
    print("multiply_shift sum: {}\ntime: {}\n".format(A, lap))
    
    stream = CreateStream(n, l)
    timeStart = time.time()
    for x, s in stream:
        B += multiply_mod_prime(x, q, l)
    lap = time.time() - timeStart
    print("multiply_mod_prime sum: {}\ntime: {}\n".format(B, lap))

test(q, l)

#Opgave2