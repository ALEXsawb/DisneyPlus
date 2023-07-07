import os
from typing import Annotated

from fastapi import APIRouter, Request, Form
from pymongo.errors import DuplicateKeyError
from starlette import status
from pydantic import EmailStr
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from backend.StarWars.services.redirect import login_then_redirect
from backend.admin.views import broadcast_user
from backend.auth.services import get_register_template_response, get_login_template_response
from backend.models.UserModel import UserModel
from backend.settings import settings
from backend.schemas.User import User

auth = APIRouter()

auth_dir = os.path.dirname(__file__)
path_to_templates = os.path.join(auth_dir, "../templates/auth")
templates = Jinja2Templates(directory=path_to_templates)

COOKIES_EXPIRES_IN = settings.COOKIES_EXPIRES_IN


@auth.post('/register', response_class=RedirectResponse, name='register')
async def create_user(request: Request, email: Annotated[EmailStr, Form()], password:  Annotated[str, Form()]):
    email = email.lower()
    user = UserModel(email=email, password=password, visits=[])
    try:
        await user.save()
        await broadcast_user(User.parse_obj(user.dict()))
    except DuplicateKeyError:
        return get_register_template_response(templates, request,
                                              error='The user with this email already exists in the system')
    return login_then_redirect(request.url_for('star_wars')._url, COOKIES_EXPIRES_IN, user.id)


@auth.get('/register', status_code=status.HTTP_201_CREATED, name='register_page')
async def get_create_user_page(request: Request):
    if request.cookies.pop('end_user_id', None) and request.cookies.pop('logged_in', None):
        return RedirectResponse(request.url_for('star_wars')._url, status_code=status.HTTP_303_SEE_OTHER)
    return get_register_template_response(templates, request)


@auth.get('/login', status_code=status.HTTP_201_CREATED, name='login_page')
async def get_login_user_page(request: Request):
    if request.cookies.pop('end_user_id', None) and request.cookies.pop('logged_in', None):
        return RedirectResponse(request.url_for('star_wars')._url, status_code=status.HTTP_303_SEE_OTHER)
    return get_login_template_response(templates, request)


@auth.post('/login', name='login')
async def login(request: Request, email: Annotated[EmailStr, Form()], password:  Annotated[str, Form()],):
    try:
        user = await UserModel.verified(email=email, password=password)
    except ValueError as e:
        if e.__str__() == 'Incorrect Email or Password':
            return get_login_template_response(templates, request, error='Incorrect Email or Password')
    return login_then_redirect(request.url_for('star_wars')._url, COOKIES_EXPIRES_IN, user['_id'])


@auth.get('/logout', status_code=status.HTTP_200_OK, name='logout')
async def logout(request: Request):
    response = RedirectResponse(request.url_for('login')._url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie('logged_in', '', -1)
    response.set_cookie('end_user_id', '', -1)
    return response
