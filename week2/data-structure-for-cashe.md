# browser LRU cache implementation

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

**after searching:**

## improve code quality through reducing edge case:

- use dummy node to reduce edge case and make cleaner code
- before dummy node: I need a lof of conditional to handle when moving a tail node
- same thing apply to list, by adding float('inf') and float('-inf') to the sides

before:

```python
def move_to_head(self, exist_node: Node) -> tuple[Node, bool]:
        '''
        head: check if node is already head
        if not:
            point current head's next to exist_node,
            point exist_node's prev to current head,
            move self.head to exist_node
        '''
        if self.head is not exist_node:
            if exist_node.prev is not None:
                # when exist node is not self.tail
                exist_node.prev.next = exist_node.next
            else:
                # when exist node is self.tail(the oldest page), we change the self.tail pointer
                self.tail = exist_node.next
            exist_node.next.prev = exist_node.prev
            self.head.next = exist_node
            exist_node.prev = self.head
            self.head = exist_node
        return (exist_node, True)
```

## direction of doublt linked list:

- tail <-next- head -prev->None

## memory leak:

- when droping the tail, we should remove a node from both hash table and linked list
