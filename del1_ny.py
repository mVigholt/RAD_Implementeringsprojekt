import time
from create_stream import CreateStream
q = 89
l = 100
n = 2**(l*2)

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
#test(q, l)

#Opgave2
def hash_table():
    A = [ [] for _ in range(2**l) ]
    stream = CreateStream(n, l)

    for x,s in stream:
        #h = multiply_shift(x, l)
        h = multiply_mod_prime(x, q, l)
        add_h = True
        for i in range(0,len(A[h])):
            first, second = A[h][i]
            if (first == x):
                add_h = False
                A[h][i] = (x, s + second)
                exit
        if add_h:
            A[h].append((x,s))
    return A

#Opagve3
def square_sum(hash_table):
    sum = 0
    for linked_list in hash_table:
        for x, s in linked_list:
            sum += s
    return sum**2
square_sum(hash_table())