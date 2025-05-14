from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import common.authenticate as authenticate

home_router = APIRouter(prefix='')
templates = Jinja2Templates(directory='templates')

@home_router.get('/')
def serve_index(request: Request):
    user = None
    token = request.cookies.get('u-token')
    if token:
        try:
            user = authenticate.get_user_or_raise_401(token)
        except Exception:
            user = None
    return templates.TemplateResponse(request=request, name="index.html", context={"user": user})