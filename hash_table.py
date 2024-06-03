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
                y -= p
            return y

        def H(x):
            y = f(x * a) + b
            if y >= p:
                y -= p 
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
            enumerator: Object enumerating over hash table.
        """
        # return enumerate(self.table)
        return enumerate([i for ll in self.table for i in ll])
    
    def __contains__(self, key):
        """
        Checks if the given key is present in the hash table can be used with the `in` keyword.

        Args:
            key: The key to look up.

        Returns:
            bool: `True` if the given key is present, otherwise `False`.

        """
        # return bool(self.table[self.h(key)])
        bucket = self.table[self.h(key)]
        for _, (k, _) in enumerate(bucket):
            if k == key:
                return True
        return False


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
