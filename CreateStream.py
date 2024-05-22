import random
from typing import Generator, Tuple

def create_stream(n: int, l: int) -> Generator[Tuple[int, int], None, None]:
    # We generate a random uint64 number.
    a = 0
    b = bytearray(8)
    rnd = random.Random()
    rnd.getrandbits(8 * 8).to_bytes(8, 'big')
    for i in range(8):
        a = (a << 8) + b[i]
    
    # We demand that our random number has 30 zeros on the least significant bits and then a one.
    a = (a | ((1 << 31) - 1)) ^ ((1 << 30) - 1)
    x = 0
    
    for i in range(n // 3):
        x += a
        yield ((x & (((1 << l) - 1) << 30)), 1)
    
    for i in range((n + 1) // 3):
        x += a
        yield ((x & (((1 << l) - 1) << 30)), -1)
    
    for i in range((n + 2) // 3):
        x += a
        yield ((x & (((1 << l) - 1) << 30)), 1)