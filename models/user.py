from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

class UserSignUp(User):
    password: str
    
class UserSignIn(BaseModel):
    email: str
    password: str

class UserResponse(User):
    token: str