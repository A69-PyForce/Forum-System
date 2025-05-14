from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from services import users_service
import utils.auth_utils as auth_utils
from data.models import UserLoginData, UserRegisterData

users_router = APIRouter(prefix="/users")
templates = CustomJinja2Templates(directory='templates')

@users_router.get('/login')
def serve_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@users_router.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    
    login_data = UserLoginData(username=username, password=password)
    user = users_service.login_user(login_data)

    if user:
        token = auth_utils.encode_user_token(user)
        response = RedirectResponse(url='/', status_code=302)
        response.set_cookie('u-token', token)
        return response
    else:
        return templates.TemplateResponse(request=request, name="login.html", context={"error": "Wrong username or password."})

@users_router.get('/register')
def serve_register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@users_router.post('/register')
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    
    register_data = UserRegisterData(username=username, password=password, is_admin=0) # is_admin always 0 for now because no field for it
    user = users_service.register_user(register_data)

    if user:
        return RedirectResponse(url='/users/login', status_code=302)
    else:
        return templates.TemplateResponse(request=request, name="register.html", context={"error": "Username already taken."})

@users_router.post('/logout')
def logout():
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie("u-token")
    return response
