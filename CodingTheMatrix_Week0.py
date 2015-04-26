# Coding the Matrix - Week 0

# Sets
S = {-4, 4, -3, 3, -2, 2, -1, 1, 0}
{x for x in S if x >= 0}

# Cardinality (Cartesian product) of two sets A and B = A x B
A = {1, 2}
B = {a, b, c, d}
# Answer: {{1,a},{1,b},{2,a},{2,b},{3,a},{3,b},{4,a},{4,b}}

# TODO: Domain and sub-domain (video 3)

# Co-domain is the set from which all outputs are chosen

# The output of a given input is called the image of that input
# The image of q under a function f is denoted f(q)
# If f(q) = r, we say that q maps to f under r (q -> r)

# A probability distribution - rolling a die:
A = {1:1/6, 2:1/6, 3:1/6, 4:1/6, 5:1/6, 6:1/6}
A[3] # Gives 1/6

# Create a simple solver for ax + b = c:
def solve(a, b, c):
    return ((c - b) / a)

# Solve 10x + 5 = 30
solve(10, 5, 30) # Answer: 2.5
# This can also solve complex numbers. (10 + 5i)x + 5 = 30:
solve(10+5j, 5, 20)

range
