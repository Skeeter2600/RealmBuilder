from fastapi import APIRouter
from pydantic import BaseModel
import src.components.worlds

router = APIRouter(
    prefix='/world',
    tags=['World']
)


class World(BaseModel):
    name: str
    description: str
    owner_id: int
    public: bool


class EditWorld(BaseModel):
    world_id: int
    user_id: int
    session_key: str
    details: World


@router.put("/manage", tags=["Edit"])
async def edit_world(request_info: EditWorld):
    """
    This will edit a world
    """
    outcome = src.components.worlds.edit_world(request_info.world_id, request_info.user_id,
                                               request_info.session_key, request_info.details)
    if outcome[0]:
        return src.components.worlds.get_world_details(request_info.world_id,
                                                       request_info.user_id, request_info.session_key)
    return outcome[0]


class NewWorld(BaseModel):
    name: str
    owner_id: int
    session_key: str


@router.post("/manage", tags=["New"])
async def new_world(request_info: NewWorld):
    """
    This will create a new world
    """
    outcome = src.components.worlds.add_world(request_info.name,
                                              request_info.owner_id, request_info.session_key)
    if outcome[0]:
        return src.components.worlds.get_world_details(outcome[1],
                                                       request_info.owner_id, request_info.session_key)
    return outcome[0]


class DeleteWorld(BaseModel):
    world_id: int
    user_id: int
    session_key: str


@router.delete("/manage", tags=["Delete"])
async def delete_world(request_info: DeleteWorld):
    """
    This will delete a world that a user owns
    """
    return src.components.worlds.delete_world(request_info.world_id,
                                              request_info.user_id, request_info.session_key)


class JoinWorldPublic(BaseModel):
    world_id: int
    user_id: int
    session_key: int


@router.put("/join/public/", tags=["Join", "Public"])
async def join_world_public(request_info: JoinWorldPublic):
    """
    This will have a user join a public world
    """
    return src.components.worlds.join_world_public(request_info.world_id,
                                                   request_info.user_id, request_info.session_key)


class JoinWorldPrivate(BaseModel):
    world_id: int
    user_id: int
    session_key: int
    admin_id: int


@router.put("/join/private/", tags=["Join", "Private"])
async def join_world_public(request_info: JoinWorldPrivate):
    """
    This will have a user join a private world
    """
    return src.components.worlds.join_world_private(request_info.world_id, request_info.user_id,
                                                    request_info.admin_id, request_info.session_key)


@router.get("{world_id}/owner", tags=["Owner", "Details"])
async def get_world_owner(world_id):
    """
    This will retrieve the info of a world owner
    """
    return src.components.worlds.get_owner(world_id)


class WorldAccess(BaseModel):
    user_id: int
    session_key: str


@router.get("{world_id}/admins", tags=["List", "Admins"])
async def get_World_admins(request_info: WorldAccess, world_id):
    """
    This will get the list of admins in a world
    """
    return src.components.worlds.get_world_admin_list(world_id,
                                                      request_info.user_id, request_info.session_key)


@router.get("{world_id}/users", tags=["List", "Users"])
async def get_world_admins(request_info: WorldAccess, world_id):
    """
    This will get the list of users in a world
    """
    return src.components.worlds.get_world_user_list(world_id,
                                                     request_info.user_id, request_info.session_key)


@router.get("{world_id}", tags=["Details"])
async def get_world(request_info: WorldAccess, world_id):
    """
    This will get the info on a world
    """
    return src.components.worlds.get_world_details(world_id,
                                                   request_info.user_id, request_info.session_key)
