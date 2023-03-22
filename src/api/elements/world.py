from typing import List

from fastapi import APIRouter
import src.components.worlds as worlds
from src.api.resources.request_classes import EditWorld, NewWorld, DeleteWorld, JoinWorldPublic, JoinWorldPrivate, \
    AuthoDetails
from src.api.resources.response_classes import WorldResponse, UserResponse

router = APIRouter(
    prefix='/world',
    tags=['World']
)


@router.put("/manage", tags=["Edit"], response_model=WorldResponse)
async def edit_world(request_info: EditWorld):
    """
    This will edit a world
    """
    outcome = worlds.edit_world(request_info.world_id, request_info.AuthoDetails.user_id,
                                request_info.AuthoDetails.session_key, request_info.details)
    if outcome[0]:
        return worlds.get_world_details(request_info.world_id,
                                        request_info.AuthoDetails.user_id,
                                        request_info.AuthoDetails.session_key)
    return outcome[0]


@router.post("/manage", tags=["New"], response_model=WorldResponse)
async def new_world(request_info: NewWorld):
    """
    This will create a new world
    """
    outcome = worlds.add_world(request_info.name,
                               request_info.owner_id,
                               request_info.session_key)
    if outcome[0]:
        return worlds.get_world_details(outcome[1],
                                        request_info.owner_id,
                                        request_info.session_key)
    return outcome[0]


@router.delete("/manage", tags=["Delete"], response_model=bool)
async def delete_world(request_info: DeleteWorld):
    """
    This will delete a world that a user owns
    """
    return worlds.delete_world(request_info.world_id,
                               request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.put("/join/public/", tags=["Join"], response_model=bool)
async def join_world_public(request_info: JoinWorldPublic):
    """
    This will have a user join a public world
    """
    return worlds.join_world_public(request_info.world_id,
                                    request_info.AuthoDetails.user_id,
                                    request_info.AuthoDetails.session_key)


@router.put("/join/private/", tags=["Join"], response_model=bool)
async def join_world_public(request_info: JoinWorldPrivate):
    """
    This will have a user join a private world
    """
    return worlds.join_world_private(request_info.world_id, request_info.AuthoDetails.user_id,
                                     request_info.admin_id, request_info.AuthoDetails.session_key)


@router.get("/{world_id}/owner", tags=["Details"], response_model=UserResponse)
async def get_world_owner(world_id):
    """
    This will retrieve the info of a world owner
    """
    return worlds.get_owner(world_id)


@router.get("/{world_id}/admins", tags=["List"], response_model=List[UserResponse])
async def get_World_admins(request_info: AuthoDetails, world_id):
    """
    This will get the list of admins in a world
    """
    return worlds.get_world_admin_list(world_id,
                                       request_info.user_id, request_info.session_key)


@router.get("/{world_id}/users", tags=["List"], response_model=List[UserResponse])
async def get_world_users(request_info: AuthoDetails, world_id):
    """
    This will get the list of users in a world
    """
    return worlds.get_world_user_list(world_id,
                                      request_info.user_id, request_info.session_key)


@router.get("/{world_id}", tags=["Details"], response_model=WorldResponse)
async def get_world(request_info: AuthoDetails, world_id):
    """
    This will get the info on a world
    """
    return worlds.get_world_details(world_id,
                                    request_info.user_id, request_info.session_key)
