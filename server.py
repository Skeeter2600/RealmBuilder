from fastapi import FastAPI

import src.api.resources.startup as startup
import src.api.elements.users_api as users
import src.api.elements.worlds_api as worlds
import src.api.elements.likes_dislikes_api as likes_dislikes

app = FastAPI()

# resource folder
app.include_router(startup.router)
app.include_router(users.router)
app.include_router(worlds.router)
app.include_router(likes_dislikes.router)