from fastapi import APIRouter

from src.api.resources.request_formats import LoginFormat, IdSessionKeyFormat, NewUserFormat, UserEditFormat

import src.components.users as users

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post("/login")
async def login(login_body: LoginFormat):
    """
    This will log a user in and get them the session
    key for their current session
    :param login_body: the user's username and password (in the body of the request)
    :return: the session key of successful and user id, error string if not
    """
    return users.login_user(login_body.username, login_body.password)

@router.post("/logout")
async def logout(logout_body: IdSessionKeyFormat):
    """
    This function will log a user out and wipe
    their session key from the database

    :param logout_body: the user's id and session key (in the body of the request)

    :return: "signed out" if signed out, "bad request" otherwise
    """
    return users.logout_user(logout_body.user_id, logout_body.session_key)


@router.put("/new")
async def newUser(new_params: NewUserFormat):
    """
    This function will create a new user
    :param new_params: the username, password, and email of the new user
        (in the body of the request)
    :return: a message based on the status
    """
    return users.create_user(new_params.username, new_params.password, new_params.email)


@router.delete("/delete")
async def deleteUser(delete_params: IdSessionKeyFormat):
    """
    This function will delete a user and for each
    world they own, will try to move ownership to an
    admin
    :param delete_params:  the user's id and session key (in the body of the request)
    :return: True if successful, False if failure
    """
    return users.delete_user(delete_params.user_id, delete_params.session_key)


@router.post("/edit")
async def editUser(edit_params: UserEditFormat):
    """
        This function will edit a user's information
        given they are the user requesting it

        :param edit_params: the user's id, session key, and details to change

        :format details: { username: new username,
                           profile_pic: new profile picture,
                           public: True or False,
                           bio: new bio
                         }

        :return: True if successful, False if not
        """
    return users.edit_account(edit_params.user_id, edit_params.session_key, edit_params.details)


@router.get("/{user_id}")
async def getUser(user_id: int):
    """
    This function will get public the info on a user
    :param user_id: the user's id
    :return: the user's info in json format

    :format return: { username: user's username,
                      profile_pic: user's profile picture,
                      bio: the user's bio,
                      worlds: [{id: world id,
                                name: world name} (note: only public ones)]
                    }
    """
    return users.get_user_public(user_id)


@router.post("/private/{user_id}")
async def getUserPrivate(user_id: int, session_key: str):
    """
    This function will get private the info on a user
    :param user_id: the user's id
    :param session_key: the user's session key
    :return: the user's info in json format

    :format return: { username: user's username,
                      profile_pic: user's profile picture,
                      bio: the user's bio,
                      email: the user's email
                      worlds: [{id: world id,
                                name: world name}]
                    }
    """
    return users.get_user_private(user_id, session_key)
