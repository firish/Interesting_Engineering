### What in the world is a quotient filter?
# A quotient filter is a space-efficient probabilistic data structure,
# that is used to test whether an item is a member of a set. 

### Characteristics
# The quotient filter will always say yes if an item is a set member. 
# However, the quotient filter might still say yes although an item is not a member of the set.
# Just like a bloom filter, a quotient filter has FALSE POSITIVES.
# The filter will however always say no, when an element is not present in the set. This is definitive.

# Note:
# A common trade-off is space vs false positivity rate. (Inversely proportional)


### Addressing the Elephant in the room
### If we have a Bloom Filter, do we even need a Quotient Filter?
# The answer is yes.
# The biggest fault with a bloom filter is that it does not support delete operations,
# Without complications like a composite filter (costing space, increasing complexity, and introducing False Negatives)
# With quotient filters, we can support "DELETE ELEMENTs" operation

# This makes this filter brilliant for operations like, "DATABASE PROXY"
# Going to a database and checking if the key exists, takes time. 
# Hence a quotient filter acts as a database proxy, and only if the filter says that the key (possibly) exists,
# Do we make the expensive call that goes to the database.
# If the filter returns absence, the key is known not to be in the database without any disk accesses having been performed.
# This can't be done simply with a bloom filter as database keys, may get "added" and "deleted" frequently.
# hence the ability to support these operations is extremely beneficial.


# IMPORTANT
# Second benefit, 
# A quotient filter "CAN BE RESIZED WITHOUT REHASHING"
# This is a second big benefit over a bloom filter, which would need expensive rehashing for resizing.
# This also avoids the need to access those keys from secondary storage, which is required for a bloom filter.


### Base Algorithm
# The quotient filter is based on a kind of hash table in which entries contain only a portion of the key plus some additional meta-data bits. 
# These bits are used to deal with the case when distinct keys happen to hash to the same table entry.

# In a quotient filter a hash function generates a p-bit FINGERPRINT. 
# The r least significant bits are called the REMAINDER.
# The q = p - r most significant bits is called the QUOTIENT, hence the name.
# The hash table/array has m=2^q slots.

# For some key d which hashes (single hashing function is used, unlike BF) to the fingerprint dH, 
# let its quotient be dQ and the remainder be dR. 
# QF will try to store the remainder (dR) in slot dQ, known as the CANONICAL slot.

# In simple terms,
# The quotient is used to identify the bucket position while the remainder gets stored in the bucket.


### What about Collisions?
# There are two types of collisions,
# HARD collisions - If multiple keys hash to the same fingerprint
# SOFT collisions - If the keys' fingerprints are distinct they can have the same quotient

# IMP: If the canonical slot is occupied then the remainder is stored in some slot to the right.
# The insertion algorithm ensures that all fingerprints having the same quotient are stored in contiguous slots.
# IMP: Such a set of fingerprints is defined as a RUN.

# More Important Terminology
# Note: A run's first fingerprint might not occupy its canonical slot if the run has been forced right by some run to the left.
# Note: However a run whose first fingerprint occupies its canonical slot indicates the start of a CLUSTER.
# The initial run and all subsequent runs comprise the cluster, which terminates at an unoccupied slot or the start of another cluster.


### The Meta-data bits!!!
# Three additional bits are used to reconstruct a slot's fingerprint. 
# 1. is_occupied - is set when a slot is the canonical slot for some key stored (somewhere) in the filter (but not necessarily in this slot).
# 2. is_continuation - is set when a slot is occupied but not by the first remainder in a run
# 3. is_shifted - is set when the remainder in a slot is not in its canonical slot.

# is_occupied - is_continuation - is_shifted          | Meaning
#    0        -         0       -      0              | Empty Slot
#    0        -         0       -      1              | Slot is holding the start of a run that has been shifted from its canonical slot.
#    0        -         1       -      0              | Not used
#    0        -         1       -      1              | Slot is holding continuation of run that has been shifted from its canonical slot.
#    1        -         0       -      0              | Slot is holding the start of a run that is in its canonical slot. This is also the start of the cluster.
#    1        -         0       -      1              | Slot is holding start of run that has been shifted from its canonical slot. Also the run for which this is the canonical slot exists but is shifted right.
#    1        -         1       -      0              | Not used
#    1        -         1       -      1              | Slot is holding continuation of run that has been shifted from its canonical slot. Also the run for which this is the canonical slot exists but is shifted right.



