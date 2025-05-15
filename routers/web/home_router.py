from fastapi import APIRouter, Request
import common.authenticate as authenticate
from common.template_config import CustomJinja2Templates

home_router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory='templates')

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