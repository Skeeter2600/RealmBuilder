from typing import List

from fastapi import APIRouter

from src.api.resources.request_classes import AuthoDetails
from src.api.resources.response_classes import UserResponse, SimpleResponse
from src.components.cities import search_for_city
from src.components.npcs import search_for_npc
from src.components.specials import search_for_special
from src.components.users import search_user
from src.components.worlds import search_world

router = APIRouter(
    prefix='/search',
    tags=['Search']
)


@router.get("/city/{world_id}/{param}/{limit}/{page}/", tags=["City"], response_model=List[SimpleResponse])
async def CitySearch(request_info: AuthoDetails, param, world_id, limit, page):
    """
    This will search a city by the defined parameters
    """
    return search_for_city(param, world_id, limit, page,
                           request_info.user_id, request_info.session_key)


@router.get("/npc/{world_id}/{param}/{limit}/{page}/", tags=["NPC"], response_model=List[SimpleResponse])
async def NPCSearch(request_info: AuthoDetails, param, world_id, limit, page):
    """
    This will search a city by the defined parameters
    """
    return search_for_npc(param, world_id, limit, page,
                          request_info.user_id, request_info.session_key)


@router.get("/special/{world_id}/{param}/{limit}/{page}/", tags=["Special"], response_model=List[SimpleResponse])
async def SpecialSearch(request_info: AuthoDetails, param, world_id, limit, page):
    """
    This will search a special by the defined parameters
    """
    return search_for_special(param, world_id, limit, page,
                              request_info.user_id, request_info.session_key)


@router.get("/user/{param}/{limit}/{page}/", tags=["User"], response_model=List[UserResponse])
async def UserSearch(request_info: AuthoDetails, param, limit, page):
    """
    This will for a search a user by the defined parameters
    """
    return search_user(param, limit, page,
                       request_info.user_id, request_info.session_key)


@router.get("/world/{param}/{limit}/{page}", tags=["World"], response_model=List[SimpleResponse])
async def WorldSearch(request_info: AuthoDetails, param, limit, page):
    """
    This will search a world by the defined parameters
    """
    return search_world(param, limit, page,
                        request_info.user_id, request_info.session_key)
