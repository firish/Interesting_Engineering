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
# 1. is_occupied - is set when a slot is a canonical slot for some key stored (somewhere) in the filter (but not necessarily in this slot).
# 2. is_continuation - is set when a slot is occupied but not by the first remainder in a run
# 3. is_shifted - is set when the remainder in a slot is not in its canonical slot.

# is_occupied - is_continuation - is_shifted          | Meaning
#    0        -         0       -      0              | Empty Slot
#    0        -         0       -      1              | Slot is holding the start of a run that has been shifted from its canonical slot.
#    0        -         1       -      0              | Not used
#    0        -         1       -      1              | Slot is holding continuation of run that has been shifted from its canonical slot.
#    1        -         0       -      0              | Slot is holding the start of a run that is in its canonical slot. This is also the start of the cluster.
#    1        -         0       -      1              | Slot is holding the start of a run that has been shifted from its canonical slot. Also the run for which this is the canonical slot exists but is shifted right.
#    1        -         1       -      0              | Not used
#    1        -         1       -      1              | Slot is holding continuation of run that has been shifted from its canonical slot. Also the run for which this is the canonical slot exists but is shifted right.



### How to do a Lookup? 
# 1. We hash the key to produce its fingerprint, dH.
# 2. We separate the q significant bits to get the quotient dQ and the remainder dR.
# 3. Slot dQ is the key's canonical slot.
# 4. That slot is empty if its three meta-data bits are false. In that case, the filter does not contain the key.

# 5. If the canonical slot is occupied then we must locate the quotient's run. (the slots that hold remainders belonging to the same quotient)
# 6. To locate the quotient's run we must first locate the start of the cluster. 

# 7. Starting with the quotient's canonical slot we can scan left to locate the start of the cluster.
# 8. We scan left looking for a non-empty slot with is_shifted as false. This indicates the start of the cluster. (See table above)

# 9. Then we scan right (from the cluster) to locate the quotient's run's end.
# 10. We scan right keeping a running count of the number of runs we must skip over. (BECAUSE it is possible that the entire run has been shifted to the right by the encroachment from the left of another run/s).
# 11. Each slot to the right of the cluster and left of the canonical slot having is_occupied set,
#     indicates another run to be skipped, so we increment the running count.
# 12. Each slot having is_continuation clear indicates the start of another run, 
#     thus the end of the previous run, so we decrement the running count.
# 13. When the running count reaches zero, we will be scanning the quotient's run.

# 14. We can compare the remainder in each slot in the run with dR. 
#     If found, we report that the key is (probably) in the filter otherwise we report that the key is definitely not in the filter.


### Lookup Example
# consider, this quotient filter with 8 slots, and the three meta-data bits per slot
# (is_occupied, is_continuous, is_shifted)

#   000   100   111   011    101   001   000   100
# |_____|_aR__|_bR__|_cR___|_dR__|_eR__|_____|_fR___|

# Let's say we are hashing element e, which generates eQ=4 and eR, and we want to check if it exists in the filter.
# First, we see that index=4 is occupied.
# Next we have to look for the cluster head, so start scanning left.
# ind4 is shifted, ind3 is shifted, ind2 is shifted, ind1 is not shifted.
# So, ind1 is cluster start.
# Now, we start scanning right and maintaining the two counts, oc=occupied count, and cc=continous count, rc=running count (oc-cc).
# at ind1, oc=1, cc=0, rc=1.
# at ind2, oc



