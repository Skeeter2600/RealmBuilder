from fastapi import APIRouter
import src.components.specials
from src.api.resources.classes import EditSpecial, NewSpecial, DeleteSpecial, CopyData, ElementDetails, AuthoDetails

router = APIRouter(
    prefix='/special',
    tags=['Special']
)


@router.put("/manage", tags=["Edit"])
async def editSpecial(request_info: EditSpecial):
    """
    This will edit a special's info
    """
    outcome = src.components.specials.edit_special(request_info.AuthoDetails.user_id,
                                                   request_info.AuthoDetails.session_key,
                                                   request_info.special_id, request_info.world_id,
                                                   request_info.details)
    if outcome[0]:
        return src.components.specials.get_special_info(request_info.AuthoDetails.user_id,
                                                        request_info.AuthoDetails.session_key,
                                                        request_info.special_id, True)
    return outcome[0]


@router.post("/manage", tags=["New"])
async def new_special(request_info: NewSpecial):
    """
    This will create a new special
    """
    outcome = src.components.specials.add_special(request_info.AuthoDetails.user_id,
                                                  request_info.AuthoDetails.session_key,
                                                  request_info.details)
    if outcome[0]:
        return src.components.specials.get_special_info(request_info.AuthoDetails.user_id,
                                                        request_info.AuthoDetails.session_key,
                                                        outcome[1], True)
    return outcome[0]


@router.delete("/manage", tags=["Delete"])
async def delete_special(request_info: DeleteSpecial):
    """
    This will delete a special that a user owns
    """
    return src.components.specials.delete_special(request_info.AuthoDetails.user_id,
                                                  request_info.AuthoDetails.session_key,
                                                  request_info.special_id, request_info.world_id)


@router.post("copy/{special_id}", tags=["Copy"])
async def copy_special(request_info: CopyData, special_id):
    """
    This will make a copy of a special
    """
    outcome = src.components.specials.copy_special(request_info.AuthoDetails.user_id,
                                                   request_info.AuthoDetails.session_key,
                                                   special_id, request_info.world_id)
    if outcome[0]:
        return src.components.specials.get_special_info(request_info.AuthoDetails.user_id,
                                                        request_info.AuthoDetails.session_key,
                                                        outcome[1], True)
    return outcome[0]


@router.put("reveal/{world_id}/{special_id}", tags=["Reveal Hidden"])
async def reveal_hidden_special_info(request_info: AuthoDetails, world_id, special_id):
    """
    This will reveal hidden info for a special
    """
    return src.components.specials.reveal_hidden_special(request_info.user_id, request_info.session_key,
                                                         world_id, special_id)


@router.get("/{special_id}", tags=["Details"])
async def special_info(request_info: ElementDetails, special_id):
    """
    This will get the info on a special
    """
    return src.components.specials.get_special_info(special_id,
                                                    request_info.AuthoDetails.user_id,
                                                    request_info.AuthoDetails.session_key,
                                                    request_info.admin)
