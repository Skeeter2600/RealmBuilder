from typing import List

from fastapi import APIRouter, UploadFile
from src.api.resources.request_classes import ImageUpload, ImageDelete
import src.linkers.special_image_linker as special_image_linker

router = APIRouter(
    prefix='/special/image',
    tags=['Special', 'Image Linking']
)


@router.post("/{special_id}/manage", tags=["New"], response_model=bool)
async def add_special_image_link(request_info: ImageUpload, special_id):
    """
    This will add a new image to a special
    """
    return special_image_linker.add_special_image_association(special_id, request_info.image,
                               request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete("/{special_id}/manage", tags=["Delete"], response_model=bool)
async def delete_special_image_link(request_info: ImageDelete, special_id):
    """
    This will delete an existing image from a special
    """
    return special_image_linker.remove_special_image_association(special_id, request_info.image_id,
                                request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get("/{special_id}/", response_model=List[UploadFile])
async def get_special_images(special_id):
    """
    This will get images associated with a special
    """
    return special_image_linker.get_associated_special_images(special_id)
