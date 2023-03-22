from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import List


# General Responses
class SimpleResponse(BaseModel):
    """
    Returns the id and the name
    of the Element requested
    """
    id: int
    name: str


class AdminContent(BaseModel):
    """
    Content that will be included if the requesting user
    is an admin
    """
    hidden_description: str
    revealed: bool
    edit_date: datetime


# Element Responses
class CityAdminContent(BaseModel):
    """
    Content for a city that will be included if
    the requesting user is an admin
    """
    revealed: bool
    edit_date: datetime


class UserResponse(BaseModel):
    """
    Returns the basic info on
    the user requested
    """
    id: int
    username: str
    profile_picture: UploadFile


class CityResponse(BaseModel):
    """
    Return data for a city
    """
    name: str
    images: List[UploadFile]
    population: int
    song: str
    trades: str
    aesthetic: str
    description: str
    associated_npcs: List[SimpleResponse]
    associated_specials: List[SimpleResponse]
    admin_content: CityAdminContent


class CommentResponse(BaseModel):
    """
    Return data related to a comment
    """
    user: List[UserResponse]
    comment: str
    time: datetime
    likes: int
    dislikes: int


class NPCResponse(BaseModel):
    """
    Return data for an npc
    """
    name: str
    images: List[UploadFile]
    age: int
    occupation: str
    description: str
    associated_npcs: List[SimpleResponse]
    associated_special: List[SimpleResponse]
    associated_cities: List[SimpleResponse]
    admin_content: AdminContent


class SpecialResponse(BaseModel):
    """
    Return data for a special
    """
    name: str
    images: List[UploadFile]
    description: str
    associated_npcs: List[SimpleResponse]
    associated_cities: List[SimpleResponse]
    admin_content: AdminContent


class WorldResponse(BaseModel):
    """
    Return data for a world
    """
    valid: bool
    name: str
    description: str
    npcs: List[SimpleResponse]
    cities: List[SimpleResponse]
    specials: List[SimpleResponse]
    comments: List[CommentResponse]
    user_list: List[UserResponse]


# search responses
class SearchAdminChecks(BaseModel):
    """
    Info on admin and if an element is viewable
    """
    admin: bool
    revealed: bool


class SearchResponse(BaseModel):
    """
    Returns data from a city search
    """
    id: int
    name: str
    revealStatus: SearchAdminChecks
