# -*- coding: utf-8 -*-
"""
Created on Mon May 18 16:32:52 2020

@author: Gerard
"""

## Task 1

## Question 1

## 1.1 

def myreduce(anyfunc, sequence):

  result = sequence[0]
  for item in sequence[1:]:
   result = anyfunc(result, item)

  return result

## test myreduced
  
print("Sum a range of Numbers:", myreduce(lambda x, y: x + y, range(1, 500)))



## 1.2 

def myfilter(anyfunc, sequence):

 result1 = []
 for item in sequence:
       if anyfunc(item):
          result1.append(item)
 return result1

print("Prime Numbers: ", list(myfilter(lambda x: x % 3==0, range(1, 30))))


## Question 2
alpha_list = [i for i in  "ACADGILD"]
print(alpha_list)

list_1 = [item*num for item in ['x','y','z'] for num in range(1,5)]
print(list_1)

list_2 = [item*num for num in range(1,5) for item in ['x','y','z']]
print(list_2)

list_3 = [[item+num] for item in [2,3,4] for num in range(0,3)]

print(list_3)

list_4 = [[item+num for item in [2,3,4,5]]  for num in range(0,4)]

print(list_4)

list_5 = [(y,x) for x in [1,2,3] for y in [1,2,3]]

print(list_5)

## Question 3

def longest_word(list_word):
    longest_word = list_word[0]
    
    for word in list_word:
        
        if len(longest_word) < len(word):
            
            longest_word = word
    return longest_word

### Test Function
    
list_words = ['PHP', 'Gerard','Python', 'Computer Science', 'Machine Learning and Deep Learning']

print(longest_word(list_words))

## Task 2

## 1.1

class triangle:

    def __init__(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c
a= float(input("a="))
b= float(input("b="))
c= float(input("c="))
class Triangle(triangle):
    def __init__(self,a,b,c):
        super().__init__(a,b,c)
    
    def get_area(self):
        
         # calculate the semi-perimeter
        s = (self.a + self.b + self.c) / 2
        return (s*(s-self.a)*(s-self.b)*(s-self.c)) ** 0.5

A = Triangle(a,b,c)
print("area : {}".format(A.get_area()))


## 1.2

def filter_long_words(n, string):
    
    word_len = []
    word = string.split(" ")
    
    for i in word:
        
        if len(i)> n:
            word_len.append(i)
    return word_len

print(filter_long_words(3, "This class is so much interesting"))

## 2.1

def wordlength(word_list):
    
    return list(map(lambda x: len(x), word_list))

word_list = ['ab','cde','erty']

print(wordlength(word_list))

## 2.2


def vowel_check(char):
    if(char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u'):
        
        return True
    else:
        
        return False
print(vowel_check('y'))


        
       







