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
# Note: the data structure can still say with 100% certainty if a key is not a part of the set.



