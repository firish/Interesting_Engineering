### Starting with Cuckoo Hashing!?
# Invented by Rasmus Pagh and Flemming Friche Rodler in a 2001
# Cuckoo hashing is a scheme in programming for resolving hash collisions of values of hash functions in a table.
# IMP: Cuckoo hashing's worst-case lookup time is also constant. (CRAZY)

# The name derives from the behavior of some cuckoo species,
# where the cuckoo chick pushes the other eggs out of the nest.
# This behavior is referred to as "brood parasitism."

# Similarly, inserting a new key into a cuckoo hashing table may push an older key to a different location in the table.


### Operation / Algorithm
# Cuckoo hashing is a form of "open addressing" (see 1.)
# Every non-empty cell of a hash table contains a key
# A hash function is used to determine the location of each key and its presence in the table
# However, open addressing suffers from collisions when more than one key is mapped to the same cell.

# The basic idea of cuckoo hashing is to resolve collisions by using two hash functions instead of only one.
# This provides two possible locations in the hash table for each key. 
# In one of the commonly used variants of the algorithm, 
# the hash table is split into two smaller tables of equal size, 
#, and each hash function provides an index into one of these two tables. 
# It is also possible for both hash functions to provide indexes into a single table.

# A typical start choice for the hash functions is universal hashing,
# provides a family of hash functions that are designed to be independent and uniformly distributed.
# h1(k) = ((a1.k + b1) mod p) mod m
# h2(k) = ((a2.k + b2) mod p) mod m
# where, a1, a2, b1, b2, are random coefficients, p is a large prime number, and m is the hash table size


### Lookup
# hash table T is divided into T1 and T2, with hash function h1, and h2.
# Lookup = T1[h1(x)] = x or T2[h2(x)] = x
# Worst case time is O(1)


### Deletion
# Deletion is performed in O(1) time since probing is not involved.


### Insertion
# 1. When inserting a new item with key 𝑥,
# the first step involves examining if slot h1(x) of table T1 is occupied.
# If it is not, the item is inserted in that slot.

# However, if the slot is occupied,
# the existing item x' is removed, and x is inserted in its place.
# Then x' is inserted into T2 by following the same procedure.
# The process continues until an empty position is found to insert the key.

# To avoid an infinite loop, a threshold Max-Loop is specified,
# If the number of iterations exceeds this fixed threshold,
# T1 and T2 are rehashed with new hash functions and the insertion procedure repeats.

# IMP (Theory)
# Insertions succeed in expected constant time,
# Even considering the possibility of having to rebuild the table,
# as long as the number of keys is kept below half of the capacity of the hash table (load factor < 0.50)

# IMP (Practice)
# In practice, cuckoo hashing is about 20–30% slower than linear probing, 
# which is the fastest of the common approaches.
# The reason is that cuckoo hashing often causes two cache misses per search,
# instead of 1 in linear probing, and does not get the benefit of the locality of reference like linear probing.
# However, the O(1) lookup time guarantee is stronger than linear probing, (does not need any kind of probing for lookup like linear probing)
# making Cuckoo hashing value for certain types of applications.



### No system design exists without trade-offs!
# There have been many variations to cuckoo hashing to try and improve load factor tolerance and reduce rehashing of the tables.
# The most famous one is to divide the hash table into 3 hash tables and use 3 hash functions
# This simple change increases load factor tolerance to 91%,
# but makes lookups and insertions slightly slower. 

# Another variation is a blocking cuckoo hashing
# Simply put, it involved dividing the hash table into b blocks and using b hash functions.
# Instead of hashing to a slot, the hash functions hash to a block (4, 8, 16, or so slots)
# The keys are hashed into blocks, and then we can use something like linear probing within the blocks
# For insertion, we hash into a block, and if it is full, we use the same cuckoo hashing principle

# Another variation of cuckoo hashing that has been studied is cuckoo hashing with a stash.
# The stash, in this data structure, is an array of a constant number of keys,
# used to store keys that cannot successfully be inserted into the main hash table of the structure.
# This modification reduces the failure rate of cuckoo hashing.
#  A stash can be used in combination with more than two hash functions or with blocked cuckoo hashing,
# to achieve both high load factors and small failure rates.
# However, larger stashes also mean slower searches for keys that are not present or are in the stash.



### Cuckoo Filter (AMQ)
# A cuckoo filter is a space-efficient probabilistic data structure that is used to test whether an element is a member of a set
# A query returns either "possibly in the set" or "definitely not in set".
# (IMP) A cuckoo filter can also delete existing items, which is not supported by Bloom filters.



### Algo
# A cuckoo filter uses a hash table based on cuckoo hashing to store the fingerprints of items
# The data structure is broken into buckets of some size 𝑏
# To insert the fingerprint of an item x, two potential buckets are calculated, h1(x) and h2(x)

# h1(x) = hash(x)
# h2(x) = h1(x) XOR hash(fingerprint(x))






