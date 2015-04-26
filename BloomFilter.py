# Bloom Filter example
# http://en.wikipedia.org/wiki/Bloom_filter
import numpy as np

bits = 0
filter_size = 11 # The size of the bit array (bloom filter array)

def h1(x):
    number = 0
    pos = 0
    for counter in range(1, filter_size, 2):
        number = number | (((x & (1 << counter)) >> counter) << pos) 
        pos += 1
    print bin(number)
    return number % 11

def h2(x):
    number = 0
    pos = 0
    for counter in range(0, filter_size, 2):
        number = number | (((x & (1 << counter)) >> counter) << pos)
        pos += 1
    print bin(number)
    return number % 11

def add_bits(number):
    global bits
    
    n1 = h1(number)
    print n1
    n2 = h2(number)
    print n2
    result = bits & (1 << n1)
    if result > 0:
        bits1 = 1
    else:
        bits1 = 0
    result = bits & (1 << n2)
    if result > 0:
        bits2 = 1
    else:
        bits2 = 0
    print "Bits:", bits1, bits2
    
    if bits1 == 1 and bits2 == 1:
        print "%d exists!" % number
        print "Bloom filter: ", bin(bits)
        return 1
    else:
        print "%d does not exist." % number
        bits = bits | (1 << n1)
        bits = bits | (1 << n2)
        print "Bloom filter: ", bin(bits)
        return 0

 
# TODO: http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.binomial.html
if __name__ == '__main__':
    numbers = np.random.randint(10, size=10) + 1
    result = []
    
    for n in numbers:
        result.append(add_bits(n))

    #add_bits(25)
    #add_bits(159)
    #add_bits(585)
    #add_bits(586)
    #add_bits(587)
    
    print numbers
    print result
