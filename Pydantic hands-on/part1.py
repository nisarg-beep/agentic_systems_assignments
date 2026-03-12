from pydantic import BaseModel, Field , EmailStr , ConfigDict
from typing import Optional

class Address (BaseModel):
    city :str = Field (...,min_length = 3 )
    pincode : str = Field (..., pattern= r"^\d{6}$" )
    model_config = ConfigDict(validate_assignment= True)

class UserModel (BaseModel):
    user_id: int 
    name : str
    email : EmailStr
    age : int = Field(...,ge= 18)
    address : Address
    is_premium : Optional [bool] = False
    model_config = ConfigDict(validate_assignment= True)
