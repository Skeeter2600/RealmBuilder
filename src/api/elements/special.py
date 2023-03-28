from fastapi import APIRouter
import src.components.specials as specials
from src.api.resources.request_classes import EditSpecial, NewSpecial, DeleteSpecial, CopyData, ElementDetails, \
    AuthoDetails
from src.api.resources.response_classes import SpecialResponse

router = APIRouter(
    prefix='/special',
    tags=['Special']
)


@router.put("/manage", tags=["Edit"], response_model=SpecialResponse)
async def editSpecial(request_info: EditSpecial):
    """
    This will edit a special's info
    """
    outcome = specials.edit_special(request_info.AuthoDetails.user_id,
                                    request_info.AuthoDetails.session_key,
                                    request_info.special_id, request_info.world_id,
                                    request_info.details)
    if outcome[0]:
        return specials.get_special_info(request_info.AuthoDetails.user_id,
                                         request_info.AuthoDetails.session_key,
                                         request_info.special_id, True)
    return outcome[0]


@router.post("/manage", tags=["New"], response_model=SpecialResponse)
async def new_special(request_info: NewSpecial):
    """
    This will create a new special
    """
    outcome = specials.add_special(request_info.AuthoDetails.user_id,
                                   request_info.AuthoDetails.session_key,
                                   request_info.details)
    if outcome[0]:
        return specials.get_special_info(request_info.AuthoDetails.user_id,
                                         request_info.AuthoDetails.session_key,
                                         outcome[1], True)
    return outcome[0]


@router.delete("/manage", tags=["Delete"], response_model=bool)
async def delete_special(request_info: DeleteSpecial):
    """
    This will delete a special that a user owns
    """
    return specials.delete_special(request_info.AuthoDetails.user_id,
                                   request_info.AuthoDetails.session_key,
                                   request_info.special_id, request_info.world_id)


@router.post("/copy/{special_id}", tags=["Copy"], response_model=SpecialResponse)
async def copy_special(request_info: CopyData, special_id):
    """
    This will make a copy of a special
    """
    outcome = specials.copy_special(request_info.AuthoDetails.user_id,
                                    request_info.AuthoDetails.session_key,
                                    special_id, request_info.world_id)
    if outcome[0]:
        return specials.get_special_info(request_info.AuthoDetails.user_id,
                                         request_info.AuthoDetails.session_key,
                                         outcome[1], True)
    return outcome[0]


@router.put("/reveal/{world_id}/{special_id}", tags=["Reveal Hidden"], response_model=SpecialResponse)
async def reveal_hidden_special_info(request_info: AuthoDetails, world_id, special_id):
    """
    This will reveal hidden info for a special
    """
    return specials.reveal_hidden_special(request_info.user_id, request_info.session_key,
                                          world_id, special_id)


@router.get("/{special_id}", tags=["Details"], response_model=SpecialResponse)
async def special_info(request_info: ElementDetails, special_id):
    """
    This will get the info on a special
    """
    return specials.get_special_info(special_id,
                                     request_info.AuthoDetails.user_id,
                                     request_info.AuthoDetails.session_key,
                                     request_info.admin)
