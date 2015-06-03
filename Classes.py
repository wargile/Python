# Class example, and use of "self" ++
# https://freepythontips.wordpress.com/2013/08/07/the-self-variable-in-python-explained/

class BalleKlorin:
    balleklorin = 200
    more_balleklorin = -4
    is_balleklorin_ready = True
    the_balleklorin_dict = {}
    
    def init(self, multiply):
        self.balleklorin *= multiply
        self.more_balleklorin -= 10
        return self.balleklorin

    def get_balleklorin(self):
        if self.is_balleklorin_ready:
            return self.balleklorin * self.more_balleklorin
        else:
            return 0

b = BalleKlorin()
b.init(22.1575)
print(b.balleklorin)
print(b.get_balleklorin())
print(BalleKlorin().balleklorin)

# ------------------------------------------------------------------------------------------------

mygenerator = (x*x for x in range(3))
for i in mygenerator:
    print i
for i in mygenerator:
    print i
# Does not work 2nd time, it's a generator, so it's "used up"!

myiterator = [x*x for x in range(3)]
for i in myiterator:
    print i
for p in myiterator:
    print p
# Can be called several times, unlike generator!

# Using yield
def f123():
    print("Before yield 1...")
    yield 1
    print("Now 1 is yielded!")
    print("Before yield 2...")
    yield 2
    print("Now 2 is yielded!")
    print("Before yield 3...")
    yield 3
    print("Now 3 is yielded!")
    print("This is the end!")
 
for item in f123():
    print item

