"""
Task: Compute the sum of all of the values in the nested list with a few criteria
If the index of the innerlist is even, then any number in between 9 and 6 (including these two numbers) are multiplied by 2 
and added to the sum of the innerList
If the index of the innerlist is odd, then any number in between 7 and 4 (including these two numbers) are multiplied by 3 
and added to the sum of the innerList
All these sums are added to a different list, called sums.
For the final list of sums, any number between 4 and 5 (including these two numbers) is multiplied by 0 and the sum of
that list is returned as the final output.
Then, all the remaining numbers in sums is added up and returned through the function sum_smiff()
"""

"""
This function calculates the sum of each list by checking whether each list has the upper or lower and whether the 
lower comes before the upper. If all these criteria are met, then a new array is created with all the values in between and including 
the lower and upper bound multiplied by the multiple and all the other values remain the same. The function returns the sum of the new list of
modified values. 
 """

def findSum(list,upper,lower,multiple):
    if upper in list and lower in list and list.index(upper)>list.index(lower):
        sumList=list[:list.index(lower)]
        for i in list[list.index(lower):list.index(upper)+1]:
            sumList.append(i*multiple)
        sumList.extend(list[list.index(upper)+1:])
        return sum(sumList)
    else:
        return sum(list)

"""
This function takes in the nested list as a parameter. It takes the sum of each list using the previous function and appends it to 
a list with the sums of all the lists within the nested list. Depending on whether the index of the list is even or odd, the passing argument 
will vary. Then, at the end, we return the sum of the modified list of sums. 
"""

def sum_ssmif(nestList):
    sums=[]
    for list in nestList:
        sumNum=0
        if nestList.index(list)%2==0:
            sumNum=findSum(list,6,9,2)
        else:
            sumNum=findSum(list,4,7,3)    
        sums.append(sumNum)   
    return findSum(sums,5,4,0)
        



if __name__ == '__main__':
    list=[ [1, 2, 3, 9, 2, 6, 1], [1, 3], [1, 2, 3], [7, 1, 4, 2], [1, 2, 2] ]
    print(sum_ssmif(list))