# hashtable and cache implementation

implement hashtable data structure and a least-recently-used cache from scratch using list and doubly linked lists in Python.

## project Structure

```
├── README.md                     # This file
├── hash_table.py                 # Custom hash table implementation
├── cache.py                      # LRU cache implementation
├── data-structure-for-cashe.md   # Design notes and algorithm explanation
├── tree-vs-hashtable.md          # Compare tree and hash table in real world production environment
├── find-o1-structure.md          # Find data tructure that performs real O(1) time
└── broccoli.my                   # A sliding window algorithm quiz
```

## project overview

**Key Features:**

- **O(1) access time** for cache operations (get, put, update)
- **O(1) eviction** of least recently used items
- **dynamic hash table** with automatic resizing

**Hash Table Performance:**

- Average case: O(1) for get/put/delete
- Worst case: O(n) during rehashing (amortized O(1))
- Load factor: 0.3 - 0.7 for optimal performance

## nown Issues

1. **Pointer Logic**: Current implementation has backwards linked list pointers
2. **Memory Leaks**: Hash table cleanup missing during eviction
3. **Edge Cases**: Missing null pointer checks in some methods

> Note:
> Those marked which 'after research' or similar words are implemented after look up resources
> I do search websites or ask AI for specific topics once hit the time limitation I set for myself to avoid perfectionism and use the whole week on it.
