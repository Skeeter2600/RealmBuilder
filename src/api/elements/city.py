from fastapi import APIRouter
from src.api.resources.request_classes import EditCity, NewCity, DeleteCity, ElementDetails, CopyData
import src.components.cities as cities
from src.api.resources.response_classes import CityResponse

router = APIRouter(
    prefix='/city',
    tags=['City']
)


@router.put("/manage", tags=["Edit"], response_model=CityResponse)
async def editCity(request_info: EditCity):
    """
    This will edit a city
    """
    outcome = cities.edit_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                               request_info.city_id, request_info.world_id, request_info.details)
    if outcome[0]:
        return cities.get_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                               request_info.city_id, True)
    return outcome[0]


@router.post("/manage", tags=["New"], response_model=CityResponse)
async def addCity(request_info: NewCity):
    """
    This will create a new city
    """
    outcome = cities.add_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                              request_info.details)
    if outcome[0]:
        return cities.get_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                               outcome[1], True)
    return outcome[0]


@router.delete("/manage", tags=["Delete"], response_model=bool)
async def deleteCity(request_info: DeleteCity):
    """
    This will delete a city that a user owns
    """
    outcome = cities.delete_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                 request_info.city_id, request_info.world_id)
    return outcome


@router.post("/copy/{city_id}", tags=["Copy"], response_model=CityResponse)
async def copy_city(request_info: CopyData, city_id):
    """
    This will make a copy of a city
    """
    outcome = cities.copy_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                               city_id, request_info.world_id)
    if outcome[0]:
        return cities.get_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                               outcome[1], True)
    return outcome[0]


@router.get("/{city_id}", tags=["Details"], response_model=CityResponse)
async def get_city(request_info: ElementDetails, city_id):
    """
    This will get the info on a city
    """
    return cities.get_city(city_id, request_info.AuthoDetails.user_id,
                           request_info.AuthoDetails.session_key, request_info.admin)
