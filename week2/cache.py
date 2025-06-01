
import sys
from hash_table import HashTable, Item

'''
Implement a data structure that stores the most recently accessed N pages.
See the below test cases to see how it should work.

Note: Please do not use a library like collections.OrderedDict). The goal is to implement the data structure yourself!

observe the history, pick pages with higher probability
pick most recent x pages

requiremets:
input: (url,page)

implement a hash table with fixed size (X)
store the key value as <url, webpage> pair
be able to get time series order
    specifically, we want to know the key of the oldest one in O(1)
    intuitively, use something like a queue
    delete in list in O(1)(or pserform shift in O(1))
    use 2 pointers to keep watching head and tail in a fixed size queue
store the elem's idx in the queue in hashtable as well

Bubble the element to top: change node 
size limit: n
add: if items > n: remove and add
else: add
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
        first: the newest added node, 
        first's next is None
        last: the oldest node, which will be removed if new node comes in 
        last's prev is None
        '''
        self.limit = n
        self.first = None
        self.last = None
        self.count_item = 0

    def add_to_first(self, url: str, content: any) -> tuple[Node, bool]:
        '''
        create a new node 
        new node's prev is current first, next is None
        and add the new node to the first of linked list
        drop last if hit size limit
        '''
        new_node = Node(url, content, self.first, None)
        if self.count_item == 0:
            self.first = new_node
            self.last = new_node
        else:
            self.first.next = new_node
            self.first = new_node

        self.count_item += 1
        return (new_node, True)

    def remove_last(self) -> tuple[any, bool]:
        '''point the 'self.last' flag to the last second node, then drop the last item  '''
        if self.count_item < 1:
            return (None, False)
        removed_node = self.last
        self.last = self.last.next

        if self.last is not None:
            self.last.prev = None
        self.count_item -= 1
        return (removed_node, True)

    def move_to_first(self, exist_node: Node) -> tuple[Node, bool]:
        '''
        first: check if node is already first
        if not: 
            point current first's next to exist_node, 
            point exist_node's prev to current first,
            move self.first to exist_node
        '''
        if self.first is not exist_node:
            if exist_node.prev is not None:
                # when exist node is not self.last
                exist_node.prev.next = exist_node.next
            else:
                # when exist node is self.last(the oldest page), we change the self.last pointer
                self.last = exist_node.next
            exist_node.next.prev = exist_node.prev
            self.first.next = exist_node
            exist_node.prev = self.first
            self.first = exist_node
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

    def access_page(self, url, contents):
        '''
        Access a page and update the cache so that it stores the most recently
        accessed N pages. This needs to be done with mostly O(1).
        |url|: The accessed URL
        |contents|: The contents of the URL

        access in hash table, search if url exists
            if url not exists:
            remove the oldest (url,page) in cache, add the input to the most top
        '''
        item, found = self.hashtable.get(url)

        if found == True:
            self.doubly_linked_list.move_to_first(item)
            # if size limit:

        else:
            new_node, success = self.doubly_linked_list.add_to_first(
                url, contents)
            self.hashtable.put(url, new_node)
            if self.hashtable.size() > self.limit:
                self.doubly_linked_list.remove_last()

    def get_pages(self):
        '''    
        Return the URLs stored in the cache. 
        The URLs are ordered in the order in which the URLs are mostly recently accessed.
        '''
        pages = []
        item = self.doubly_linked_list.first
        while item is not None:
            pages.append(item.url)
            item = item.prev
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
