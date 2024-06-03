import time

import numpy as np
import matplotlib.pyplot as plt

from hash_table import Hash, HashTable
from create_stream import CreateStream
from count_sketch import GenerateCountSketch


def square_sums(stream, hash_table):
    # We create a HashTable object
    square_sums = 0 # A counter.

    for x, d in stream: # Told to look for each (x_n, d_n).
        hash_table.increment(x, d) # Increment should go through the linkedlist and add the value d for each x. If x is not found it will append (x,d).
    
    for _, i in hash_table:
        square_sums += i[1] ** 2
    return square_sums

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
    print("\n\n--- INITIALIZING VALUES ---\n\n")
    
    q = 89
    l = 18
    t = 18
    n = 2**l
    m = 2**t
    p = 2**89 - 1
    a1 = 0b0111010010101101000111010010111100001011001110100011101100001111 & ((2**64)-2)
    a2 = 0x9b0082714fe482d8b65b5e50 & p  
    b = 0xe9be939cd923d0df0b226526 & p

    print('q = {}'.format(q)) 
    print('l = {}'.format(l))
    print('t = {}'.format(t))
    print('n = {}'.format(n))
    print('m = {}'.format(m))
    print('p = {}'.format(p))
    print('a1 = {}'.format(a1))
    print('a2 = {}'.format(a2))
    print('b = {}'.format(b))

    print("\n\n")
    print("--------------")
    print("--- PART 1 ---")
    print("--------------")
    print("--  TASK 1 --\n\n") 


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
    print(f"Sum mulmodprime: {sum_mulmodprime_hash}")
    print(f"Time Taken mulshift: {time_taken_mulshift_hash:.7f}")
    print(f"Sum mulmodprime: {sum_mulshift_hash}")

    print("\n--------------")
    print("-- TASK 2 --\n\n")

    # Un-comment this part to test for all values of 

    # S = None 
    # for l in [16, 18, 20, 24]:
    #     print("----------------------------------------")
    #     print("l =", l)
    #     print("----------------------------------------")
    #     print("\n\n")
    #     test_stream = list(CreateStream(n, l)) # Contributes to yield in Creatstream not being consumed at first usage, such that we put each of these yield-results in a list.
    #     test_hash_table = HashTable(l, Hash.mulmodprime(a2, b, p, l)) #Hash.mulmodprime(a2,b,p,l)) # We initiate our hashtable which should hash each element.
    #     
    #     # test_hash_table = HashTable(l, Hash.mulshift(a1, l))

    #     # Opgave 3
    #     square_sums_timer = time.time()
    #     S = square_sums(test_stream, test_hash_table)
    #     square_sums_timer_delta = time.time() - square_sums_timer

    #     print("Time S", square_sums_timer_delta)

    #     print('n = {}'.format(n))
    #     print('l = {}'.format(l)) 
    #     print("\nExpectation:")
    #     print('E[x] = S = {}'.format(S))       
    #     print('Var[X] = 2*S**2/m = ',2*S**2/m)

    print("Conducting tests for hashing with chaining:")
    print("Generating hash table... wait a second please...")

    test_hash_table = HashTable(l, Hash.mulshift(a1, l))
    square_sums_timer = time.time()
    S = square_sums(test_stream, test_hash_table)
    square_sums_timer_delta = time.time() - square_sums_timer

    print("\nExpectation:\n")
    print('   S = {}'.format(S))       
    print('   2*S**2/m = ',2*S**2/m)

    print("\n")
    print("--------------")
    print("--- PART 2 ---")
    print("--------------")
    print("--  TASK 8 --") 

    count_sketch_time_start = time.time()
    X, Xe  = GenerateCountSketch(test_stream, t, q)
    count_sketch_time_delta = time.time() - count_sketch_time_start
    
    # Calculate mean square error
    mse = np.mean([(xi - S) ** 2 for xi in X])

    print("\nEstimation:")
    print('   Time taken to generate count sketch', count_sketch_time_delta)
    print("   Time taken to generate hash table with chaining", square_sums_timer_delta)
    print('   E[X] =', Xe)
    print('   Var[X] =', mse)

    print("\nPlotting graph") 

    plot(X, S)

    print("\n----------------------")
    print("DONE -- MISSION COMPLETE - WE GOT EM")
    print("----------------------")


# DONT DELETE CODE BELOW, OUTCOMMENT IT INSTEAD!!!!
# We have created the following code to estimate the amount of memory 
#   we can work with before the program starts to error by allocating
#   a large array and seeing if it generates any errors
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


