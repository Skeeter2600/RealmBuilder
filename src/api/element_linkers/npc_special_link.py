from typing import List
from fastapi import APIRouter

from src.api.resources.request_classes import NPCSpecialLinking, AuthoDetails
from src.api.resources.response_classes import SimpleResponse
from src.linkers.npc_special_linker import add_npc_special_association, remove_npc_special_association, \
    get_specials_by_npc, get_npcs_by_special

router = APIRouter(
    prefix='/link',
    tags=['Special', 'NPC']
)


@router.post('/npc/special', tags=['New', 'Linking'], response_model=bool)
async def add_npc_special_link(request_info: NPCSpecialLinking):
    """
    This function will create a new association
    between an NPC and a special
    """
    return add_npc_special_association(request_info.npc_id, request_info.special_id,
                                       request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete('/npc/special', tags=['Delete', 'Linking'], response_model=bool)
async def remove_npc_special_link(request_info: NPCSpecialLinking):
    """
    This function will delete an existing association
    between a special and an NPC
    """
    return remove_npc_special_association(request_info.npc_id, request_info.special_id,
                                          request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get('/npc/special/{npc_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_specials_to_npc(request_info: AuthoDetails, npc_id):
    """
    This function will get a Simple List
    of the specials associated with an NPC
    """
    return get_specials_by_npc(request_info.user_id, request_info.session_key, npc_id)


@router.get('/special/npc/{special_id}', tags=['Linked'], response_model=List[SimpleResponse])
async def get_npcs_to_special(request_info: AuthoDetails, special_id):
    """
    This function will get a Simple List
    of the NPCs associated with a special
    """
    return get_npcs_by_special(request_info.user_id, request_info.session_key, special_id)
