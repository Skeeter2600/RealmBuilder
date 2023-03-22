from fastapi import APIRouter
from src.api.resources.classes import EditCity, NewCity, DeleteCity, ElementDetails, CopyData
import src.components.cities

router = APIRouter(
    prefix='/city',
    tags=['City'],

)


@router.put("/manage", tags=["Edit"])
async def editCity(request_info: EditCity):
    """
    This will edit a city
    """
    outcome = src.components.cities.edit_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                              request_info.city_id, request_info.world_id, request_info.details)
    if outcome[0]:
        return src.components.cities.get_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                              request_info.city_id, True)
    return outcome[0]


@router.post("/manage", tags=["New"])
async def addCity(request_info: NewCity):
    """
    This will create a new city
    """
    outcome = src.components.cities.add_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                             request_info.details)
    if outcome[0]:
        return src.components.cities.get_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                              outcome[1], True)
    return outcome[0]


@router.delete("/manage", tags=["Delete"])
async def deleteCity(request_info: DeleteCity):
    """
    This will delete a city that a user owns
    """
    outcome = src.components.cities.delete_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                                request_info.city_id, request_info.world_id)
    return outcome


@router.post("copy/{city_id}", tags=["Copy"])
async def copy_city(request_info: CopyData, city_id):
    """
    This will make a copy of a city
    """
    outcome = src.components.cities.copy_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                              city_id, request_info.world_id)
    if outcome[0]:
        return src.components.cities.get_city(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                              outcome[1], True)
    return outcome[0]


@router.get("{city_id}", tags=["Details"])
async def get_city(request_info: ElementDetails, city_id):
    """
    This will get the info on a special
    """
    return src.components.cities.get_city(city_id, request_info.AuthoDetails.user_id,
                                          request_info.AuthoDetails.session_key, request_info.admin)
