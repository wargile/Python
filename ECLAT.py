# ECLAT (Equivalence Class Transformation) frequenct pattern algorithm

# 10,a,c,d,e
# 20,a,b,e
# 30,b,c,e

# Tid-list: List of transaction id's containing an itemset
a = {}
a[10] = ['a','c','d','e']
a[20] = ['a','b','e']
a[30] = ['b','c','e']
a

# Create Vertical format
b = {}

for x in a:
    for item in a[x]:
        if not item in b:
            b[item] = []
        b[item].append(x)

b

# TODO: Get interesection, get diffset
