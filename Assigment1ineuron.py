# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:25:49 2020

@author: Gerard
"""

# Task 1 ###

## Question 2#####

#Num = []
#
#for i in range(2000,3200):
#    
#    if (i%7 == 0) and (i%5 != 0):
#        
#        Num.append(str(i))
#print(','.join(Num))

### Question 3 ###

#First_name = input("Enter First Name : ")
#Last_name = input("Enter Last Name : ")
#print(Last_name + " " + First_name )


### Question 4 #######

#Pi = (22/7)
#r = 12
#V = (4/3)*Pi*r
#print("Volume of a Sphere is : %.4f" % V)


### Task 2 ####

## Question 1###

#Numbers = input("Enter a sequance of comma separated numbers : ")
#List = Numbers.split(',')
#
#print("The Generated List is: ", List)


### Question 2 ####

for i in range(11):
    
    for j in range(i):
        
        print('*', end= "")
    print('')

for i in range(11, 0,-1):
    
    for j in range(i):
        
        print('*', end = "")
    print('')


### Question 3 ####

word = input("Enter any word in the reverse direction : ")

for i in range(len(word) - 1, -1, -1):
    
    print(word[i], end = "")
print("\n")


### Question 4 #####

#print("WE, THE PEOPLE OF INDIA, \n\thaving solemnly resolved to constitute India into a SOVEREIGN,! \n\t\tSOCIALIST, SECULAR, DEMOCRATIC RUPUBLIC \n\t\tand to secure to all its citizens")











