"""
Just testing some class handling...
Style guide for Python: http://legacy.python.org/dev/peps/pep-0008/

# In Python interpreter:
import os
os.chdir('c:/coding/python')
import terje1
f = terje1.Foo('Fido')
dir(f) # Show methods
"""

class Dog():
    def say(self, what):
        print self.name, 'says it:', what

    def __init__(self, name):
        self.name = name
        self.tricks = []

    def getname(self):
        return self.name

    def addtrick(self, trick):
        self.tricks.append(trick)

    def gettricks(self):
        return self.tricks

if __name__ == '__main__':
    f = Dog('Fido')
    f.addtrick('Roll around')
    f.addtrick('Fetch')
    f.addtrick('Fetch')
    print f.gettricks()
    f.say('says it all!')

