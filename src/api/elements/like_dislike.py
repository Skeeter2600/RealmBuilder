from fastapi import APIRouter
import src.components.likes_dislikes as likes_dislikes
from src.api.resources.request_classes import AddLikeDislike, RemoveLikeDislike
from src.api.resources.response_classes import LikeDislikeResponse

router = APIRouter(
    prefix='/likeDislike',
    tags=['Like/Dislike']
)


@router.put("/manage", tags=["New"], response_model=bool)
async def AddNewLikeDislike(request_info: AddLikeDislike):
    """
    This will add a new like or dislike
    """
    return likes_dislikes.add_like_dislike(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                           request_info.like_dislike,
                                           request_info.component_id, request_info.component_type)


@router.delete("/manage", tags=["Delete"], response_model=bool)
async def AddNewLikeDislike(request_info: RemoveLikeDislike):
    """
    This will remove an existing like or dislike
    """
    return likes_dislikes.remove_like_dislike(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                              request_info.component_id, request_info.component_type)


@router.get("/{component_type}/{component_id}/{user_id}", response_model=LikeDislikeResponse)
async def GetLikeDislikes(component_type, component_id, user_id):
    """
    This will get the likes and dislikes associated with
    a component
    """
    return likes_dislikes.get_likes_dislike(user_id, component_id, component_type)
