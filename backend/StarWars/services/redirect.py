from starlette import status
from starlette.responses import RedirectResponse

from backend.StarWars.services.cookies import logging_in


def login_then_redirect(url, expire_time_in_min, user_id) -> RedirectResponse:
    response = RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)
    logging_in(response, expire_time_in_min, user_id)
    return response
