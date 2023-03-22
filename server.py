from fastapi import FastAPI

import src.api.elements.city as city
import src.api.elements.comment as comment
import src.api.elements.npc as npc
import src.api.elements.special as special
import src.api.elements.user as user
import src.api.elements.world as world

import src.api.image_linkers.city_image_link as city_image_link
import src.api.image_linkers.npc_image_link as npc_image_link
import src.api.image_linkers.special_image_link as special_image_link

import src.api.resources.startup as startup
import src.api.resources.search as search


app = FastAPI()

# element-linker folder

# element folder
app.include_router(city.router)
app.include_router(comment.router)
app.include_router(npc.router)
app.include_router(special.router)
app.include_router(user.router)
app.include_router(world.router)

# image-linker folder
app.include_router(city_image_link.router)
app.include_router(npc_image_link.router)
app.include_router(special_image_link.router)

# resource folder
app.include_router(startup.router)
app.include_router(search.router)
