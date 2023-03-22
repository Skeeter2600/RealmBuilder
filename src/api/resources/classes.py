from fastapi import File
from pydantic import BaseModel
from typing import List, Optional


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


# city classes
class EditCityDets(BaseModel):
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
    details: EditCityDets


class NewCityDets(BaseModel):
    world_id: int
    name: str
    # images: List[File] = None
    population: int
    song: str
    trades: str
    aesthetic: str
    description: str
    #associated_npcs: List[ElementList] = None
    #associated_specials: List[ElementList] = None


class NewCity(BaseModel):
    AuthoDetails: AuthoDetails
    details: NewCityDets


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


# npc classes
class EditNPCDets(BaseModel):
    name: str
    age: int
    occupation: str
    hidden_description: str
    revealed: bool


class EditNPC(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    npc_id: int
    details: EditNPCDets


class NewNPCDets(BaseModel):
    world_id: int
    name: str
    #images: list[File]
    age: int
    occupation: str
    hidden_description: str
    #associated_cities: list[ElementList]


class NewNPC(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    npc_id: int
    details: NewNPCDets


class DeleteNPC(BaseModel):
    AuthoDetails: AuthoDetails
    npc_id: int
    world_id: int
    
    
# special classes
class EditSpecialDets(BaseModel):
    name: str
    description: str
    hidden_description: str
    revealed: bool
    edit_date: str


class EditSpecial(BaseModel):
    world_id: int
    AuthoDetails: AuthoDetails
    special_id: int
    details: EditSpecialDets
    
    
class NewSpecialDets(BaseModel):
    world_id: int
    name: str
    #images: List[File]
    description: str
    hidden_description: str
    #associated_cities: List[ElementList]
    #associated_npcs: List[ElementList]


class NewSpecial(BaseModel):
    AuthoDetails: AuthoDetails
    details: NewSpecialDets
    
    
class DeleteSpecial(BaseModel):
    special_id: int
    AuthoDetails: AuthoDetails
    world_id: int


# user classes
class UserDetails(BaseModel):
    username: str
    #profile_pic: File
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
