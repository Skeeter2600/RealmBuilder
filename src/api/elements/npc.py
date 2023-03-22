from fastapi import APIRouter
import src.components.npcs
from src.api.resources.classes import EditNPC, NewNPC, DeleteNPC, CopyData, AuthoDetails, ElementDetails

router = APIRouter(
    prefix='/npc',
    tags=['NPC']
)


@router.put("/manage", tags=["Edit"])
async def EditNPC(request_info: EditNPC):
    """
    This will edit an NPC's info
    """
    outcome = src.components.npcs.edit_npc(request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key,
                                           request_info.npc_id, request_info.world_id, request_info.details)
    if outcome[0]:
        return src.components.npcs.get_npc_info(request_info.AuthoDetails.user_id,
                                                request_info.AuthoDetails.session_key,
                                                request_info.npc_id, True)
    return outcome[0]


@router.post("/manage", tags=["New"])
async def NewNPC(request_info: NewNPC):
    """
    This will create a new npc
    """
    outcome = src.components.npcs.add_npc(request_info.AuthoDetails.user_id,
                                          request_info.AuthoDetails.session_key, request_info.details)
    if outcome[0]:
        return src.components.npcs.get_npc_info(request_info.AuthoDetails.user_id,
                                                request_info.AuthoDetails.session_key,
                                                request_info.npc_id, True)
    return outcome[0]


@router.delete("/manage", tags=["Delete"])
async def DeleteNPC(request_info: DeleteNPC):
    """
    This will delete an npc that a user owns
    """
    return src.components.npcs.delete_npc(request_info.AuthoDetails.user_id,
                                          request_info.AuthoDetails.session_key,
                                          request_info.npc_id, request_info.world_id)


@router.post("copy/{npc_id}", tags=["Copy"])
async def CopyNPC(request_info: CopyData, npc_id):
    """
    This will make a copy of an npc
    """
    outcome = src.components.npcs.copy_npc(request_info.AuthoDetails.user_id,
                                           request_info.AuthoDetails.session_key,
                                           npc_id, request_info.world_id)
    if outcome[0]:
        return src.components.npcs.get_npc_info(request_info.AuthoDetails.user_id,
                                                request_info.AuthoDetails.session_key,
                                                outcome[1], True)
    return outcome[0]


@router.put("/reveal/{world_id}/{npc_id}", tags=["Reveal Hidden"])
async def reveal_hidden_npc_info(request_info: AuthoDetails, world_id, npc_id):
    """
    This will reveal hidden info for an npc
    """
    return src.components.npcs.reveal_hidden_npc(request_info.user_id,
                                                 request_info.session_key,
                                                 world_id, npc_id)


@router.get("/{npc_id}", tags=["Details"])
async def npc_info(request_info: ElementDetails, npc_id):
    """
    This will get the info on an npc
    """
    return src.components.npcs.get_npc_info(npc_id,
                                            request_info.AuthoDetails.user_id,
                                            request_info.AuthoDetails.session_key,
                                            request_info.admin)
