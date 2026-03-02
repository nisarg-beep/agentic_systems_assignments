first_name = input ("enter your first name:")
last_name = input ("enter your second name:")

print ("Full name :" , first_name , last_name)


try:
    age = int(input("Enter your age: "))
except ValueError:
    print ("Invalid age. Please enter a number.")
    exit ()
if age < 0:
    raise ValueError("Age cannot be negative.")

print("You will be", age + 1, "next year")