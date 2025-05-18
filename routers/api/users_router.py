import traceback
from data.models import UserRegisterData, UserLoginData, User
import services.users_service as user_service
from common import responses, authenticate
from fastapi import APIRouter, Header
from utils.regex_utils import *

api_users_router = APIRouter(prefix='/api/users')

@api_users_router.post('/login')
def user_login(login_data: UserLoginData):
    """
    Authenticate a user and return a token if successful.

    Args:
        login_data (UserLoginData): The user's login credentials.

    Returns:
        str: User authentication token if login is successful.
        BadRequest: If login data is invalid.
        None: If login fails.
    """
    user = user_service.login_user(login_data)
    if not user:
        return responses.BadRequest('Invalid login data.')
    return user_service.encode_user_token(user)
    
    
@api_users_router.post('/register')
def user_register(user_data: UserRegisterData):
    """
    Register a new user.

    Args:
        user_data (UserRegisterData): The user's registration data.

    Returns:
        Created: If user is successfully registered.
        BadRequest: If username is already in use or registration data is invalid.
    """
    
    try:
        if not match_regex(user_data.username, USERNAME_PATTERN):
            return responses.BadRequest("Username must be only letters, numbers and no special characters.")
        
        if not match_regex(user_data.password, PASSWORD_PATTERN):
            return responses.BadRequest("Password must be at least 4 characters long and contains at least 1 letter and 1 number.")
        
    except:
        print(traceback.format_exc())
        return responses.InternalServerError("An error occured while creating your account.")
    
    user = user_service.register_user(user_data)
    if user: 
        return responses.Created('User created.')
    else:
        return responses.BadRequest(f"Username '{user_data.username}' is already in use.")
    

@api_users_router.get('/info', response_model=User, response_model_exclude={"password"})
def user_info(u_token: str = Header()):
    """
    Retrieve information about the authenticated user.

    Args:
        u_token (str): User authentication token from header.

    Returns:
        User: The authenticated user's information, excluding password.
    """
    return authenticate.get_user_or_raise_401(u_token)