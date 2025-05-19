import io
import traceback
import cloudinary
from PIL import Image
import cloudinary.uploader
from utils.regex_utils import *
from services import users_service
import utils.auth_utils as auth_utils
from data.database import CLDNR_CONFIG
import common.authenticate as authenticate
from fastapi.responses import RedirectResponse
from data.models import UserLoginData, UserRegisterData
from common.template_config import CustomJinja2Templates
from fastapi import APIRouter, Request, Form, File, UploadFile

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
    
    try:
        
        if not match_regex(username, USERNAME_PATTERN):
            return templates.TemplateResponse(request=request, name="register.html", context={
        "error": "Username must be only letters, numbers and no special characters."
        })
            
        if not match_regex(password, PASSWORD_PATTERN):
            return templates.TemplateResponse(request=request, name="register.html", context={
        "error": "Password must be at least 4 characters long and contains at least 1 letter and 1 number."
        })
    
        register_data = UserRegisterData(username=username, password=password, is_admin=0)
        
    except:
        print(traceback.format_exc())
        return templates.TemplateResponse(request=request, name="register.html", context={
        "error": "An error occured while creating your account."
    })
    
    user = users_service.register_user(register_data)

    if user:
        return RedirectResponse(url='/users/login', status_code=302)
    else:
        return templates.TemplateResponse(request=request, name="register.html", context={"error": "Username already taken."})

@users_router.post('/logout')
def logout():
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie("u-token")
    return response # del auth cookie and redirect to homepage

@users_router.get('/info')
def info(request: Request):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    user.password = "" # Hide password hash NO TOUCHEY!!!
    return templates.TemplateResponse(request=request, name="user_info.html", context={"user": user})

@users_router.post('/avatar')
def change_avatar(request: Request, file: UploadFile = File(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    if CLDNR_CONFIG:
        
        try:
            # Read uploader image
            image_contents = file.file.read()
            
            # Process image with Pillow & resize
            image = Image.open(io.BytesIO(image_contents))
            resized_image = image.resize((192, 192))
            
            # Save resized image to buffer
            buffer = io.BytesIO()
            resized_image.save(buffer, format=image.format or "JPEG")
            buffer.seek(0)
            
            # Upload image with Cloudinary and get the generated URL
            result = cloudinary.uploader.upload(buffer, folder="forum-system-user-avatars")
            image_url = result["secure_url"]
            
            # Set avatar url in DB and redirect to same page to refresh
            users_service.update_user_avatar_url(user.id, image_url)
            return RedirectResponse("/users/info", status_code=302)
        
        except:
            print(traceback.format_exc())
            pass
    
    return templates.TemplateResponse(request=request, name="user_info.html", context={"user": user, "error": "Avatar service unavailable."})