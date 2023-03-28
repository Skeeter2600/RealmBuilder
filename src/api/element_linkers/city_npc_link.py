from typing import List
from fastapi import APIRouter

from src.api.resources.request_classes import CityNPCLinking, AuthoDetails
from src.api.resources.response_classes import SimpleResponse
from src.linkers.city_npc_linker import add_city_npc_association, remove_city_npc_association, get_cities_by_npc, \
    get_npcs_by_city

router = APIRouter(
    prefix='/link',
    tags=['City', 'NPC']
)


@router.post('/city/npc', tags=['New', 'Linking'], response_model=bool)
async def add_city_npc_link(request_info: CityNPCLinking):
    """
    This function will create a new association
    between a city and an NPC
    """
    return add_city_npc_association(request_info.city_id, request_info.npc_id,
                                    request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete('/city/npc', tags=['Delete', 'Linking'], response_model=bool)
async def remove_city_npc_link(request_info: CityNPCLinking):
    """
    This function will delete an existing association
    between a city and an NPC
    """
    return remove_city_npc_association(request_info.city_id, request_info.npc_id,
                                       request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get('/npc/city/{npc_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_cities_to_npc(request_info: AuthoDetails, npc_id):
    """
    This function will get a Simple List
    of the cities associated with an NPC
    """
    return get_cities_by_npc(request_info.user_id, request_info.session_key, npc_id)


@router.get('/city/npc/{city_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_npcs_to_city(request_info: AuthoDetails, city_id):
    """
    This function will get a Simple List
    of the NPCs associated with a city
    """
    return get_npcs_by_city(request_info.user_id, request_info.session_key, city_id)
