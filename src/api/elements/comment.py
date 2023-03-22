from fastapi import APIRouter
import src.components.comments
from src.api.resources.classes import EditComment, NewComment, DeleteComment

router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)


@router.put("/manage", tags=["Edit"])
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


@router.post("/manage", tags=["New"])
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


@router.delete("/manage", tags=["Delete"])
async def DeleteComment(request_info: DeleteComment):
    """
    This will delete a comment that a user owns
    """
    return src.components.comments.delete_comment(request_info.AuthoDetails.user_id,
                                                  request_info.AuthoDetails.session_key,
                                                  request_info.comment_id,)


@router.get("/{comment_id}", tags=["Details"])
async def comment_info(comment_id):
    """
    This will get the info on an npc
    """
    return src.components.comments.get_comment(comment_id)


@router.get("/{component_table}/{comment_id}", tags=["Component"])
async def comment_info(component_table, comment_id):
    """
    This will get the info on a comment
    """
    return src.components.comments.get_component_comments(comment_id, component_table)
