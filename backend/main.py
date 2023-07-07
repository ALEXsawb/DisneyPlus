import os

from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from backend.StarWars.views import star_wars
from backend.admin.views import admin
from backend.auth.views import auth
from backend.db import create_user_indexed_fields, create_show_indexed_fields
from backend.download_data_to_DB import load_data_to_DB

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DisneyPlus_dir = os.path.dirname(__file__)
path_to_static = os.path.join(DisneyPlus_dir, 'static')
app.mount('/static', StaticFiles(directory=path_to_static), name='static')
app.include_router(star_wars)
app.include_router(auth)
app.include_router(admin)


@app.exception_handler(ValueError)
async def view_exception_NOT_FOUND(request, exc):
    return PlainTextResponse(exc.__str__(), status_code=status.HTTP_404_NOT_FOUND)


@app.on_event('startup')
async def connect_and_config_db():
    await create_user_indexed_fields()
    await create_show_indexed_fields()
    await load_data_to_DB()
