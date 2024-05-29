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

# stream = CreateStream(2**10,9)
# count = 0
# for item in stream:
#     count += 1
#     print(item)
# print(count)