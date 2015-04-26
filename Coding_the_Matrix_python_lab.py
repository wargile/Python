# version code bd6127413fba+
coursera = 1
# Please fill out this stencil and submit using the provided submission script.





## 1: (Task 1) Minutes in a Week
minutes_in_week = 60 * 24 * 7



## 2: (Task 2) Remainder
remainder_without_mod = 2304811 - ((2304811 // 47) * 47)



## 3: (Task 3) Divisibility
divisible_by_3 = ((673 + 909) % 3 == 0)



## 4: (Task 4) Conditional Expression
x = -9
y = 1/2
expression_val = 2**(y+1/2) if x+10<0 else 2**(y-1/2)



## 5: (Task 5) Squares Set Comprehension
first_five_squares = { x**2 for x in {1,2,3,4,5} }



## 6: (Task 6) Powers-of-2 Set Comprehension
first_five_pows_two = { 2**x for x in {0,1,2,3,4} }



## 7: (Task 7) Double comprehension evaluating to nine-element set
X1 = { 2, 3, 4 }
Y1 = { 5, 6, 7 }
{ x*y for x in X1 for y in Y1 }



## 8: (Task 8) Double comprehension evaluating to five-element set
# NOTE: Use values that give 5 unique values in result set
X2 = { 1, 3, 9 }
Y2 = { 2, 6, 18 }
# { x*y for x in X2 for y in Y2 if x in X2 and y in Y2 }
# *** ERROR! ***
# X2 | Y2
# *** ERROR! ***
five_elements_set = { x*y for x in X2 for y in Y2 }



## 9: (Task 9) Set intersection as a comprehension
S = {1, 2, 3, 4}
T = {3, 4, 5, 6}
# Replace { ... } with a one-line set comprehension that evaluates to the intersection of S and T
S_intersect_T = { x for x in S for x in T if x in S and x in T }



## 10: (Task 10) Average
list_of_numbers = [20, 10, 15, 75]
# Replace ... with a one-line expression that evaluates to the average of list_of_numbers.
# Your expression should refer to the variable list_of_numbers, and should work
# for a list of any length greater than zero.
list_average = sum(list_of_numbers) / len(list_of_numbers) 



## 11: (Task 11) Cartesian-product comprehension
# Replace ... with a double list comprehension over {'A','B','C'} and {1,2,3}
cartesian_product = [[x, y] for x in {'A','B','C'} for y in {1,2,3}]



## 12: (Task 12) Sum of numbers in list of list of numbers
LofL = [[.25, .75, .1], [-1, 0], [4, 4, 4, 4]]
# Replace ... with a one-line expression of the form sum([sum(...) ... ]) that
# includes a comprehension and evaluates to the sum of all numbers in all the lists.
LofL_sum = sum(sum(LofL[x]) for x in range(len(LofL)))



## 13: (Task 13) Three-element tuples summing to zero
S = {-4, -2, 1, 2, 5, 0}
# Replace [ ... ] with a one-line list comprehension in which S appears
zero_sum_list = [(x,y,z) for x in S for y in S for z in S if x+y+z == 0]



## 14: (Task 14) Nontrivial three-element tuples summing to zero
S = {-4, -2, 1, 2, 5, 0}
# Replace [ ... ] with a one-line list comprehension in which S appears
exclude_zero_list = [(x,y,z) for x in S for y in S for z in S if x+y+z == 0 and not sum([x == 0 for x in [x,y,z]]) == 3]


## 15: (Task 15) One nontrivial three-element tuple summing to zero
S = {-4, -2, 1, 2, 5, 0}
# Replace ... with a one-line expression that uses a list comprehension in which S appears
first_of_tuples_list = [(x,y,z) for x in S for y in S for z in S if x+y+z == 0 and not sum([x == 0 for x in [x,y,z]]) == 3][0]



## 16: (Task 16) List and set differ
# Assign to example_L a list such that len(example_L) != len(list(set(example_L)))
example_L = [1,1,2,3]



## 17: (Task 17) Odd numbers
# Replace {...} with a one-line set comprehension over a range of the form range(n)
# Task 17: Write a comprehension over a range of the form range(n) such that the value of the compre-
# hension is the set of odd numbers from 1 to 99.
odd_num_list_range = {x for x in set(range(1,100,2))}



## 18: (Task 18) Using range and zip
# In the line below, replace ... with an expression that does not include a comprehension.
# Instead, it should use zip and range.
# Note: zip() does not return a list. It returns an 'iterator of tuples'
# Task 18: Assign to L the list consisting of the first five letters ['A','B','C','D','E']. Next, use L in
# an expression whose value is
# [(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E')]
# Your expression should use a range and a zip, but should not use a comprehension.
L =  ['A','B','C','D','E']
range_and_zip = list(zip(range(len(L)), L))



## 19: (Task 19) Using zip to find elementwise sums
A = [10, 25, 40]
B = [1, 15, 20]
# Replace [...] with a one-line comprehension that uses zip together with the variables A and B.
# The comprehension should evaluate to a list whose ith element is the ith element of
# A plus the ith element of B.
list_sum_zip = [sum(x) for x in zip(A, B)]



## 20: (Task 20) Extracting the value corresponding to key k from each dictionary in a list
dlist = [{'James':'Sean', 'director':'Terence'}, {'James':'Roger', 'director':'Lewis'}, {'James':'Pierce', 'director':'Roger'}]
k = 'James'
# Replace [...] with a one-line comprehension that uses dlist and k
# and that evaluates to ['Sean','Roger','Pierce']
value_list = [x[k] for x in dlist]



## 21: (Task 21) Extracting the value corresponding to k when it exists
dlist = [{'Bilbo':'Ian','Frodo':'Elijah'},{'Bilbo':'Martin','Thorin':'Richard'}]
k = 'Bilbo'
#Replace [...] with a one-line comprehension
value_list_modified_1 = [x[k] if k in x else 'NOT PRESENT' for x in dlist] # <-- Use the same expression here
k = 'Frodo'
value_list_modified_2 = [x[k] if k in x else 'NOT PRESENT' for x in dlist] # <-- as you do here

## 22: (Task 22) A dictionary mapping integers to their squares
# Task 22: Using range, write a comprehension whose value is a dictionary. The keys should be the integers
# from 0 to 99 and the value corresponding to a key should be the square of the key.
# Replace {...} with a one-line dictionary comprehension
square_dict = { k:k**2 for k in range(0,100,1) }


## 23: (Task 23) Making the identity function
D = {'red','white','blue'}
# Replace {...} with a one-line dictionary comprehension
identity_dict = { x:x for x in D }



## 24: (Task 24) Mapping integers to their representation over a given base
base = 10
digits = set(range(base))
# Replace { ... } with a one-line dictionary comprehension
# Your comprehension should use the variables 'base' and 'digits' so it will work correctly if these
# are assigned different values (e.g. base = 2 and digits = {0,1})
representation_dict = { ... }



## 25: (Task 25) A dictionary mapping names to salaries
id2salary = {0:1000.0, 1:1200.50, 2:990}
names = ['Larry', 'Curly', 'Moe']
id2salary = {0:1000.0, 3:990, 1:1200.50}
names = ['Larry', 'Curly', '', 'Moe']
# Replace { ... } with a one-line dictionary comprehension that uses id2salary and names.
listdict2dict = { names[x]:id2salary[x] for x in range(len(names)) if len(names[x]) > 0 }



## 26: (Task 26) Procedure nextInts
# Complete the procedure definition by replacing [ ... ] with a one-line list comprehension
def nextInts(L): return [x+1 for x in L]


## 27: (Task 27) Procedure cubes
# Complete the procedure definition by replacing [ ... ] with a one-line list comprehension
def cubes(L): return [x**3 for x in L]



## 28: (Task 28) Procedure dict2list
# Input: a dictionary dct and a list keylist consisting of the keys of dct
# Output: the list L such that L[i] is the value associated in dct with keylist[i]
# Example: dict2list({'a':'A', 'b':'B', 'c':'C'},['b','c','a']) should equal ['B','C','A']
# Complete the procedure definition by replacing [ ... ] with a one-line list comprehension
def dict2list(dct, keylist): return [dct[x] for x in keylist]


## 29: (Task 29) Procedure list2dict
# Input: a list L and a list keylist of the same length
# Output: the dictionary that maps keylist[i] to L[i] for i=0,1,...len(L)-1
# Example: list2dict(['A','B','C'],['a','b','c']) should equal {'a':'A', 'b':'B', 'c':'C'}
# Complete the procedure definition by replacing { ... } with a one-line dictionary comprehension
def list2dict(L, keylist): return {keylist[i]:L[i] for i in range(len(keylist)) }
