# first_name = input ("enter your first name:")
# last_name = input ("enter your second name:")

# print ("Full name :" , first_name , last_name)


# age = int (input("Enter your age:"))

# if age == str :
#     raise ValueError("Invalid age")

# if age < 0:
#     raise TypeError("Age cannot be negative")

# print ("You will be " , age+1, "next year")


try:
    age = int(input("Enter your age: "))
except ValueError:
    raise ValueError("Invalid age. Please enter a number.")

if age < 0:
    raise ValueError("Age cannot be negative.")

print("You will be", age + 1, "next year")