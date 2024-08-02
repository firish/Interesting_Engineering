### What is a skip list
It is a linked-list-based probabilistic data structure with,
O(log N) lookup and insertion,
within an ordered sequence of elements.

A skip list has,
benefits of sorted array (searching)
benefits of linked list (insertion)

### Intuitions
Fast search is made possible by:
maintaining a linked hierarchy of subsequences,
with each successive subsequence skipping over fewer elements than the previous one.

Searching starts in the sparsest subsequence until two consecutive elements have been found,
one smaller and one larger than or equal to the element searched for.
Via the linked hierarchy, these two elements link to elements of the next sparsest subsequence, 
where searching is continued until finally searching in the full sequence. 


### Implementation
A skip list is built in layers.
The bottom layer 1 is an ordinary ordered linked list.
Each higher layer acts as an "express lane" for the lists below,
where an element in layer i appears in layer i+1 with a probability of p.
NOTE: The common values for p are 1/2 and 1/4.

![skip list wiki](https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Skip_list.svg/800px-Skip_list.svg.png)

A schematic picture of the skip list data structure. 
Each box with an arrow represents a pointer and a row is a linked list giving a sparse subsequence; 
the numbered boxes (in yellow) at the bottom represent the ordered data sequence. 
Searching proceeds downwards from the sparsest subsequence at the top until consecutive elements bracketing the search element are found.

IMP: A skip list will have log (base 1/p) n skip lists, where p is the probability and n is number of elements.

### Lookup
A search for a target element begins at the head element in the top list, 
and proceeds horizontally until the current element is greater than or equal to the target.
If the current element is equal to the target, it has been found.  
If the current element is greater than the target, or the search reaches the end of the linked list,
the procedure is repeated after returning to the previous element and dropping down vertically to the next lower list.
The expected steps at each lane is p, and the overall extected lookup time complexity is O(log n).


### Insertion
![skip list insertion](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Skip_list_add_element-en.gif/800px-Skip_list_add_element-en.gif)
