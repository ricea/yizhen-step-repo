# browser cache implementation

## requirements:

- input: (url,page)
- actions:
  search if url exists
  - if url not exists, remove the oldest (url,page) in cache, then add the input to the most top
  - if url already in the cache, move that (url,page) to the top

## intuitive:

I head thought of queue, which allows we implement head-in-head-out, fixed size, enqueue / dequeue with O(1)

## try to implement:

After searching, I found **circular array implementation of queue**
It allows us perform pop(0) in O(1) with 2 pointers keep watching the head and tail of a queue, and move as elements changing

**example:**

```
initial:
[A, B, C, D]
 F        L
after enqueue E and dequeue A:
[E, B, C, D]
 L  F
```

**dequeue and enqueue:**

```python
self.queue[F] = None
L = F
F = (F + 1)%len(self.queue)
# F: 0 -> 1

# enqueue when it's not filled:
L+=1
```

## find problem after searching:

- A queue usually cannot bubble an element from middle of the queue to the top with O(1) time
- Data structures with nodes can change order/ relation surrond a single element with O(1)
- To change order with O(1), we need to store the prev and next node

## two way linked list

- How to access each node without loop from head / tail:
  - we store the address of node in hash table
  - each node contains url, content, prev node, next node
- how we get node:
  - url -> hashvalue -> idx of hash tbale -> bucket: key: url value: node
  - after accessing the node, we manipulate the pointers to put it on the head of linked list

### to add new to head and remove tail:

- move self.head to point to the new head
- move the tail second node (new tail)'s prev to point to None, and move self.tail to point to the new tail

### to get pages in most recent order:

- loop through linked list from head until reach tail
