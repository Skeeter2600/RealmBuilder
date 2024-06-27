from fastapi import APIRouter

from src.api.resources.request_formats import IdSessionKeyFormat

import src.components.likes_dislikes as likes_dislikes

router = APIRouter(
    tags=['Likes Dislikes'],
    prefix='/likeDislike'
)


@router.get("/{user_id}/{component_type}/{component_id}")
async def get_like_dislikes(user_id: int, component_type: str, component_id: int):
    """
    This function will get the likes and dislikes
    on a component, as well as if the user has liked
    or disliked it

    :param user_id: the id of user checking
    :param component_id: the component being checked
    :param component_type: the type of component being checked

    :return: the info on likes

    :format return: {'likes': number of likes,
                     'dislikes': number of dislikes,
                     'user_like': bool of liked,
                     'user_dislike': bool of disliked
                     }
    """
    return likes_dislikes.get_likes_dislike(user_id, component_id, component_type)

@router.put("/{component_type}/{component_id}/{like_dislike}")
async def add_like_dislike(component_type: str, component_id: int,
                           like_dislike:bool, user_details: IdSessionKeyFormat):
    """
    This function will add a new like or dislike to the table.

    :param like_dislike: if it is a like or dislike
                         (True for like, False for dislike)
    :param component_id: the id of the component being liked
    :param component_type: the type of component being liked
    :param user_details: the user's id and session_key (stored in body of request)

    :return: True if successful, False if not
    """
    return likes_dislikes.add_like_dislike(user_details.user_id, user_details.session_key,
                                           like_dislike, component_id, component_type)

@router.delete("/{component_type}/{component_id}")
async def remove_like_dislike(component_type: str, component_id: int, user_details: IdSessionKeyFormat):
    """
    This function will remove a new like or dislike to the table.

    :param component_id: the id of the component being liked
    :param component_type: the type of component being liked
    :param user_details: the user's id and session_key (stored in body of request)

    :return: True if successful, False if not
    """
    return likes_dislikes.remove_like_dislike(user_details.user_id, user_details.session_key, component_id, component_type)
