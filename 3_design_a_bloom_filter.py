### What the fuck is a Bloom Filter?
# Bloom Filter is basically used to check whether an element is a part of a set. Thats it.

# Typically, hashmaps, and sets would suffice for this, as they both offer (almost) an constant time lookup.
# However, this problem becomes very tricky at scale.
# Like gmail checking if an email already exists
# Or checking if a webpage exists in the DNS cache
# both of these have hundreds of millions of elements that are a part of the membership set,
# and in such cases, we can do better than a set/dict.


### What the fuck is the problem with a set/dict?
# How is a set implemented?
# Most languages internally implement a set as a hashmap, or a balanced-binary tree,
# behind-the-scenes, hashmaps, might also use linked lists, or balanced trees (chaining), to store data.
# For both of these, 1 node will be roughly 12 bytes, 4 for data, and 4 as meta-data (left, right pointers for a tree, and prev, next for a linked list)
# So for storing a million keys, the data will be 12MB, where 8MB is just metadata.
# This problem becomes worse with an increasing number of keys.


### When storage is so cheap, is this even a problem?
# Absolutely yes. Consider a few cases,
# you are designing a mobile app, and the app should utilize less storage
# You are designing a small microprocessor-based product, and do not have an abundance of memory available
# If you used balanced trees/ linked lists, they would be stored in fragmented heap memory, and we could not improve performance by referencing CPU cache (locality of reference)

# Lastly, scale is a monster. consider, you want to write a micro-service that would fetch reels for a users explore page.
# but you don't want to fetch reels that the user has already liked. So for all (millions) of users, we need to track all the reels they have seen.
# If you consider just 10k per user's lifetime, it still is 10GB of storage, just for this simple service.


### How to address this problem?
# One way would be to use a data structure, which doesn't use so much metadata
# so for 1 Mil integers, it would use 4 bytes*1 Mil = 4 MB
# but, can we do better?
# What if we don't store the actual data?
# What if we use 1 bit for 1 key? (the absolute barebones)


### Enter, Bloom Filters
# We induce data loss, by not storing the actual element, just the presence of the element.
# consider an arr with 16 slots. you take a key, hash it, mod it by 16, take the result, and set the corresponding bit in arr to 1
# so we can get the presence of this key, but not the actual key from the array.


# Dealing with collisions (FALSE POSITIVEs)
# if we use a hash function followed by a mod function, we will inevitably have collisions
# Multiple keys can be hashed to the same index
# Which means, we can have "FALSE POSITIVES"
# key abc@gmail hashes to index 233, and now we are checking for bca@gmail,
# If this also hashes to index 233, we get a false positive
# So, this is one drawback of the Bloom Filters.
# Note: the data structure can still say with 100% certainty if a key is not a part of the set (if the bit in arr is 0).


### How to reduce the probability of false positives?
# The simplest way is to increase the size of the bloom filter
# Generally speaking, collisions happen more probably because of the mod operation rather than the hash function.
# Hence, increasing the bloom filter size significantly should substantially lower the odds of a collision.

# Next, we look at the type of hash functions available to use for our bloom filter
# We have md5, sha256, murmur hash, FN hash. Which one to pick?
# sha, md5 are cryptographic in nature, here, the focus is on security (avoiding reverse hashing)
# Due to this, they have complex algorithms, that can be reasonably CPU intensive, lowering the efficiency of the bloom filter.
# Moreover, bloom filters do not warrant the security benefits that come alongside cryptographic hashing.
# Hence, the most common implementations use MurMur hash (which is almost 10x faster than the above hashes) and also ensures a highly uniform distribution


### Why do we need to resize our bloom filters? 
# When the bloom filter arr starts filling up, the false positivity rate shoots up
# when the arr is full, the fp rate is 100%
# Hence, for the data structure to function, we need to manage the fp rate and keep it below a threshold
# To do this, we need to resize the bloom filters.


### Problem with resizing the bloom filters?
# We CAN NOT simply copy-paste the existing bloom filter arr into a larger array.
# This is because, we use a hash function, and when size changes, the hash and mod output will be affected, so all bits need to be re-hashed and replaced.
# However, we do not have the actual keys stored in the bloom filter, so we can't re-hash them!
# So, we need to have the keys stored in some other data structure, and then use that to resize our bloom filter. 
# However, as expected, this operation will be very costly.


### Can we do something better?
# Of course, here comes the smart piece of engineering optimization.
# The answer: we use k different hash functions.
# To add an element, feed it to each of the k hash functions to get k array positions. 
# Set the bits at all these positions to 1.
# To test whether an element is in the set, feed it to each of the k hash functions to get k array positions.
# If any of the bits at these positions is 0, the element is definitely not in the set.
# Using multiple hash functions significantly reduces the chances of false positives.
# Note: the value of k is not too large, and double hashing and triple hashing are effective for k=3

### The magic formula
# We know that we start with a large enough size of the bloom filter, so we don't have to resize it often.
# However, if the filter is too big, we end up wasting space, the very thing that the bloom filter is meant to save.
# Next, what should be the value of k (no of hash functions to use)?

# After, a lot of research, we have a general formula,
# n = Number of items that will be inserted in the filter
# m = Number of bits in the filter (size of the filter)
# k = Number of hash functions
# p = Acceptable probability of false positive


### Space Requirement Comparison
# We start with an acceptable value of probability (threshold), estimated n, and a constant k,
# and calculate m using the magic formula (noted above).
# If we wanted a false positive rate of just 1%, will have up to 10M elements in the set, and will use 3 hash functions,
# m should be 12,364,167 bits or 1.47 MB

# In contrast, if we stored them in a set, of 10M elements, 
# We would roughly need, 8kb metadata, and 4kb key data, so 12kb data per key
# So total data = 10*10^6 * 12*10^3 = 120*10^9 = 120 GB
# Every time you think about whether the bloom filter hassle is worth it, remember about this size disparity.



