#Travesal of list
# Function to get unique values

def unique(llist):
    unique_list = []

    x: object
    for x in llist:
        if x not in unique_list:
            unique_list.append(x)

    for x in unique_list:
        print(x),


# driver code
list1 = [10, 20, 10, 30, 40, 40]
print("the unique values from 1st list is")
unique(list1)



list2 = [1, 2, 1, 1, 3, 4, 3, 3, 5]
print("\nthe unique values from 2nd list is")
unique(list2)

#Collections.counter() method
from collections import Counter


# Function to get unique values
def unique1(list1):
    # Print directly by using * symbol
    print(*Counter(list1))


# driver code
list3 = [10, 20, 10, 30, 40, 40]
print("the unique values from 1st list is")
unique1(list3)

list4 = [1, 2, 1, 1, 3, 4, 3, 3, 5]
print("\nthe unique values from 2nd list is")
unique1(list4)

