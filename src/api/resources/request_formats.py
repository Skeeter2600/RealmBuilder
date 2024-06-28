
from pydantic import BaseModel

#general classes

class IdSessionKeyFormat(BaseModel):
    user_id: int
    session_key: str


# User Classes
class LoginFormat(BaseModel):
    username: str
    password: str

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

# Worlds
class WorldElementsFormat(BaseModel):
    name: str
    description: str
    public: bool

class WorldJoinPrivateFormat(BaseModel):
    user_id: int
    admin_id: int
    session_key: str

# Comments
class AddCommentFormat(BaseModel):
    user_id: int
    session_key: str
    world_id: int
    component_id: int
    component_type: str
    comment: str

class EditCommentFormat(BaseModel):
    user_id: int
    session_key: str
    comment_id: int
    comment: str