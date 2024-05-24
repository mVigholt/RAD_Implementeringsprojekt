import random

def gen_nbit_rand(n):
    return random.getrandbits(n)

def gen_nbit_rand_odd(n):
    return random.getrandbits(n) | 1


class Hash(object):
    @staticmethod
    def mulshift_hash(x, a=None, l=None):
        return (a * x) >> (64 -l)

    @staticmethod
    def mulmodprime_hash(x, a=None, b=None, p=None, l=None):
        # if l % 2:
        #     return ((a * x + b) % p) & (2**l - 1) 
        return ((a * x + b) % p) % 2**l 
    

if __name__ == "__main__":
    import create_stream


    gen_nbit_rand(256)

    l = random.randint(0,64)
    n = 100
    p = 2**89 - 1
    a1 = 0b0111010010101101000111010010111100001011001110100011101100001111
    a2 = 0b0111010010101101000111010010111100001011001110100011101100001110 
    b = 0b1000111011010111000110101111000100001011001110001010110111101010
    sum_mulshift_hash = 0
    sum_mulmodprime_hash = 0

    for i in create_stream.CreateStream(n, l):
        sum_mulshift_hash += Hash.mulshift_hash(i[0], a1, l)
        sum_mulmodprime_hash += Hash.mulmodprime_hash(i[0], a2, b, p, l)

    print(sum_mulshift_hash)
    print(sum_mulmodprime_hash)
