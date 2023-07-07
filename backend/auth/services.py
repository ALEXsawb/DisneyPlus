from typing import Optional

from fastapi import Response


def get_register_template_response(templates, request, error: Optional[str] = None) -> Response:
    data = {'request': request,
            'title': 'Register',
            'name_of_handler': 'register',
            'path_to_css': 'css/auth/register_and_login.css', }
    if error:
        data.update({'error': error})
    return templates.TemplateResponse('base_form.html', data)


def get_login_template_response(templates, request, error: Optional[str] = None) -> Response:
    data = {'request': request,
            'name_of_handler': 'login',
            'title': 'Login',
            'path_to_css': 'css/auth/register_and_login.css', }
    if error:
        data.update({'error': error})
    return templates.TemplateResponse('login.html', data)
