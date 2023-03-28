from typing import List

from fastapi import APIRouter, UploadFile
from src.api.resources.request_classes import ImageUpload, ImageDelete
import src.linkers.city_image_linker as city_image_linker

router = APIRouter(
    prefix='/city/image',
    tags=['City', 'Image Linking']
)


@router.post("/{city_id}/manage", tags=["New"], response_model=bool)
async def add_city_image_link(request_info: ImageUpload, city_id):
    """
    This will add a new image to a city
    """
    return city_image_linker.add_city_image_association(city_id, request_info.image,
                               request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.delete("/{city_id}/manage", tags=["Delete"], response_model=bool)
async def delete_city_image_link(request_info: ImageDelete, city_id):
    """
    This will delete an existing image from a city
    """
    return city_image_linker.remove_city_image_association(city_id, request_info.image_id,
                                request_info.AuthoDetails.user_id, request_info.AuthoDetails.session_key)


@router.get("/{city_id}/", response_model=List[UploadFile])
async def get_city_images(city_id):
    """
    This will get images associated with a city
    """
    return city_image_linker.get_associated_city_images(city_id)
