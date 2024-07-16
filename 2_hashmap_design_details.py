########################################## MEASURING HASH TABLE PERFORMANCE ######################################
# An important metric of every hash table is the "LOAD FACTOR"
# Load Factor (alpha) = n/m, where n is the no of elements in the table, and m is the total available slots

## Time to resolve conflict
# In chaining, 
# alpha = the average number of elements per linked list
# time to resolve conflict = O(alpha + 1)  (alpha for traversing the linked list and 1 for adding the node) 

# In open addressing,
# With linear/quad probing and double hashing, the calculation of an exact time complexity is not practical
# However, researchers approximate that as number of elements in the arr/table increases, the number of probes
# (and subsequently) time to resolve conflict increases in an "exponential" manner
# Also, linear probing has the worst performance and double hashing has a relatively better performance 
# worst case would be O(m), assuming no infinite loops

## Cost of probing
# In chaining,
# cost of probing is high
# We use an arr of linked list heads, so we have to traverse the nodes of the linked list to find the key (linear traversal)
# Plus, it is not CPU cache friendly, as linked lists and trees are typically stored in a fragmented manner
# so we don't get any "locality of reference" benefits

# In open addressing
# Linear and quadratic hashing benefit from "locality of reference"
# For double hashing the cost is again high,
# as little to no "locality of reference" benefit plus CPU intensive as two hash functions need to be computed per key per attempt

########################################## BENCHMARKING HASH TABLE PERFORMANCE ######################################
# hence, there is no one good hash table strategy
# We have to choose the right strategy based on our use case
# The easiest way to do this is to use all the strategies for our case, compare the results, and choose the best one

# A standard benchmark test is,
# "LOOKUP TIME AS A FUNCTION OF INCREASING LOAD"

# 1. Create a hash table of size 1024
# 2. Insert n elements varying from 32 to 900
# 3. Lookup 1000 keys (keep a high miss ratio)

# General heuristics state that,
# 1. Performance for open addressing degrades quickly as alpha nears 1 (arr is getting full)
# 2. Chained approach degrades more gracefully (slow degradation in performance)
# 3. In open addressing, Linear Probing would almost always be slower than double-hashing
# 4. In open addressing, Probes will be shorter in double hashing
# 5. We can not generalize chained > open addressing as chained is not caching-friendly 
# 6. Cache friendliness becomes important when the arr/table size grows huge


########################################## OPTIMIZING CHAINING?  ######################################
# A major drawback of chained hashing is that we can not leverage the CPU cache with it
# We change chaining to be,
# An array, where every node is the head of a linked list,
# and every subsequent node in each linked list is an arr of fixed size (say 16 elements)
# This allows us to leverage the CPU cache while traversing linked lists

# NOTE: Even with this optimization,
# Chaining will be generally better for smaller arr sizes, and open addressing for larger arr sizes
# But this optimization helps to bridge the gap


########################################## HASH TABLE RESIZING  ######################################
# It is known that the performance of the hash table decreases as the table load factor increases
# So, we need to resize after a certain threshold
# However, resizing is very expensive, as we have to move a lot of keys to different indexes (as hash/prob functions will change to reflect the new size)
# A common threshold is, alpha = 0.5
# A common size increase strategy is to double the size of the current table/arr

# Q: Why do we always/mostly double the size?
# A: If we just increased the size of arr by 1 each time a key is added, 
# for creating a new array, copying the elements, and adding the element, 
# the time complexity for n operations will be O(n2) 

# Now, assume every time the arr is filled, we double the arr
# The time complexity for n operations will be O(n)

# INTERESTING!
# Q: Why is hash table size always a power of 2?
# A: Hash functions use the mod operation to bind the output to the size of the arr/table
# but for the CPU, a mod operation is expensive, as it needs to perform a long division to calculate the mod function
# To do better we exploit a formula of bitwise operations
# IMPORTANT: [number % m] = [number AND m-1] ..... WHERE m is a power of 2
# The bitwise AND is faster than mod and that's how we can speed up the hashing significantly by making sure hash table size m is a power of 2

# To keep exploiting this optimization
# hash table size is a power of 2, and when it needs to be increased, it is DOUBLED

# Q: When do we SHRINK the hash table/arr?
# A: by simple reverse engineering, if we follow the above good practice,
# if hash table size is n, it would have at max n/2 elements (load factor is 0.5)
# if we shrink it and reduce it by a factor of 2, it would have n/2 slots
# and hence should have at max n/4 elements
# but if we resize at n/4 - 1 elements, just 1 insertion will cause a resize again, and that will be poor design,
# so we go one more step back and reduce by a factor of 2 to n/8 elements
# hence the most common shrink condition is, alpha < 12.5% 


##################################### (CAN IGNORE) MY IMPLEMENTATION #################################
class Dict:
    def __init__(self, size=10):
        self.size = size
        self.count = 0
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def check_load_factor_and_resize(self):
        # Grow the table
        if self.count > 0.67 * self.size:
            self.resize(self.size * 2)
        # Shrink the table
        elif self.count < 0.125 * self.size and self.size > 10:
            self.resize(self.size // 2)

    def insert(self, key, value):
        self.check_load_factor_and_resize()
        index = self.hash_function(key)
        bucket = self.table[index]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket[i] = (key, value)  # Update existing key
                return
        bucket.append((key, value))  # Insert new key
        self.count += 1

    def delete(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                del bucket[i]  # Delete the key-value pair
                self.count -= 1
                self.check_load_factor_and_resize()
                return True
        return False  # Return False if the key was not found

    def get(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]

        for kv in bucket:
            if kv[0] == key:
                return kv[1]
        raise KeyError(f"Key not found: {key}")

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        if not self.delete(key):
            raise KeyError(f"Key not found: {key}")

    def __repr__(self):
        return '{' + ', '.join(f'{k}: {v}' for bucket in self.table for k, v in bucket) + '}'
