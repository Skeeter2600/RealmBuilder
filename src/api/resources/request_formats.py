
from pydantic import BaseModel

# User Classes
class LoginFormat(BaseModel):
    username: str
    password: str

class IdSessionKeyFormat(BaseModel):
    user_id: int
    session_key: str

class NewUserFormat(BaseModel):
    username: str
    password: str
    email: str

class UserDetailsFormat(BaseModel):
    username: str
    profile_pic: str #temp for now, update once url figured out
    public: bool
    bio: str

class UserEditFormat(BaseModel):
    user_id: int
    session_key: str
    details: UserDetailsFormat