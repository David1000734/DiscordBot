# flake8: noqa
import random
import sys
import os

breaker = "********************"

print("Hello Feds!")

name = "Chunk"

print(name)

name = 25

''' 5 main data types in python
    Numbers Strings Lists Tuples Dictionaries

    Arithmatic
    + - * / % **(exponential) //(floor division)
'''

print("5 + 2 =", 5 + 2)
print("5 / 2 =", 5 / 2)
print("5 ** 2 =", 5 ** 2)
print("5 // 2 =", 5 // 2)


# First commment

'''
MultiLine Comment
'''

quote = "\"Always be humble.\""

multi_Line_Quote = '''Multi-line
just like everything 
else'''

concat = quote + multi_Line_Quote

print("%s %s %s" % ('I like the quote', quote, multi_Line_Quote))

print('\n' * 5)

print("I don't like this ", end="")
print("newline")

# ******************** Start on Lists ********************
print("%s End of practice. Start Lists %s" % (breaker, breaker))

grocery_list = ['Juice', 'Tomatoes', 'Potatoes', 'Bananas']

print('First Item', grocery_list[0])

grocery_list[0] = "Green Juice"
print('First Item', grocery_list[0])

print(grocery_list[1:3])

other_events = ['Wash Car', 'Pick Up Kids', 'Cash Check']
to_do_list = [other_events, grocery_list]
print(to_do_list)

print((to_do_list[1][1]))
grocery_list.append('Onions')
print(grocery_list)

grocery_list.insert(1, "Pickle")

grocery_list.remove("Pickle")

grocery_list.sort()

grocery_list.reverse()

del grocery_list[4]
print(to_do_list)

to_do_list2 = other_events + grocery_list

print(len(to_do_list2))
print(max(to_do_list2))
print(min(to_do_list2))

print("%s End of Lists. Start Tuples %s" % (breaker, breaker))
# ******************** End of Lists ********************
pi_tuple = (3, 1, 4, 1, 5, 9)

new_tuple = list(pi_tuple)
new_list = tuple(new_tuple)
# Useful Functions: len(tuple) min(tuple) max(tuple)

print("%s End of Tuples. Start Dictionaries %s" % (breaker, breaker))
# ******************** End of Tuples ********************
super_villians = {'Fiddler' : 'Issac Bowin',
                  'Captain Cold' : 'Leonard Snart',
                  'Weather Wizard' : 'Mark Mardon',
                  'Mirror Master' : 'Sam Scudder',
                  'Pied Piper' : 'Thomas Peterson'}

print(super_villians['Captain Cold'])
del super_villians['Fiddler']

super_villians['Pied Piper'] = 'Hartley Rathaway'

print(len(super_villians))

print(super_villians.get("Pied Piper"))

print(super_villians.values())
print("%s End of Tuples. Start Conditionals %s" % (breaker, breaker))
# ******************** End of Dictionaries ********************
# if else elif
# ==
# !=
# >=
# <=

age = 16

if age > 16:
    print('You are old enough to drive')
else :
    print('You are not old enough to drive')

if age >= 21 :
    print('You are old enough to drive a tractor trailer')
elif age >= 16 :
    print('You are old enough to drive a car')
else : 
    print("You are not old enough to drive")

print("%s End of conditionals. Start For Loops %s" % (breaker, breaker))
# ******************** End of conditionals ********************
for x in range(0, 10) :
    print(x, ' ', end="")

print('\n')

grocery_list = ['Juice', 'Tomatoes', 'Potatoes', 'Bannanas']
for y in grocery_list :
    print(y)

for x in [2, 4, 6, 8, 10] :
    print (x)

num_list = [[1, 2, 3], [10, 20, 30], [100, 200, 300]]

for x in range(0, 3) :
    for y in range(0, 3) :
        print(num_list[x][y])

print("%s End of for Loops. Start while Loop %s" % (breaker, breaker))
# ******************** End of for loops ********************
random_num = random.randrange(0, 100)   # numbers from 0 to 99

''' Comment out the rando number
while(random_num != 15) :
    print(random_num)
    random_num = random.randrange(0, 100)
'''

i = 0

while (i <= 20) :
    if (i % 2 == 0) :
        print(i)
    elif (i == 9) :
        break
    else: 
        i += 1 # i = i + 1
        continue
    i += 1

print("%s End of for While Loops. Start Functions/Strings %s" % (breaker, breaker))
# ******************** End of for while loops ********************
def addNumber(fNum, lNum) :
    sumNum = fNum + lNum
    return sumNum

print('Function Call: ', addNumber(1, 4))

print('What is your name')
name = sys.stdin.readline()

print('Hello', name)

long_string = "I'll catch you if you fall - The Floor"

print(long_string[0:4])

print(long_string[-5:])     # Last 5 char

print(long_string[:-5])     # All but last 5

print(long_string[:5] + " be there")

print("%c is my %s letter and my number %d number is %.5f" % 
      ('X', 'favorite', 1, 0.14))

print(long_string.capitalize())

print(long_string.find("Floor"))        # Case sensative

print(long_string.isalpha())

print(len(long_string))

print(long_string.replace("Floor", "Ground"))

print(long_string.strip())              # Strip white space

quote_list = long_string.split(" ")
print(quote_list)

print("%s End of Function/Strings. Start Input/Output files %s" % (breaker, breaker))
# ******************** End of Functions/strings ********************
test_file = open("test.txt", "wb")      # "wb" to allow for writing to file

print(test_file.mode)

print(test_file.name)

test_file.write(bytes("Write me to the file \n", 'UTF-8'))

test_file.close()

test_file = open("test.txt", "r+")      # "r+" allow for reading and writing

text_in_file = test_file.read()
print(text_in_file)

# os.remove("test.txt")

print("%s End of File I/O. Start Objects %s" % (breaker, breaker))
# ******************** End of File I/O ********************
class Animal:           # __(stuff) means private
    __name = None       # __name = ""       Same
    __height = 0
    __weight = 0
    __sound = 0

    def __init__(self, name, height, weight, sound):
        self.__name = name
        self.__height = height
        self.__weight = weight
        self.__sound = sound

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name
    
    def set_height(self, height):
        self.__height = height

    def get_height(self):
        return self.__height
    
    def set_weight(self, weight):
        self.__weight = weight

    def get_weight(self):
        return self.__weight
    
    def set_sound(self, sound):
        self.__sound = sound

    def get_sound(self):
        return self.__sound
    
    def get_type(self):
        print("Animal")

    def toString(self):
        return "{} is {} cm tall and {} kilograms and say {}.".format(self.__name,
                                                                     self.__height,
                                                                     self.__weight,
                                                                     self.__sound)

cat = Animal('Whiskers', 33, 10, 'Meow')

print(cat.toString())

class Dog(Animal):
    __Owner = ""

    def __init__(self, name, height, weight, sound, owner):
        self.__Owner = owner
        super(Dog, self).__init__(name, height, weight, sound)

    def set_owner(self, owner):
        self.__Owner = owner

    def get_owner(self):
        return self.__Owner

    def get_type(self):
        print("Dog")

    def toString(self):
        return super().toString() + (" His owner is {}".format(self.__Owner))

    def multiple_sounds(self, how_many=None):
        if how_many is None:
            print(self.get_sound())
        else:
            print(self.get_sound() * how_many)

spot = Dog("Spot", 53, 27, "Ruff", "Darnel")
print(spot.toString())

print("%s End of Objects. Start Polymorphism %s" % (breaker, breaker))
# ******************** End of Objects ********************
class AnimalTesting:
    def get_type(self, animal):
        animal.get_type()

test_animals = AnimalTesting()

test_animals.get_type(cat)
test_animals.get_type(spot)

spot.multiple_sounds(4)
spot.multiple_sounds()

