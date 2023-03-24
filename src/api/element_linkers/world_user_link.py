from typing import List
from fastapi import APIRouter

from src.api.resources.request_classes import WorldUserLinking, AuthoDetails
from src.api.resources.response_classes import SimpleResponse
from src.linkers.admins import add_world_user_admin_association, delete_world_user_admin_association
from src.linkers.world_user_linker import add_world_user_association, delete_world_user_association

router = APIRouter(
    prefix='/link',
    tags=['World', 'User']
)


@router.post('/world/user/', tags=['New', 'Linking'], response_model=bool)
async def add_world_user_link(request_info: WorldUserLinking):
    """
    This function will add a user as a member of a world
    """
    return add_world_user_association(request_info.world_id, request_info.user_id,
                                      request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete('/world/user/', tags=['Delete', 'Linking'], response_model=bool)
async def remove_world_user_link(request_info: WorldUserLinking):
    """
    This function will delete an existing association
    between a user and a world
    """
    return delete_world_user_association(request_info.world_id, request_info.user_id,
                                         request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.post('/world/admin', tags=['New', 'Linking'], response_model=bool)
async def add_world_admin_link(request_info: WorldUserLinking):
    """
    This function will add a user as a member of a world
    """
    return add_world_user_admin_association(request_info.world_id, request_info.user_id,
                                            request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete('/world/admin', tags=['Delete', 'Linking'], response_model=bool)
async def remove_world_admin_link(request_info: WorldUserLinking):
    """
    This function will delete an existing association
    between a user and a world
    """
    return delete_world_user_admin_association(request_info.world_id, request_info.user_id,
                                               request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)

