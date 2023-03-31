from fastapi import APIRouter

from src.api.resources.request_classes import EditUserDetails, NewUser, LoginDetails, AuthoDetails
import src.components.users as users
from src.components.comments import get_user_comments

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get("/{user_id}", tags=["Details"])
async def get_user_details_public(user_id):
    """
    This will retrieve the info of a user
    """
    return users.get_user_public(user_id)


@router.get("/", tags=["Details"])
async def get_user_details_private(request_info: AuthoDetails):
    """
    This will retrieve the info of a user
    """
    return users.get_user_private(request_info.user_id, request_info.session_key)


@router.put("/", tags=["Edit"])
async def edit_user_details(request_info: EditUserDetails):
    """
    This will edit a user's profile
    """
    return users.edit_account(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                              request_info.details)


@router.post("/", tags=["New"])
async def new_user(request_info: NewUser):
    """
    This will create a new user
    """
    outcome = users.create_user(request_info.username, request_info.password,
                                request_info.email)
    if outcome == "Success!":
        return users.login_user(request_info.username, request_info.password)

    return outcome


@router.delete("/", tags=["Delete"])
async def delete_user(request_info: AuthoDetails):
    """
    This will delete a user's account
    """
    return users.delete_user(request_info.user_id, request_info.session_key)


@router.post("/log", tags=["Login/LogOut"], response_model=LoginDetails)
async def login_user(request_info: LoginDetails):
    """
    This will sign a user in
    """
    return users.login_user(request_info.username, request_info.password)


@router.put("/log", tags=["Login/LogOut"], response_model=str)
async def logout_user(request_info: AuthoDetails):
    """
    This will log a user out
    """
    return users.logout_user(request_info.user_id, request_info.session_key)


@router.get("/{user_id}/comments/{limit}/{page}/", tags=["Comment"])
async def user_comments(user_id, limit, page):
    """
    This will get the comments that a user has posted
    """
    return get_user_comments(user_id, limit, page)
