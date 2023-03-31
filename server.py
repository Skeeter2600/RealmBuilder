import uvicorn
from fastapi import FastAPI

import src.api.element_linkers.city_npc_link as city_npc_linker
import src.api.element_linkers.city_special_link as city_special_linker
import src.api.element_linkers.npc_npc_link as npc_npc_linker
import src.api.element_linkers.npc_special_link as npc_special_linker
import src.api.element_linkers.world_user_link as world_user_linker

import src.api.elements.city as city
import src.api.elements.comment as comment
import src.api.elements.npc as npc
import src.api.elements.special as special
import src.api.elements.user as user
import src.api.elements.world as world
import src.api.elements.like_dislike as like_dislike

import src.api.image_linkers.city_image_link as city_image_link
import src.api.image_linkers.npc_image_link as npc_image_link
import src.api.image_linkers.special_image_link as special_image_link

import src.api.resources.startup as startup
import src.api.resources.search as search


app = FastAPI()

# element-linker folder
app.include_router(city_npc_linker.router)
app.include_router(city_special_linker.router)
app.include_router(npc_npc_linker.router)
app.include_router(npc_special_linker.router)
app.include_router(world_user_linker.router)

# element folder
app.include_router(city.router)
app.include_router(comment.router)
app.include_router(npc.router)
app.include_router(special.router)
app.include_router(user.router)
app.include_router(world.router)
app.include_router(like_dislike.router)

# image-linker folder
app.include_router(city_image_link.router)
app.include_router(npc_image_link.router)
app.include_router(special_image_link.router)

# resource folder
app.include_router(startup.router)
app.include_router(search.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
