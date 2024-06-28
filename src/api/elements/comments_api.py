from fastapi import APIRouter

from src.api.resources.request_formats import IdSessionKeyFormat, AddCommentFormat, EditCommentFormat

import src.components.comments as comments

router = APIRouter(
    tags=['Comments'],
    prefix='/comments'
)

@router.put('/add')
async def add_comment(comment_details: AddCommentFormat):
    """
    This function will be called when a user makes
    a comment on a component

    NOTE: all values in the body of request
    :param comment_details:
        :param user_id: the id of the user commenting
        :param session_key: the session key of the user
        :param world_id: the id of the world the comment is in
        :param comment: the comment being made
        :param component_id: the id of the item being commented on
        :param component_type: the table name of the element being commented on

    :return: True if successful, False if not
    """
    return comments.add_comment(comment_details.user_id, comment_details.session_key, comment_details.world_id,
                                comment_details.component_id, comment_details.component_type, comment_details.comment)

@router.delete('/delete/{comment_id}')
async def delete_comment(comment_id: int, user_details: IdSessionKeyFormat):
    """
    This function will delete a comment from the table.

    :param comment_id: the id of the comment being deleted
    :param user_details: the user's id and session_key (stored in body of request)

    :return: True if deleted, False if not
    """
    return comments.delete_comment(user_details.user_id, user_details.session_key, comment_id)

@router.post('/edit')
async def edit_comment(edit_details: EditCommentFormat):
    """
    This function will edit the text in a comment, given
    the user trying to is the one who posted the comment

    NOTE: all values in the body of request
    :param edit_details:
        :param user_id: the is of the user editing
        :param session_key: the user's session key
        :param comment_id: the id of the comment being edited
        :param comment: the new comment text

   :return: True if successful, False if not
   """
    return comments.edit_comment(edit_details.user_id, edit_details.session_key,
                                 edit_details.comment_id, edit_details.comment)

@router.get('/{comment_id}/{user_id}')
async def read_comment(comment_id: int, user_id: int):
    """
    This function will get the info related to a comment

    :param comment_id: the id of the component with the comments
    :param user_id: the id of the user signed in

    :return: info on the comment

    :format return: { user: { user_id: user's id,
                              user_name: user's name,
                              profile_picture: user's profile picture},
                      comment: the comment,
                      time: the time stamp of the comment
                      like_info: {
                          likes: int of likes,
                          dislikes: int of dislikes
                          user_like: is user liked it (True or False),
                          user_dislike: is user disliked it (True or False)
                      }
                    }
    """
    return comments.get_comment(comment_id, user_id)

@router.get('/{component_table}/{component_id}/{user_id}')
async def read_component_comments(user_id: int, component_table: str, component_id: int):
    """
    This function will get the comments associated with
    a component and the info associated to them

    :param user_id: the id of the user signed in
    :param component_id: the id of the component with the comments
    :param component_table: the table of component with the comments

    :return: list of comments and their info

    :format: [{ user: { user_id: user's id,
                        user_name: user's name,
                        profile_picture: user's profile picture},
                comment: the comment,
                time: the time stamp of the comment
                like_dislike_info: {
                          likes: int of likes,
                          dislikes: int of dislikes
                          user_like: is user liked it (True or False),
                          user_dislike: is user disliked it (True or False)
                      }
            }]
    """
    return comments.get_component_comments(user_id, component_id, component_table)

@router.get('/user/{user_id}/{page}/{limit}')
def get_user_comments(user_id: int, limit: int, page: int):
    """
    This function will get the comments made by a
    user with a page limit and selection

    :param user_id: the id of the user being checked
    :param limit: the amount of comments to return
        (if none, default 25)
    :param page: the offset of the comment page
    """
    return comments.get_user_comments(user_id, limit, page)