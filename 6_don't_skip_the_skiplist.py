### What is a skip list
# It is a linked-list-based probabilistic data structure with,
# O(log N) lookup and insertion,
# within an ordered sequence of elements.

# A skip list has,
# benefits of sorted array (searching)
# benefits of linked list (insertion)

### Intuitions
# Fast search is made possible by:
# maintaining a linked hierarchy of subsequences,
# with each successive subsequence skipping over fewer elements than the previous one.

# Searching starts in the sparsest subsequence until two consecutive elements have been found,
# one smaller and one larger than or equal to the element searched for.
# Via the linked hierarchy, these two elements link to elements of the next sparsest subsequence, 
# where searching is continued until finally searching in the full sequence. 

