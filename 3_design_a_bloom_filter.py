### What the fuck is a Bloom Filter?
# Bloom Filter is basically used to check whether an element is a part of a set. Thats it.

# Typically, hashmaps, and sets would suffice for this, as they both offer (almost) an constant time lookup.
# However, this problem becomes very tricky at scale.
# Like gmail checking if an email already exists
# Or checking if a webpage exists in the DNS cache
# both of these have hundreds of millions elements that are a part of the membership set,
# and in such cases, we can do better than a set/dict.


### What the fuck is the problem with a set/dict?
# How is a set implemented?
# Most languages internally implement set as a hashmap, or a balanced-binary tree,
# behind-the-scenes, hashmaps, might also use linkedlists, or balanced-trees (chaining), to store data.
# For both of these, 1 node will be roughly 12 bytes, 4 for data, and 4 as meta-data (left, right pointers for a tree, and prev, next for a linked list)
# so for storing a million keys, the data will be 12MB, where 8MB is just meta data.
# this problem becomes more bad with increasing number of keys.


### When storage is so cheap, is this even a problem?
# Absolutely yes. Consider a few cases,
# you are designing a mobile app, and the app should utilize less storage
# you are designing a small microprocessor-based product, and do not have an abundance of memory available
# if you used balanced trees/ linked lists, they would be stored in fragmented heap memory, and we could not improve performance by referencing CPU cache (locality of reference)

# lastly, scale is a monster. consider, you want to write a micro-service that would fetch reels for a users explore page.
# but you don't want to fetch reels that the user has already liked. So for all (millions) of users, we need to track all the reels they have seen.
# if you consider just 10k per user's lifetime, it still is 10GB of storage, just for this simple service.



### How to address this problem?
# one way would be to use a data structure, which doesnt use so much meta data
# so for 1 Mil integers, it would use 4 bytes*1 Mil = 4 MB
# but, can we do better?
# what if we dont store the actual data?
# what if we just use 1 bit for 1 key? (the absolute barebones)

# we address this by,
# We induce data loss, by not storing the actual element, just presence of the element.
# consider an arr with 16 slots. you take a key, hash it, mod it by 16, take the result, and set the corresponding bit in arr to 1
# so we can get the presence of this key, but not the actual key from array.

