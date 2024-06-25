from fastapi import FastAPI

import src.api.resources.startup as startup

app = FastAPI()

# resource folder
app.include_router(startup.router)
