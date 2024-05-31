import time
import random
from matplotlib import test

import numpy as np
import matplotlib.pyplot as plt

from typing import Generator, Tuple
from create_stream import CreateStream

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

# def gen_nbit_rand(n):
#     return random.getrandbits(n)

# def gen_nbit_rand_odd(n):
#     return random.getrandbits(n) | 1

class Hash(object):
    """ 
    A utility class that provides hash functions for use in a hash table implementation.

    The `Hash` class uses decorators to allow the hash functions to be instantiated without needing to calculate the hash of the input value. This is achieved by using higher-order functions that return the actual hash function.
    
    Examples:
        >>> # Using the mulshift hash function
        >>> h = Hash.mulshift(a=123, l=8)
        >>> value = h(213412341234)

        >>> # Using the mulmodprime hash function
        >>> h = Hash.mulmodprime(a=456, b=789, p=1009, l=10)
        >>> value = h(130812039812)

    """
    @staticmethod
    def mulshift(a: int, l: int):
        def H(x):
            return ((a * x)&0xFFFFFFFFFFFFFFFF) >> (64 -l)
        return H

    @staticmethod
    def mulmodprime(a: int, b: int, p: int, l: int):
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
    """
    A hash table implementation, designed to be a drop in replacement for the standard python `Dict`.

    Attributes:
        h (callable): A hash function that takes a key and returns an index within the table.
        size (int): The size of the hash table.
        table (list): The underlying list that stores the key-value pairs.

    Methods:
        __getitem__(key): Retrieves the value associated with the given key.
        __setitem__(key, value): Assigns the given value to the specified key.
        __len__(): Returns the total number of key-value pairs in the hash table.
        __iter__(): Allows the hash table to be iterated over.
        __contains__(key): Checks if the given key is present in the hash table.
        __delitem__(key): Removes the key-value pair associated with the given key.
        increment(key, d): Increments the value associated with the given key by the specified amount.

    Examples:
        >>> ht = HashTable(4, Hash.mulmodprime(1,2,3,4))
        >>> ht[234234234] = 5
        >>> ht[234098233] = 10
        >>> len(ht)
        2
        >>> ht[234234234]
        5
        >>> 234234234 in ht
        True
        >>> del ht[234098233]
        >>> len(ht)
        1
    """
    def __init__(self, l, h=Hash.mulmodprime) -> None:
        """
        Initializes a new HashTable instance.

        Args:
            l (int): The base-2 logarithm of the desired hash table size.
            h (callable, optional): A hash function that takes a key and returns an index within the table. Defaults to Hash.mulmodprime.
        """
        self.h = h
        self.size = 2**l
        self.table = [[] for i in range(self.size)]

    def __getitem__(self, key): 
        """
        Retrieves the value associated with the given key, while allowing for use with standard python dict syntax.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the given key.

        Raises:
            KeyError: If the key is not found in the hash table.

        """
        for k, v in self.table[self.h(key)]:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Assigns the given value to the specified key, allowing for use with standard python dict syntax.

        Args:
            key: The key to look up.
            value: The value associated with the given key.

        Returns:
            None
        """
        for i, (k, v) in enumerate(self.table[self.h(key)]):
            if k == key:
                self.table[self.h(key)][i] = (key, value)
                return
        self.table[self.h(key)].append((key, value))

    def __len__(self):
        """
        Returns the total number of key-value pairs in the hash table, can be used with the standard `len` function.

        Returns:
            int: The total number of key-value pairs in the hash table.  
        """

        return sum(len(bucket) for bucket in self.table)

    def __iter__(self):
        """
        Allows the hash table to be iterated over with standard python syntax `for i in HashTable`.

        Returns:
            enumerator: Object enumerating over hash table for each hashed key, linked_list.  
        """
        return enumerate(self.table)
    
    def __contains__(self, key):
        """
        Checks if the given key is present in the hash table can be used with the `in` keyword.

        Args:
            key: The key to look up.

        Returns:
            bool: `True` if the given key is present, otherwise `False`.

        """
        return bool(self.table[self.h(key)])

    def __delitem__(self, key):
        """
        Removes the key-value pair associated with the given key.

        Args:
            key: The key to delete.

        Returns:
            None

        Raises:
            KeyError: If the key is not found in the hash table.
        """

        bucket = self.table[self.h(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
        raise KeyError(key)

    def increment(self, key, d: int):
        """
        Increments the value associated with the given key by the specified amount.

        Args:
            key: The key to delete.
            d (int): Amount to increment value associated to `key` by.

        Returns:
            None
        """
        for i, (k, v) in enumerate(self.table[self.h(key)]):
            if k == key:
                self.table[self.h(key)][i] = (k, v + d)
                return
        self.table[self.h(key)].append((key, d))

#Opgave 7 
def hashing_parameters(path):
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

def compute_X(n, l, b, path="./RandomHex.txt"):
    AA = hashing_parameters(path)
    X = []
    for i in range(0,len(AA),1):
        stream = CreateStream(n, l)
        count_sketch = CountSketch(l, b, AA[i])
        for x, s in stream:
            count_sketch.update(x, s)
        X.append(count_sketch.estimate())
    return X

def plot(X, S):
    Xx = list(range(1,101))
    Xy = sorted(X, key=lambda x: x, reverse=False)

    plt.plot(Xx, Xy, '.', label='X')

    M = []
    for i in range(0,99,11):
        G = []
        for j in range(0,11):
            G.append(X[i+j])
        G.sort(key=lambda x: x, reverse=False)
        M.append(G[5])
    Mx = list(range(6,100,11))
    My = sorted(M, key=lambda x: x, reverse=False)
    plt.plot(Mx, My, '.', label='M')
    
    plt.plot([1,100], [S,S], label='S')

    plt.legend(loc = 'upper left')
    plt.show()

if __name__ == "__main__":
    # Biggest possible value of `l`, that we could find before freezing runtime.
    q = 89
    l = 15
    n = 2**l
    m = 2**l
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

    test_hash_table = HashTable(l, Hash.mulmodprime(a2, b, p, l)) #Hash.mulmodprime(a2,b,p,l)) # We initiate our hashtable which should hash each element. 
    #test_S = square_sums(test_stream, test_hash_table) # We test our squaresum function on the hashtable with correlation to our stream.

    #print("Testing square sums function:", test_S)

    # Opgave 3

    # -----------------------

    # Count sktech tests 

    a0 = 0x478ad369f6852eac0de7ccf7
    a1 = 0xd472f7b830cf473f771bf810
    a2 = 0x695b4252f2c52ba0031649c4
    a3 = 0xd4e0ab8bb4907f43b1ede881
    A = [a0,a1,a2,a3]

    # Example
    # t = 16  # Example t value (log2(m))

    count_sketch = CountSketch(l, q, A)

    # Generate stream and update sketch
    for x, s in test_stream:
        count_sketch.update(x, s)

    # Estimate the sum of squared counts
    estimate = count_sketch.estimate()
    print("Estimate:", estimate)

    # -------------------

    S = square_sums(test_stream, test_hash_table)
    print('n = {}'.format(n))
    print('l = {}'.format(l)) 
    print('S = {}'.format(S))       
    print('Var[X]:',2*S**2/m)

    X = compute_X(n, l, q)
    # Calculate mean square error
    mse = np.mean([(xi - S) ** 2 for xi in X])

    print('Mean Square Error:', mse)

    plot(X, S)


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


