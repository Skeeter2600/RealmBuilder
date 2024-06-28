from fastapi import APIRouter

from src.api.resources.request_formats import IdSessionKeyFormat, AddCityFormat, EditCityFormat

import src.components.cities as cities

router = APIRouter(
    tags=['Cities'],
    prefix='/city'
)

@router.put('/new')
def new_city(details: AddCityFormat):
    """
    This function will add a new city to the world,
    given the user is an owner or admin

    :param details: the info on the new city

    :format details: {
        user_id: the id of the user adding,
        session_key: the user's session key,
        details: {world_id: world city is in,
                  name: city name,
                  images: [images associated with npc],
                  population: city population,
                  song: city song,
                  trades: city trades,
                  aesthetic: city aesthetic
                  description: city description,
                  associated_npc_ids: [id: npc id],
                  associated_special_ids: [id: special id],
                }
        }

    :return: [created boolean, city id (-1 if failed)]
    """
    return cities.add_city(details.user_id, details.session_key, details.details)

@router.put('/copy/{world_id}/{city_id}')
def copy_city(user_details: IdSessionKeyFormat, city_id: int, world_id: int):
    """
    This function will make a copy of a city in
    the user's specified world

    :param user_details: the user's id and session_key (stored in body of request)
    :param city_id: the id of the city being copied
    :param world_id: the id of the world being copied to

    :return: true and the id is successful, false and -1 if failure
    """
    return cities.copy_city(user_details.user_id, user_details.session_key, city_id, world_id)

@router.delete('/{world_id}/{city_id}')
def delete_city(user_details: IdSessionKeyFormat, city_id: int, world_id: int):
    """
    This function will delete a city from the world

    :param user_details: the user's id and session_key (stored in body of request)
    :param city_id: id of the city
    :param world_id: id that the world is in

    :return: True if deleted, False if not
    """
    cities.delete_city(user_details.user_id, user_details.session_key, city_id, world_id)

@router.post('/update/{world_id}/{city_id}')
def update_city(user_details: IdSessionKeyFormat, city_id: int, world_id: int, details: EditCityFormat):
    """
    This function will modify the elements of a city
    in a world, give the user can edit it

    :param user_details: the user's id and session_key (stored in body of request)
    :param city_id: the id of the city being edited
    :param world_id: the id of the world the city is in
    :param details: the new info for the city

    :format details: { name: city name,
                       population: city population,
                       song: city song,
                       trades: city trades,
                       aesthetic: city aesthetic
                       description: city description,
                       revealed: T or F
                     }

    :return: the updated city info, fail format if failure

    :format return: { name: city name,
                  images: [images associated with npc],
                  population: city population,
                  song: city song,
                  trades: city trades,
                  aesthetic: city aesthetic
                  description: city description,
                  associated_npcs: [{id: npc id,
                                     name: npc name}]
                  associated_specials: [{id: special id,
                                         name: special name}],
                  admin_content: {
                        revealed: T or F,
                        edit_date: last time updated
                  } (empty if not admin)
                }
    """
    return cities.edit_city(user_details.user_id, user_details.session_key, city_id,
                            world_id, details)

@router.post('/{city_id}')
async def get_city(user_details: IdSessionKeyFormat, city_id: str, admin: bool):
    """
    This function will get the parameters for a city
    based on admin status, given the user is logged in

    :param user_details: the user's id and session_key (stored in body of request)
    :param city_id: the id of the city
    :param admin: if the user is an admin or not

    :return: the city info in a json format

    :format return: { name: city name,
                      images: [images associated with npc],
                      like_dislike_info: {
                          'likes': number of likes,
                          'dislikes': number of dislikes,
                          'user_like': bool of liked,
                          'user_dislike': bool of disliked
                      }
                      population: city population,
                      song: city song,
                      trades: city trades,
                      aesthetic: city aesthetic
                      description: city description,
                      associated_npcs: [{id: npc id,
                                         name: npc name}]
                      associated_specials: [{id: special id,
                                             name: special name}],
                      admin_content: {
                            revealed: T or F,
                            edit_date: last time updated
                      } (empty if not admin)
                    }
    """
    return cities.get_city(user_details.user_id, user_details.session_key, city_id, admin)

@router.post('/{world_id}/{page}/{limit}')
async def get_cities(user_details: IdSessionKeyFormat, world_id: int, page: int, limit: int):
    """
    This function will get all the cities in a world
    within a limit

    :param user_details: the user's id and session_key (stored in body of request)
    :param world_id: the id of the world being accessed
    :param limit: the number of cities to return
        if None, defaults to 25
    :param page: determines the cities to show

    :return: a list of cities (name, population, and
        revealed status if admin) each in json format

    :format return: [{ name: city name,
                       population: city population,
                       reveal_status: revealed(if admin)}]
    """
    return cities.get_cities(user_details.user_id, user_details.session_key, world_id, limit, page)

@router.post('/search/{world_id}/{param}/{page}/{limit}')
async def search_cities(user_details: IdSessionKeyFormat, world_id: int, param: str, page: int, limit: int):
    """
    This function will search for cities that contain the
    searched string within them.

    :param param: the string to search for
    :param world_id: the world to search in
    :param limit: the number of results to show
    :param page: the selection of elements to show
    :param user_details: the user's id and session_key (stored in body of request)

    :return: the list of cities and their elements that
        meet the search requirements in json format

    :format return: [{ id: the city's id
                       name: city name,
                       reveal_status: { admin: if admin in world
                                        revealed(if admin): True of False}
                    }]
    """
    return cities.search_for_city(param, world_id, limit, page, user_details.user_id, user_details.session_key)