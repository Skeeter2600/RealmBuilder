from typing import List

from fastapi import APIRouter, UploadFile
from src.api.resources.request_classes import ImageUpload, ImageDelete
import src.linkers.npc_image_linker as npc_image_linker

router = APIRouter(
    prefix='/npc/image',
    tags=['NPC', 'Image Linking']
)


@router.post("/{npc_id}/manage", tags=["New"], response_model=bool)
async def add_npc_image_link(request_info: ImageUpload, npc_id):
    """
    This will add a new image to an npc
    """
    return npc_image_linker.add_npc_image_association(npc_id, request_info.image,
                               request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete("/{npc_id}/manage", tags=["Delete"], response_model=bool)
async def delete_npc_image_link(request_info: ImageDelete, npc_id):
    """
    This will delete an existing image from an npc
    """
    return npc_image_linker.remove_npc_image_association(npc_id, request_info.image_id,
                                request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get("/{npc_id}/", response_model=List[UploadFile])
async def get_npc_images(npc_id):
    """
    This will get images associated with an npc
    """
    return npc_image_linker.get_associated_npc_images(npc_id)
