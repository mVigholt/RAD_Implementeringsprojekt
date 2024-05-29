import random
from typing import Generator, Tuple

def create_stream(n: int, l: int) -> Generator[Tuple[int, int], None, None]:
    random.seed(1)

    a = 0
    b = random.getrandbits(64)
    a = b
    
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

stream= create_stream(2**10,5)
for item in stream:
    print(item)