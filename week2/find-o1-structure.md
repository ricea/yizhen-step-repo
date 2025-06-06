# Data structure that can search / insert / delete in O(1)

> question: Is there a data structure where searches, additions, and deletions can always be done in O(1)?

### Intuitive:

hash table has the limitation of worst case O(n) time, despite amorized O(1)

**skratch ideas**

- 1: To reduce collision in buckets I naturally think of
  a **nested hash** or a hash table **nested with BST** table to get more space with shorter probe length.

  - but mathematically, we need to infinitly nested structures if there are many elements, which lead to O(log n) (**trie**)

- 2: Use different hash function to reduce duplication (the case 2 or more elements have same hash value). such as hashing the hash value again
  - have the input x, the hash value f(x), when we find the destiny bucket already has element, we jump to next until find an empty bucket
    such as hash the hash value again and revord the trace(like how many times we've hashed)in some ways

**after searching:**

By searching, I found Robin Hood hashing
for dynamic data(we can not predict the amout and distribution), generally it's hard to find a perfect way, and for many approaches, the query time has a trade off of update time

Another direction: What if we have finit number of data?

So generally we can think of problem following below path:

## category by data type:

### Dynamic

#### open addressing hashing technique

- With n buckets and m (m > n) amout data, there must be extra spaces needed
- So how do we allocate this spcace to achieve smaller **probe length**?

##### nest with other data type

- for standart hash table, linked list has O(n) to look up. So we can use tree like structures

##### open addressing thechniques

We can have multiple hash functions, split hash table to swap data directions as so on to maintain a flat shape of hash table(s)

- Robin hood hashing
- Cuckoo hashing

### Static

- theoritically we can achieve O(1) lookup, insert, update, delete
- perfect hashing

#### topics to learn further:

- cache performances, cache-friendly data structures
- cell probe model
- logarithmic barrier
- pigeonhole principle

## How to choose:

it depends on the use case. We can consider below aspects:

- the shape of data we want to store

  - nested data and flat data may require different ways

- the operation we want to perform

  - open addressing thechniques are good for look up, and gets complex when inserting data. Maintaining the probe chain may get complex as well

- priority:
  - insertion frequency
  - space efficiency
  - easily maintain
