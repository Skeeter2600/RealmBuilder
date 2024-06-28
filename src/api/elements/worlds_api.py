from fastapi import APIRouter

from src.api.resources.request_formats import IdSessionKeyFormat, WorldElementsFormat, WorldJoinPrivateFormat

import src.components.worlds as worlds

router = APIRouter(
    tags=['Worlds'],
    prefix='/worlds'
)

@router.put('/add/{name}')
async def add_world(name: str, user_details: IdSessionKeyFormat):
    """
    This function will add a world to the database
    :param name: The name of the world
    :param user_details: the user's id and session_key (stored in body of request)

    :return: { result: bool,
               world_id: int (-1 if failed)
              }
    """
    return worlds.add_world(name, user_details.user_id, user_details.session_key)

@router.delete('/delete/{world_id}')
async def delete_world(world_id: int, user_details: IdSessionKeyFormat):
    """
    This function will delete a world and all
    the components associated with it
    :param world_id: the id of the world to delete
    :param user_details: the user's id and session_key (stored in body of request)

    :return: True if successful, False if not
    """
    return worlds.delete_world(world_id, user_details.user_id, user_details.session_key)

@router.post('/update/{world_id}')
async def update_world(world_id: int, user_details: IdSessionKeyFormat, elements: WorldElementsFormat):
    """
    This function will edit the elements of a world
    :param world_id: the id of the world
    :param user_details: the user's id and session_key (stored in body of request)
    :param elements: the elements being changed in json (in body of request

    :format elements:
            { name: the world name,
              description: the world description,
              public: True or False
            }

    :return: True if edited, False if not
    """
    return worlds.edit_world(world_id, user_details.user_id, user_details.session_key, elements)

@router.put('/join/public/{world_id}')
async def join_world_public(world_id: int, user_details: IdSessionKeyFormat):
    """
    This function will allow a user to join a world

    :param world_id: the id of the world
    :param user_details: the user's id and session_key (stored in body of request)

    :return: True if successful, False if not
    """
    return worlds.join_world_public(world_id, user_details.user_id, user_details.session_key)


@router.put('/join/private/{world_id}')
async def join_world_private(world_id: int, join_details: WorldJoinPrivateFormat):
    """
    This function will allow a user to join a world

    :param world_id: the id of the world
    :param join_details: the user's id, the admin's id, and session_key (stored in body of request)


    :return: True if successful, False if not
    """
    return worlds.join_world_private(world_id, join_details.user_id,
                                     join_details.admin_id, join_details.session_key)

@router.get('/owner/{world_id}')
async def world_owner(world_id: int):
    """
    This will get the info on the owner of the world

    :param world_id: the id of the world being checked

    :return: the info on the owner
    :format return:
            {  id:   user id,
               name: user's name,
               profile_pic: user's profile picture
            }
    """
    return worlds.get_owner(world_id)

@router.post('users/{world_id}')
async def world_users(world_id: int, user_details: IdSessionKeyFormat):
    """
    This function will get a list of all users who
    are a part of a world
    :param world_id: the id of the world being checked
    :param user_details: the user's id and session_key (stored in body of request)

    :return: a list of the users in a world

    :format return:
            [{  id:   user id,
                name: user's name,
                profile_picture: user's profile picture
            }]
    """
    return worlds.get_world_user_list(world_id, user_details.user_id, user_details.session_key)

@router.post("/users/{world_id}/admins")
async def world_admins(world_id: int, user_details: IdSessionKeyFormat):
    """
    This function will get a list of all users who
    are admins of a world
    :param world_id: the id of the world being checked
    :param user_details: the user's id and session_key (stored in body of request)

    :return: a list of the admins in a world

    :format return:
            [{  id:   user id,
                name: user's name,
                profile_picture: user's profile picture
            }]
    """
    return worlds.get_world_admin_list(world_id, user_details.user_id, user_details.session_key)

@router.post('/details/{world_id}')
async def world_details(world_id: int, user_details: IdSessionKeyFormat):
    """
    This function will get the information about a world
    based on if they are an owner, admin, or if they are
    able to access it
    :param world_id: the id of the world being accessed
    :param user_details: the user's id and session_key (stored in body of request)

    :return: The information in json format if good
             {valid: False} if not good

    :format return:
            { valid: able to view details,
              like_dislike_info: {
                  likes: int of likes,
                  dislikes: int of dislikes
                  user_like: is user liked it (True or False),
                  user_dislike: is user disliked it (True or False)
              }
              name: world name,
              description: world description,
              npcs:     [{ id: npc id,
                           name: npc name}],
              cities:   [{ id: city id,
                           name: city name}],
              specials: [{ id: special id,
                           name: special name}],
              comments:     [{ user: { user_id: user's id,
                                       user_name: user's name,
                                       profile_picture: user's profile picture},
                              comment: the comment,
                              time: the time stamp of the comment
                              likes: int of likes,
                              dislikes: int of dislikes
                            }]
              user_list:    [{ id: user id,
                               username: user's name,
                               profile_picture: user's profile picture}]
            }
    """
    return worlds.get_world_details(world_id, user_details.user_id, user_details.session_key)

@router.post('/search/{query}/{page}/{limit}')
async def search(query: str, page: int, limit: int, user_details: IdSessionKeyFormat):
    """
    This function will search for worlds that have the
    searched string in them

    :param query: the string to search for
    :param limit: the number of results to show
    :param page: the selection of worlds to show
    :param user_details: the user's id and session_key (stored in body of request)

    :return: the list of worlds and their elements that
        meet the search requirements in json format

    :format return: [{ id: world_id
                       name: world's name}]
    """
    return worlds.search_world(query, page, limit, user_details.user_id, user_details.session_key)
