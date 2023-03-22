from fastapi import APIRouter
import src.components.npcs as npcs
from src.api.resources.request_classes import EditNPC, NewNPC, DeleteNPC, CopyData, AuthoDetails, ElementDetails
from src.api.resources.response_classes import NPCResponse

router = APIRouter(
    prefix='/npc',
    tags=['NPC']
)


@router.put("/manage", tags=["Edit"], response_model=NPCResponse)
async def EditNPC(request_info: EditNPC):
    """
    This will edit an NPC's info
    """
    outcome = npcs.edit_npc(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                            request_info.npc_id, request_info.world_id, request_info.details)
    if outcome[0]:
        return npcs.get_npc_info(request_info.AuthoDetails.user_id,
                                 request_info.AuthoDetails.session_key,
                                 request_info.npc_id, True)
    return outcome[0]


@router.post("/manage", tags=["New"], response_model=NPCResponse)
async def NewNPC(request_info: NewNPC):
    """
    This will create a new npc
    """
    outcome = npcs.add_npc(request_info.AuthoDetails.user_id,
                           request_info.AuthoDetails.session_key, request_info.details)
    if outcome[0]:
        return npcs.get_npc_info(request_info.AuthoDetails.user_id,
                                 request_info.AuthoDetails.session_key,
                                 request_info.npc_id, True)
    return outcome[0]


@router.delete("/manage", tags=["Delete"], response_model=bool)
async def DeleteNPC(request_info: DeleteNPC):
    """
    This will delete an npc that a user owns
    """
    return npcs.delete_npc(request_info.AuthoDetails.user_id,
                           request_info.AuthoDetails.session_key,
                           request_info.npc_id, request_info.world_id)


@router.post("/copy/{npc_id}", tags=["Copy"], response_model=NPCResponse)
async def CopyNPC(request_info: CopyData, npc_id):
    """
    This will make a copy of an npc
    """
    outcome = npcs.copy_npc(request_info.AuthoDetails.user_id,
                            request_info.AuthoDetails.session_key,
                            npc_id, request_info.world_id)
    if outcome[0]:
        return npcs.get_npc_info(request_info.AuthoDetails.user_id,
                                 request_info.AuthoDetails.session_key,
                                 outcome[1], True)
    return outcome[0]


@router.put("/reveal/{world_id}/{npc_id}", tags=["Reveal Hidden"], response_model=NPCResponse)
async def reveal_hidden_npc_info(request_info: AuthoDetails, world_id, npc_id):
    """
    This will reveal hidden info for an npc
    """
    return npcs.reveal_hidden_npc(request_info.user_id,
                                  request_info.session_key,
                                  world_id, npc_id)


@router.get("/{npc_id}", tags=["Details"], response_model=NPCResponse)
async def npc_info(request_info: ElementDetails, npc_id):
    """
    This will get the info on an npc
    """
    return npcs.get_npc_info(npc_id,
                             request_info.AuthoDetails.user_id,
                             request_info.AuthoDetails.session_key,
                             request_info.admin)
