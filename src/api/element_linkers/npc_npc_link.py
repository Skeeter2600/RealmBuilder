from typing import List
from fastapi import APIRouter

from src.api.resources.request_classes import NPCNPCLinking, AuthoDetails
from src.api.resources.response_classes import SimpleResponse
from src.linkers.npc_npc_linker import add_npc_npc_association, remove_npc_npc_association, get_associated_npcs

router = APIRouter(
    prefix='/link',
    tags=['NPC']
)


@router.post('/npc/npc', tags=['New', 'Linking'], response_model=bool)
async def add_npc_npc_link(request_info: NPCNPCLinking):
    """
    This function will create a new association
    between two NPCs
    """
    return add_npc_npc_association(request_info.npc_one_id, request_info.npc_two_id,
                                   request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete('/npc/npc', tags=['Delete', 'Linking'], response_model=bool)
async def remove_npc_npc_link(request_info: NPCNPCLinking):
    """
    This function will delete an existing association
    between two NPCs
    """
    return remove_npc_npc_association(request_info.npc_one_id, request_info.npc_two_id,
                                      request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get('/npc/npc/{npc_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_npcs_to_npc(request_info: AuthoDetails, npc_id):
    """
    This function will get a Simple List
    of the cities associated with an NPC
    """
    return get_associated_npcs(request_info.user_id, request_info.session_key, npc_id)
