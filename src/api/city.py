from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel
import src.components.cities

router = APIRouter(
    prefix='/city',
    tags=['City']
)


class City(BaseModel):
    name: str
    population: int
    song: str
    trades: str
    aesthetic: str
    description: str
    revealed: bool
    edit_date: datetime
    world_id: int


class EditCity(BaseModel):
    user_id: int
    session_key: str
    city_id: int
    world_id: int
    details: City


@router.put("/manage", tags=["Edit"])
async def editCity(request_info: EditCity):
    """
    This will edit a city
    """
    outcome = src.components.cities.edit_city(request_info.user_id, request_info.session_key,
                                              request_info.city_id, request_info.details.world_id, request_info.details)
    if outcome[0]:
        return src.components.cities.get_city(request_info.user_id, request_info.session_key,
                                              request_info.city_id, True)
    return outcome[0]


class NewCity(BaseModel):
    user_id: int
    session_key: str
    details: City


@router.post("/manage", tags=["New"])
async def addCity(request_info: NewCity):
    """
    This will create a new city
    """
    outcome = src.components.cities.add_city(request_info.user_id, request_info.session_key,
                                             request_info.details)
    if outcome[0]:
        return src.components.cities.get_city(request_info.user_id, request_info.session_key,
                                              outcome[1], True)
    return outcome[0]


class DeleteCity(BaseModel):
    user_id: int
    session_key: str
    city_id: int
    world_id: int


@router.delete("/manage", tags=["Delete"])
async def deleteCity(request_info: DeleteCity):
    """
    This will delete a city that a user owns
    """
    outcome = src.components.cities.delete_city(request_info.user_id, request_info.session_key,
                                                request_info.city_id, request_info.world_id)
    return outcome


class CopyCity(BaseModel):
    user_id: int
    session_key: str
    world_id: int


@router.post("copy/{city_id}", tags=["Copy"])
async def copy_city(request_info: CopyCity, city_id):
    """
    This will make a copy of a city
    """
    outcome = src.components.cities.copy_city(request_info.user_id, request_info.session_key,
                                              city_id, request_info.world_id)
    if outcome[0]:
        return src.components.cities.get_city(request_info.user_id, request_info.session_key,
                                              outcome[1], True)
    return outcome[0]


class CityDetails(BaseModel):
    user_id: int
    session_key: str
    admin: bool


@router.get("{city_id}", tags=["Details"])
async def get_city(request_info: CityDetails, city_id):
    """
    This will get the info on a special
    """
    return src.components.cities.get_city(city_id, request_info.user_id,
                                          request_info.session_key, request_info.admin)
