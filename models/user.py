from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    birth: int
    name_responsible: str
    phone_responsible: Optional[str]
    email_responsible: str
    cpf_responsible: str
    zip_code: str
    city: str
    address: str
    state: str
    scholarship_holder: bool = False
    
class UserSignUp(User):
    password: str
    
class UserSignIn(BaseModel):
    email: str
    password: str
    
class UserEdit(User):
    pass
    
class UserToken(BaseModel):
    id: int
    
class UserResponse(User):
    id: int
    token: Optional[str] = None