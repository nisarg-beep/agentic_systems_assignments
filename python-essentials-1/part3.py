user_name = input("enter your name:")


try :
    user_age = int(input("Enter your age : "))
    print ("Hello", user_name)
    if user_age<0:
        print ("Age cannot be negative")
        exit()
    if user_age < 13:
        print ("You are a Child")
    elif user_age >= 13 and user_age <= 17:
        print ("You are a Teenager")
    elif user_age >=18 and user_age <= 59:
        print ("You are an Adult")
    else:
        print ("You are a Senior Citizen")

    if user_age >= 18:
        print ("You are eligible to vote")
    else:
        print ("You are not eligible to vote")
    
    
except ValueError:
    print ("Invalid age input ")


