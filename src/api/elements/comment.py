from typing import List

from fastapi import APIRouter
import src.components.comments
from src.api.resources.request_classes import EditComment, NewComment, DeleteComment
from src.api.resources.response_classes import CommentResponse

router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)


@router.put("/manage", tags=["Edit"], response_model=CommentResponse)
async def EditComment(request_info: EditComment):
    """
    This will edit a comment's info
    """
    outcome = src.components.comments.edit_comment(request_info.AuthoDetails.user_id,
                                                   request_info.AuthoDetails.session_key,
                                                   request_info.comment_id, request_info.comment)
    if outcome[0]:
        return src.components.comments.get_comment(request_info.comment_id)

    return outcome[0]


@router.post("/manage", tags=["New"], response_model=CommentResponse)
async def NewComment(request_info: NewComment):
    """
    This will create a new comment
    """
    outcome = src.components.comments.add_comment(request_info.AuthoDetails.user_id,
                                                  request_info.AuthoDetails.session_key,
                                                  request_info.world_id, request_info.component_id,
                                                  request_info.component_type, request_info.comment)
    if outcome[0]:
        return src.components.comments.get_comment(outcome[1])
    return outcome[0]


@router.delete("/manage", tags=["Delete"], response_model=bool)
async def DeleteComment(request_info: DeleteComment):
    """
    This will delete a comment that a user owns
    """
    return src.components.comments.delete_comment(request_info.AuthoDetails.user_id,
                                                  request_info.AuthoDetails.session_key,
                                                  request_info.comment_id,)


@router.get("/{comment_id}", tags=["Details"], response_model=CommentResponse)
async def commentInfo(comment_id):
    """
    This will get the info on a comment
    """
    return src.components.comments.get_comment(comment_id)


@router.get("/{component_table}/{comment_id}", tags=["Component"], response_model=List[CommentResponse])
async def commentInfo(component_table, comment_id):
    """
    This will get the info on a comment
    """
    return src.components.comments.get_component_comments(comment_id, component_table)
