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





