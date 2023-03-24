from typing import List
from fastapi import APIRouter

from src.api.resources.request_classes import CitySpecialLinking, AuthoDetails
from src.api.resources.response_classes import SimpleResponse
from src.linkers.city_special_linker import add_city_special_association, remove_city_special_association, \
    get_cities_by_special, get_specials_by_city

router = APIRouter(
    prefix='/link',
    tags=['City', 'Special']
)


@router.post('/city/special', tags=['New', 'Linking'], response_model=bool)
async def add_city_npc_link(request_info: CitySpecialLinking):
    """
    This function will create a new association
    between a city and a special
    """
    return add_city_special_association(request_info.city_id, request_info.special_id,
                                       request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete('/city/special', tags=['Delete', 'Linking'], response_model=bool)
async def remove_city_npc_link(request_info: CitySpecialLinking):
    """
    This function will delete an existing association
    between a city and a special
    """
    return remove_city_special_association(request_info.city_id, request_info.special_id,
                                           request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get('/special/city/{special_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_cities_to_special(request_info: AuthoDetails, special_id):
    """
    This function will get a Simple List
    of the cities associated with a special
    """
    return get_cities_by_special(request_info.user_id, request_info.session_key, special_id)


@router.get('/city/special/{city_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_specials_to_city(request_info: AuthoDetails, city_id):
    """
    This function will get a Simple List
    of the specials associated with a city
    """
    return get_specials_by_city(request_info.user_id, request_info.session_key, city_id)

