# Gini impurity is a measure of how impure a set is. If you have a set of items,
# such as [A, A, B, B, B, C], then Gini impurity tells you the probability that
# you would be wrong if you picked one item and randomly guessed its label.
# If the set were all As, you would always guess A and never be wrong, so the set would be totally pure.

# Gini impurity
# This function takes a list of items and calculates the Gini impurity:

def gini_impurity(l):
  total = len(l)
  counts = {}
  for item in l:
    counts.setdefault(item, 0)
    counts[item] += 1

  imp = 0
  for j in l:
    f1 = float(counts[j])/total
    for k in l:
      if j == k: continue
      f2 = float(counts[k]) / total
      imp += f1 * f2
  return imp

v = [3,1,2,1,4,10,2,2,3,5,6,7,4,4,10]
gini_impurity(v)
