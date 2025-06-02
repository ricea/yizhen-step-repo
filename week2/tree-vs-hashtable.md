## Why real-world large-scale database systems tend to prefer a tree to a hash table

### performance:

- tree: O(log N)
- hashtable: O(1)
- hashtable has O(n) worst case (after research: this will cause unpredictable behaviour)(may lead to poor user experience), compare to stable behaviour of tree.

### accessibility:

- tree can be sorted,
- we may need to access associated values or similar values in production environment (like recommendation features)
- after research: tree fits the database query pattern better(allow query with value's range or )

### scalibility:

- tree is fractal structure, makes it easier to split into smaller ones and maintain the structure
- easy to deploy in a distributed way when scale up
- when hash table grows fast, it may trigger frequently rehash, each rehash takes O(n), and demands great amout of calculating. This may make system unstable

**after searching**

### concurrency:

- tree can handle multiple concurrent operation
- rehash will lock the whole structure
