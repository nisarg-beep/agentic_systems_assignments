try :
    x = int(input("enter the first number :"))
    y = int(input("enter the second number :"))
    res = x+y
    print ("The sum of the numbers is:" , res)

    if y == 0:
        raise ZeroDivisionError("Number cannot be divided by zero")
    
    div = x/ y
    print (div)
except ValueError:
    print ("Invalid input")


