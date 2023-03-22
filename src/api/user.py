from fastapi import APIRouter
from pydantic import BaseModel
from PIL import Image
import src.components.users

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get("/{user_id}", tags=["Details", "Public"])
async def get_user_details_public(user_id):
    """
    This will retrieve the info of a user
    """
    return src.components.users.get_user_public(user_id)


class UserDetails(BaseModel):
    user_id: int
    session_key: str


@router.get("/", tags=["Details", "Private"])
async def get_user_details_private(request_info: UserDetails):
    """
    This will retrieve the info of a user
    """
    return src.components.users.get_user_private(request_info.user_id, request_info.session_key)


class UpdateDetails(BaseModel):
    username: str
    profile_pic: Image
    public: bool
    bio: str


class EditUserDetails(BaseModel):
    user_id: int
    session_key: str
    details: UpdateDetails


@router.put("/", tags=["Edit"])
async def edit_user_details(request_info: EditUserDetails):
    """
    This will edit a user's profile
    """
    return src.components.users.edit_account(request_info.user_id, request_info.session_key,
                                             request_info.details)


class NewUser(BaseModel):
    username: str
    password: str
    email: str


@router.post("/", tags=["New"])
async def new_user(request_info: NewUser):
    """
    This will create a new user
    """
    outcome = src.components.users.create_user(request_info.username, request_info.password,
                                               request_info.email)
    if outcome == "Success!":
        return src.components.users.login_user(request_info.username, request_info.password)

    return outcome


@router.delete("/", tags=["Delete"])
async def delete_user(request_info: UserDetails):
    """
    This will delete a user's account
    """
    return src.components.users.delete_user(request_info.user_id, request_info.session_key)


class LoginDetails(BaseModel):
    username: str
    password: str


@router.get("/log", tags=["Login"])
async def login_user(request_info: LoginDetails):
    """
    This will sign a user in
    """
    return src.components.users.login_user(request_info.username, request_info.password)


@router.put("/log", tags=["Logout"])
async def logout_user(request_info: UserDetails):
    """
    This will log a user out
    """
    return src.components.users.logout_user(request_info.user_id, request_info.session_key)
