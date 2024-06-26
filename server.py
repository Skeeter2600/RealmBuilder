from fastapi import FastAPI

import src.api.resources.startup as startup
import src.api.elements.users_api as users

app = FastAPI()

# resource folder
app.include_router(startup.router)
app.include_router(users.router)
