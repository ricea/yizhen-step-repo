
import sys
from hash_table import HashTable

'''
Implement a data structure that stores the most recently accessed N pages.
See the below test cases to see how it should work.

Note: Please do not use a library like collections.OrderedDict). The goal is to implement the data structure yourself!
'''


class Node:
    def __init__(self, url: str, content: any, prev: any, next: any):
        self.url = url
        self.content = content
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    def __init__(self, n: int):
        '''
        head: the newest added node, most recently accessed
        head's next is None
        tail: the oldest node, which will be removed if new node comes in 
        tail's prev is None
        '''
        self.limit = n
        self.head = Node('dummy', None, None, None)
        self.tail = Node('dummy', None, None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.count_item = 0

    def add_to_head(self, url: str, content: any) -> tuple[Node, bool]:
        '''
        create a new node 
        and add the new node to the head of linked list
        '''
        new_node = Node(url, content, self.head, self.head.next)
        self.head.next.prev = new_node
        self.head.next = new_node
        self.count_item += 1
        return (new_node, True)

    def remove_tail(self) -> tuple[any, bool]:
        '''
        point the 'self.tail' flag to the tail second node, then drop the tail item 
        the node should also be removed from hash map
        '''
        if self.count_item < 1:
            return (None, False)
        removed_node = self.tail.prev
        self.tail.prev = self.tail.prev.prev
        self.tail.prev.next = self.tail

        self.count_item -= 1
        return (removed_node, True)

    def move_to_head(self, exist_node: Node) -> tuple[Node, bool]:
        '''
        head: check if node is already head
        if not: 
            connect point exist_node's prev and next, 
            move exist_node to next of self.head 
            change previous first node's prev to exist_node
            change self.head's next to exist_node
        '''
        if self.count_item < 1:
            return (None, False)
        if self.head.next is exist_node:
            return (exist_node, True)

        exist_node.prev.next = exist_node.next
        exist_node.next.prev = exist_node.prev

        exist_node.prev = self.head
        exist_node.next = self.head.next
        exist_node.next.prev = exist_node
        self.head.next = exist_node

        return (exist_node, True)


class Cache:
    def __init__(self, n):
        ''' 
        Initialize the cache.
        |n|: The size of the cache.
        '''
        self.limit = n
        self.doubly_linked_list = DoublyLinkedList(n)
        self.hashtable = HashTable()

    def access_page(self, url, contents) -> None:
        '''
        Access a page and update the cache so that it stores the most recently
        accessed N pages. This needs to be done with mostly O(1).
        |url|: The accessed URL
        |contents|: The contents of the URL

        access in hash table, search if url exists
            if url not exists:
            add the input to the most top
            drop current tail (the oldest (url,page) in cache) if hit size limit
        '''
        item, found = self.hashtable.get(url)

        if found == True:
            self.doubly_linked_list.move_to_head(item)

        else:
            new_node, success = self.doubly_linked_list.add_to_head(
                url, contents)
            if success == True:
                self.hashtable.put(url, new_node)
                if self.hashtable.size() > self.limit:
                    removed_node, success = self.doubly_linked_list.remove_tail()
                    if success == True:
                        self.hashtable.delete(removed_node.url)

    def get_pages(self) -> list[str]:
        '''    
        Return the URLs stored in the cache. 
        The URLs are ordered in the order in which the URLs are mostly recently accessed.
        '''
        pages = []
        item = self.doubly_linked_list.head.next
        while item is not None:
            pages.append(item.url)
            item = item.next
        pages.pop()
        return pages


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
