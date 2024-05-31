import time
import random
from typing import Generator, Tuple

def CreateStream(n: int, l: int) -> Generator[Tuple[int, int], None, None]:
    seed = 13
    random.seed(seed)
    a = random.getrandbits(64)
  
    # We demand that our random number has 30 zeros on the least significant bits and then a one.
    a = (a | ((1 << 31) - 1)) ^ ((1 << 30) - 1)
    x = 0

    for i in range(n // 3):
        x = x + a
        yield (x & (((1 << l) - 1) << 30), 1)
    
    for i in range((n + 1) // 3):
        x = x + a
        yield (x & (((1 << l) - 1) << 30), -1)
    
    for i in range((n + 2) // 3):
        x = x + a
        yield (x & (((1 << l) - 1) << 30), 1)


def square_sums(stream, hash_table):
    # We create a HashTable object

    square_sums = 0 # A counter.

    for x, d in stream: # Told to look for each (x_n, d_n).
        hash_table.increment(x, d) # Increment should go through the linkedlist and add the value d for each x. If x is not found it will append (x,d).
    
    for _, linked_list in hash_table:
        square_sum_for_list = 0
        # print(linked_list)
        for _, current_sum in linked_list:
            square_sum_for_list += current_sum ** 2 # squares each of our current sum in the linked list.
        square_sums += square_sum_for_list # then we put this sum to our counter and return it.
    return square_sums





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
        q = 89

        def f(x):
            y= (x & p) + (x >> q)
            if (y>=p):
                y-=p
            return y

        def H(x):
            y = f(x * a) + b
            if y >= p:
                y =- p 
            return y & ((2**l) - 1)
        return H


class HashTable(object):
    def __init__(self, l, h=Hash.mulmodprime) -> None:
        self.h = h
        self.size = 2**l
        self.table = [[]] * self.size

    def __getitem__(self, key):
        for k, v in self.table[self.h(key)]:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        for i, (k, v) in enumerate(self.table[self.h(key)]):
            if k == key:
                self.table[self.h(key)][i] = (key, value)
                return
        self.table[self.h(key)].append((key, value))

    def __len__(self):
        return sum(len(bucket) for bucket in self.table)

    def __iter__(self):
        return enumerate(self.table)
    
    def __contains__(self, key):
      return bool(self.table[self.h(key)])

    def __delitem__(self, key):
        bucket = self.table[self.h(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
        raise KeyError(key)

    def increment(self, key, d):
        for i, (k, v) in enumerate(self.table[self.h(key)]):
            if k == key:
                self.table[self.h(key)][i] = (k, v + d)
                return
        self.table[self.h(key)].append((key, d))





if __name__ == "__main__":


    gen_nbit_rand(256)

    l = 18
    n = 2**10
    p = 2**89 - 1
    a1 = 0b0111010010101101000111010010111100001011001110100011101100001111
    a2 = 0b0111010010101101000111010010111100001011001110100011101100001110 
    b = 0b1000111011010111000110101111000100001011001110001010110111101010
    sum_mulshift_hash = 0
    sum_mulmodprime_hash = 0
    
    time_mulshift_hash = 0
    time_mulmodprime_hash = 0

    test_stream = list(CreateStream(n, l)) # Contributes to yield in Creatstream not being consumed at first usage, such that we put each of these yield-results in a list.
    
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

    test_hash_table = HashTable(l, Hash.mulmodprime(a2,b,p,l)) # We initiate our hashtable which should hash each element. 
    S = square_sums(test_stream, test_hash_table) # We test our squaresum function on the hashtable with correlation to our stream.

    print(S)


    # Opgave 3 

# DONT DELETE CODE BELOW, OUTCOMMENT IT INSTEAD!!!!
"""
    new_l = 64
    while True:
        try:
            t = HashTable(new_l, Hash.mulmodprime(a2, b, p, l))
        except MemoryError:
            print("MemError L: ", new_l)
            new_l -= 1
            continue
        except OverflowError:
            print("OverflowError L: ", new_l)
            new_l -= 1
            continue
        break
    print("Found L", new_l)

"""

