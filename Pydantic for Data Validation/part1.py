from pydantic import BaseModel , Field , EmailStr

class UserRegister (BaseModel):
    username : str = Field (min_length= 5)
    email : EmailStr
    age : int = Field (ge= 18)

user_info = {"username" : "nisarg" , "email" : "abcd@gmail.com" , "age" : 18}

u1 = UserRegister(**user_info)

print (user_info)
