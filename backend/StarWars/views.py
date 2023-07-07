import os

from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from backend.admin.views import broadcast_visit
from backend.db.db import shows
from backend.models.UserModel import UserModel
from backend.schemas.Visit import Visit

star_wars = APIRouter(prefix='/star_wars')

star_wars_dir = os.path.dirname(__file__)
path_to_templates = os.path.join(star_wars_dir, "../templates/star_wars")
PATH_TO_IMG = 'images/star_wars/'

templates = Jinja2Templates(directory=path_to_templates)


@star_wars.get('', status_code=status.HTTP_200_OK, name='star_wars')
async def home_page(request: Request):
    data = {}
    if request.cookies.get('logged_in'):
        data['logged_in'] = True
    else:
        return RedirectResponse(request.url_for('login')._url, status_code=status.HTTP_303_SEE_OTHER)
    show = await shows.find_one({'show': 'StarWars'}, {'content.content': 0})
    data.update({'request': request,
                 'title': show['show'],
                 'path_to_css': 'css/star_wars/home.css',
                 'path_to_background_img': PATH_TO_IMG + 'DarthVader.jpg',
                 'history': show['history'],
                 'content': show['content']})
    return templates.TemplateResponse('home.html', data)


@star_wars.get("/motions/{slug}", status_code=status.HTTP_200_OK, name='motion_picture')
async def get_motion(request: Request, slug: str):
    data = {}
    if request.cookies.get('logged_in'):
        data['logged_in'] = True
    else:
        return RedirectResponse(request.url_for('login')._url, status_code=status.HTTP_303_SEE_OTHER)
    content = await shows.find_one({'show': 'StarWars', 'content.slug': slug},
                                   {'content': {'$elemMatch': {'slug': slug}}})
    content = content['content'][0]
    data.update({'request': request,
                 'title': content['title'],
                 'path_to_css': 'css/star_wars/motion_picture.css',
                 'path_to_background_img': PATH_TO_IMG + content['path_to_img'],
                 'content': content['content']})
    if request.cookies.get('logged_in'):
        data['logged_in'] = True
    return templates.TemplateResponse('motion_picture.html', data)


@star_wars.post('/visit', status_code=status.HTTP_202_ACCEPTED, name='visit')
async def set_new_visit(data: Visit) -> dict:
    await UserModel.add_visit(data)
    await broadcast_visit(data)
    return data
