import random
import sys
import time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################


class Item:
    '''
    An item object that represents one key - value pair in the hash table.
    |key|: The key of the item. The key must be a string.
    |value|: The value of the item.
    |next|: The next item in the linked list. If this is the last item in the linked list, |next| is None.
    '''

    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


class HashTable:
    '''
    The main data structure of the hash table that stores key - value pairs.
    The key must be a string. The value can be any type.

    |self.bucket_size|: The bucket size.
    |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
                    stores a linked list of items whose hash value is |hash|.
    |self.item_count|: The total number of items in the hash table.
    '''

    def __init__(self):
        '''        
        Initialize the hash table.
        Set the initial bucket size to 97. A prime number is chosen to reduce hash conflicts.
        '''
        self.sizes = [97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869,
                      3145739, 6291469, 12582917, 25165843, 50331653, 100663319, 201326611, 402653189, 805306457, 1610612741]
        self.bucket_size_idx = 0
        self.bucket_size = self.sizes[self.bucket_size_idx]
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    def calculate_hash(self, key: str) -> int:
        '''
        TODO: why rolling hash? 
        Hash function.
        |key|: string
        Return value: a hash value

        self.bucket_size: modulo, should be a large prime number 
        p: a const prime number used to generate exponent
        pow: p**i
        '''
        assert type(key) == str

        p = 31
        hash = 0
        pow = 1
        for i in key:
            hash = (hash + (ord(i)-ord('a')) * pow) % self.bucket_size
            pow = pow*p % self.bucket_size
        return hash

    def put(self, key: str, value: any) -> bool:
        '''
        Put an item to the hash table. If the key already exists, the corresponding value is updated to a new value.
        |key|: The key of the item.
        |value|: The value of the item.
        Return value: True if a new item is added. False if the key already exists and the value is updated.
        seems it puts the newest item at the head of linked list
        '''
        assert type(key) == str
        self.check_size()

        self._check_rehash()

        bucket_index = self.calculate_hash(key)
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    def get(self, key) -> tuple[any, bool]:
        '''
        Get an item from the hash table.
        |key|: The key.
        Return value: If the item is found, (the value of the item, True) is returned. Otherwise, (None, False) is returned.
        TODO: Question: 
        why we return (None, False) instead of None?
        '''
        assert type(key) == str
        self.check_size()

        bucket_index = self.calculate_hash(key)
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    def delete(self, key: str) -> bool:
        '''
        Delete an item from the hash table.
        |key|: The key.
        Return value: True if the item is found and deleted successfully. False otherwise.
        '''
        assert type(key) == str

        self._check_rehash()
        bucket_index = self.calculate_hash(key)
        item = self.buckets[bucket_index]
        if item is not None:
            if item.key == key:
                self.buckets[bucket_index] = item.next
                self.item_count -= 1
                return True

            prev = None
            while item is not None:
                if item.key == key:
                    prev.next = item.next
                    self.item_count -= 1
                    return True

                prev = item
                item = item.next

        return False

    def _check_rehash(self) -> None:
        '''
        TODO: find bucket size
        size down if total usage is less than 0.3
        size up if total usage is over 0.7
        '''

        if self.bucket_size_idx > 0 and self.item_count <= self.bucket_size * 0.3:
            self.bucket_size_idx -= 1
            self._rehash()

        elif self.bucket_size_idx < len(self.sizes)-1 and self.item_count >= self.bucket_size * 0.7:
            self.bucket_size_idx += 1
            self._rehash()

    def _rehash(self) -> None:
        '''
        assign new bucket size, empty new buckets and initial count number to self
        make a copy of origin bucket
        '''
        origin_buckets = self.buckets

        self.bucket_size = self.sizes[self.bucket_size_idx]
        self.buckets = [None]*self.bucket_size
        self.item_count = 0
        for bucket in origin_buckets:
            item = bucket
            # iteratively rehash items in linked list to new table
            while item is not None:
                key, value = item.key, item.value
                bucket_index = self.calculate_hash(key)
                # check existing items in the same bucket
                new_item = Item(key, value, self.buckets[bucket_index])
                self.buckets[bucket_index] = new_item
                self.item_count += 1
                item = item.next

    def size(self) -> int:
        '''Return the total number of items in the hash table.'''
        return self.item_count

    def check_size(self):
        '''
        Check that the hash table has a "reasonable" bucket size.
        The bucket size is judged "reasonable" if it is smaller than 100 or the buckets are 30% or more used.
        Note: Don't change this function.
        '''
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


def functional_test():
    '''Test the functional behavior of the hash table.'''
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


def performance_test():
    '''
    Test the performance of the hash table.
    Your goal is to make the hash table work with mostly O(1).
    If the hash table works with mostly O(1), the execution time of each iteration should not depend on the number of items in the hash table. 
    To achieve the goal, you will need to 
    1) implement rehashing (Hint: expand / shrink the hash table when the number of items in the hash table hits some threshold) and
    2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
    '''

    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
