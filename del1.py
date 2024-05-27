import time
import random

def gen_nbit_rand(n):
    return random.getrandbits(n)

def gen_nbit_rand_odd(n):
    return random.getrandbits(n) | 1

class Hash(object):
    @staticmethod
    def mulshift(a=0, l=0):
        def H(x):
            return (a * x) >> (64 -l)
        return H

    @staticmethod
    def mulmodprime(a=0, b=0, p=0, l=0):
        # if l % 2:
        #     return ((a * x + b) % p) & (2**l - 1)
        q = 89

        def f(x):
            y= (x & p) + (x >> q);
            if (y>=p):
                y-=p
            return y

        def H(x):
            y = f(x * a) + b
            if y >= p:
                y =- p 
            return y & ((2**l) - 1)
            # return ((a * x + b) % p) % 2**l 
        return H

class HashTable(object):
    def __init__(self, l, h=Hash.mulmodprime) -> None:
        self.h = h 
        self.size = 2**l 
        self.table = [None] * self.size

    def __getitem__(self, key):
        return self.table[self.h(key)]

    def __setitem__(self, key, value):
       self.table[self.h(key)] = value

    def __len__(self):
        return self.size
    
    def __delitem__(self, key):
        self.table[self.h(key)] = None

    def increment(self, key, d):
        item = self.table[self.h(key)]
        self.table[self.h(key)] = item + d if item else d

if __name__ == "__main__":
    import create_stream


    gen_nbit_rand(256)

    # l = random.randint(0,64)
    l = 32
    n = 2**10
    p = 2**89 - 1
    a1 = 0b0111010010101101000111010010111100001011001110100011101100001111
    a2 = 0b0111010010101101000111010010111100001011001110100011101100001110 
    b = 0b1000111011010111000110101111000100001011001110001010110111101010
    sum_mulshift_hash = 0
    sum_mulmodprime_hash = 0
    
    time_mulshift_hash = 0
    time_mulmodprime_hash = 0

    test_stream = create_stream.CreateStream(n, l)
    
    time_mulmodprime_hash = time.time()
    for i in test_stream:
        sum_mulmodprime_hash += Hash.mulmodprime(a2, b, p, l)(i[0])
    time_taken_mulmodprime_hash = time.time() - time_mulmodprime_hash

    time_mulshift_hash = time.time()
    for i in test_stream:
        sum_mulshift_hash += Hash.mulshift(a1, l)(i[0])
    time_taken_mulshift_hash = time.time() - time_mulshift_hash


    print(f"Time Taken mulmodprime: {time_taken_mulmodprime_hash:.7f}")
    print(f"Time Taken mulshift: {time_taken_mulshift_hash:.7f}")

    t = HashTable(l, Hash.mulmodprime(a2, b, p, l))
    t_test_key = random.randint(0,100)

    t[t_test_key] = random.randint(0,100)
    

    print("T initial value", t[t_test_key])
    t.increment(t_test_key, 1)
    print("T increment", t[t_test_key])
