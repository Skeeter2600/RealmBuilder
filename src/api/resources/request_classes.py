from fastapi import UploadFile
from pydantic import BaseModel
from typing import List


# general classes
class ElementList(BaseModel):
    id: int
    
    
class AuthoDetails(BaseModel):
    user_id: int
    session_key: str


class CopyData(BaseModel):
    AuthoDetails: AuthoDetails
    world_id: int


class ElementDetails(BaseModel):
    AuthoDetails: AuthoDetails
    admin: bool


class ImageUpload(BaseModel):
    image: UploadFile
    AuthoDetails: AuthoDetails


class ImageDelete(BaseModel):
    image_id: int
    AuthoDetails: AuthoDetails


# linking classes
class CityNPCLinking(BaseModel):
    city_id: int
    npc_id: int
    AuthoDetails: AuthoDetails


class CitySpecialLinking(BaseModel):
    city_id: int
    special_id: int
    AuthoDetails: AuthoDetails


class NPCNPCLinking(BaseModel):
    npc_one_id: int
    npc_two_id: int
    AuthoDetails: AuthoDetails


class NPCSpecialLinking(BaseModel):
    npc_id: int
    special_id: int
    AuthoDetails: AuthoDetails


class WorldUserLinking(BaseModel):
    world_id: int
    user_id: id
    AuthoDetails: AuthoDetails


# city classes
class EditCityInfo(BaseModel):
    name: str
    population: int
    song: str
    trades: str
    aesthetic: str
    description: str
    revealed: bool


class EditCity(BaseModel):
    AuthoDetails: AuthoDetails
    city_id: int
    world_id: int
    details: EditCityInfo


class NewCityInfo(BaseModel):
    world_id: int
    name: str
    images: List[UploadFile]
    population: int
    song: str
    trades: str
    aesthetic: str
    description: str
    associated_npcs: List[ElementList]
    associated_specials: List[ElementList]


class NewCity(BaseModel):
    AuthoDetails: AuthoDetails
    details: NewCityInfo


class DeleteCity(BaseModel):
    AuthoDetails: AuthoDetails
    city_id: int
    world_id: int


# comment classes
class EditComment(BaseModel):
    AuthoDetails: AuthoDetails
    comment_id: int
    comment: str


class NewComment(BaseModel):
    AuthoDetails: AuthoDetails
    world_id: int
    component_id: int
    component_type: str
    comment: str


class DeleteComment(BaseModel):
    AuthoDetails: AuthoDetails
    comment_id: int


# like_dislike classes
class AddLikeDislike(BaseModel):
    AuthoDetails: AuthoDetails
    like_dislike: bool
    component_id: int
    component_type: str


class RemoveLikeDislike(BaseModel):
    AuthoDetails: AuthoDetails
    component_id: int
    component_type: str


# npc classes
class EditNPCInfo(BaseModel):
    name: str
    age: int
    occupation: str
    hidden_description: str
    revealed: bool


class EditNPC(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    npc_id: int
    details: EditNPCInfo


class NewNPCInfo(BaseModel):
    world_id: int
    name: str
    images: List[UploadFile]
    age: int
    occupation: str
    hidden_description: str
    associated_cities: List[ElementList]


class NewNPC(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    npc_id: int
    details: NewNPCInfo


class DeleteNPC(BaseModel):
    AuthoDetails: AuthoDetails
    npc_id: int
    world_id: int
    
    
# special classes
class EditSpecialInfo(BaseModel):
    name: str
    description: str
    hidden_description: str
    revealed: bool
    edit_date: str


class EditSpecial(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    special_id: int
    details: EditSpecialInfo
    
    
class NewSpecialInfo(BaseModel):
    world_id: int
    name: str
    images: List[UploadFile]
    description: str
    hidden_description: str
    associated_cities: List[ElementList]
    associated_npcs: List[ElementList]


class NewSpecial(BaseModel):
    AuthoDetails: AuthoDetails
    details: NewSpecialInfo
    
    
class DeleteSpecial(BaseModel):
    special_id: int
    AuthoDetails: AuthoDetails
    world_id: int


# user classes
class UserDetails(BaseModel):
    username: str
    profile_pic: UploadFile
    public: bool
    bio: str


class EditUserDetails(BaseModel):
    AuthoDetails: AuthoDetails
    details: UserDetails


class NewUser(BaseModel):
    username: str
    password: str
    email: str


class LoginDetails(BaseModel):
    username: str
    password: str


# world details
class World(BaseModel):
    name: str
    description: str
    owner_id: int
    public: bool


class EditWorld(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    details: World


class NewWorld(BaseModel):
    name: str
    owner_id: int
    session_key: str


class DeleteWorld(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails


class JoinWorldPublic(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails


class JoinWorldPrivate(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    admin_id: int

