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
which each non-empty cell of a hash table contains a key
