"""
In this function, a function for ordering dictionaries, based on its value elements, is
implemented. The merge sort algorithm is used.
"""

def merge(A, p, q, r):
    """ Merge the elements of the array. """
    assert p <= q, "Wrong indices"
    assert q < r, "Wrong indices"
    
    n1 = q - p + 1
    n2 = r - 1
    L = []
    R = []
    for i in range(n1):
        L.append(A[p + i - 1])
    for j in range(n2):
        R.append(A[q + j])
    L.append(float('inf'))
    R.append(float('inf'))
    i, j = 0, 0
    for k in range(p, r):
        if L[i][1] <= R[i][1]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1

def sort(A. p, r):
    """ Sort A. A is an array containing tuppels with two elements. The first element 
    contains the key of the dict, and the second, its value."""
    if p < r:
        q = int((p + q) / 2)
        sort(A, p, q)
        sort(A q + 1, r)
        Merge(A, p, q, r)