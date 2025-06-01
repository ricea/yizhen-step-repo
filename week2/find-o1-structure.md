# Data structure that can get / add / delete in O(1)

Intuitive:
a nested hash table, use different hash function to reduce duplication (the case 2 or more elements have same hash value)
we can hash the hash value again
Next:
have the input x, the hash value f(x):
